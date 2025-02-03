import streamlit as st
import yfinance as yf
from utils import scrape_spy_tickers, compute_default_values, reset_inputs_to_default
from plotting import historical_stock_cumulative_return_chart
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
from mpt_funcs import negative_sharpe_ratio, minimize_variance, portfolio_performance

# Page Configuration
st.set_page_config(
    page_title="S&P 500 Portfolio Optimization & Sharpe Ratio Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for reset flag used to reload app when selected equity changes
if "reset_flag" not in st.session_state:
    st.session_state.reset_flag = False

# Store default values in session state
if "default_values" not in st.session_state or st.session_state.reset_flag:
    st.session_state.default_values = compute_default_values()
    st.session_state.update(st.session_state.default_values)
    st.session_state.reset_flag = False
    st.rerun()

st.title("Portfolio Optimization & Sharpe Ratio Analysis")

with st.sidebar:
    tickers = st.multiselect(
        "Select Portfolio Tickers",
        scrape_spy_tickers(),
        key='tickers'
    )

    # If tickers have changed, trigger reset logic
    if tickers != st.session_state.tickers:
        st.session_state.tickers = tickers
        st.session_state.reset_flag = True
        st.rerun()

    st.write("Select Portfolio Tickers:", tickers)

    if st.sidebar.button("Reset Below Inputs to Default"):
        reset_inputs_to_default()

    start_date = st.sidebar.date_input("Start Date", key="start_date")
    end_date = st.sidebar.date_input("End Date", key="end_date")

    # If the start or end data has changed, trigger reset logic
    if start_date != st.session_state.start_date or end_date != st.session_state.end_date:
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date
        st.session_state.reset_flag = True
        st.rerun()

    risk_free_rate = st.sidebar.number_input(
        "Enter Annualized Risk-Free Rate value or use 10yr T-Note Default",
        min_value=0.0,  # Minimum value of 0 (no strike below 0)
        step=0.01,  # Increment step
        format="%.2f",
        key='risk_free_rate_input'
    ) / 100

    if len(tickers) > 0:
        ticker_data = yf.download(
            tickers,
            start_date,
            end_date
        )["Close"]

st.plotly_chart(
    historical_stock_cumulative_return_chart(selected_equities=tickers,
                                             start_date=start_date,
                                             end_date=end_date),
    use_container_width=True
)

returns = ticker_data.pct_change().dropna()
expected_returns = returns.mean() * 252
cov_matrix = returns.cov() * 252

# Optimization
num_assets = len(expected_returns)
init_guess = np.array(num_assets * [1. / num_assets])
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
bounds = tuple((0, 0.5) for asset in range(num_assets))

opt_result = minimize(negative_sharpe_ratio, init_guess,
                      args=(expected_returns.values, cov_matrix.values, risk_free_rate),
                      method='SLSQP', bounds=bounds, constraints=constraints)
optimal_weights = opt_result.x

st.subheader("Optimal Portfolio Weights")
for ticker, weight in zip(tickers, optimal_weights):
    st.write(f"{ticker}: {weight:.2%}")

target_returns = np.linspace(expected_returns.min(), expected_returns.max(), 50)
efficient_std = []

for target in target_returns:
    constraints_extended = (
        constraints,
        {'type': 'eq', 'fun': lambda w: np.dot(w, expected_returns.values) - target}
    )
    result = minimize(minimize_variance, init_guess,
                      args=(cov_matrix.values,),
                      method='SLSQP', bounds=bounds, constraints=constraints_extended)
    _, port_std = portfolio_performance(result.x, expected_returns.values, cov_matrix.values)
    efficient_std.append(port_std)

my_return, my_risk = portfolio_performance(optimal_weights, expected_returns.values, cov_matrix.values)

fig, ax = plt.subplots()
ax.plot(efficient_std, target_returns, 'b--', label='Efficient Frontier')
ax.scatter(my_risk, my_return, color='green', marker='o', s=100, label='Your Portfolio')
plt.scatter(0, risk_free_rate, color='red', s=100, marker='o', label='Riskfree Portolio')
ax.set_xlabel("Portfolio Risk (Std Dev)")
ax.set_ylabel("Portfolio Return")
ax.grid()
ax.legend()
st.pyplot(fig)