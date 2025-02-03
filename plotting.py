import pandas as pd
import yfinance as yf
import plotly.express as px
import streamlit as st


def historical_stock_cumulative_return_chart(selected_equities, start_date, end_date):
    """
    Fetches historical stock data for the given equities within a specified date range
    and generates an interactive Plotly chart of cumulative returns.
    """
    if not selected_equities:
        st.warning("Please provide at least one stock ticker.")
        return px.line(title="Historical Stock Cumulative Returns")

    all_data = []

    for equity in selected_equities:
        hist_stock_data = yf.Ticker(equity).history(start=start_date, end=end_date)

        if hist_stock_data.empty:
            st.warning(f"No data available for {equity}. Please try another stock.")
            continue

        hist_stock_data["Equity"] = equity  # Add column to distinguish stocks
        hist_stock_data["Returns"] = hist_stock_data["Close"].pct_change()  # Calculate daily returns
        hist_stock_data["Cumulative Returns"] = (1 + hist_stock_data[
            "Returns"]).cumprod() - 1  # Compute cumulative return
        hist_stock_data = hist_stock_data.reset_index()
        all_data.append(hist_stock_data)

    if not all_data:
        st.error("No valid stock data available to plot.")
        return px.line(title="Historical Stock Cumulative Returns")

    combined_data = pd.concat(all_data, ignore_index=True)

    fig = px.line(
        combined_data,
        x="Date",
        y="Cumulative Returns",
        color="Equity",  # Differentiate stocks by color
        title="Historical Stock Cumulative Returns",
        labels={"Cumulative Returns": "Cumulative Return", "Date": "Date"},
    )

    fig.update_layout(
        width=1200,
        height=500,
        xaxis_title="Date",
        yaxis_title="Cumulative Return",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        template="plotly_white",
    )

    return fig

