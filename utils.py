import streamlit as st
import pandas as pd
import yfinance as yf


@st.cache_data  # Caches data to prevent re-running on every reload
def scrape_spy_tickers() -> list[str]:
    """Scrapes S&P 500 tickers from Wikipedia and caches the result."""
    tickers = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]["Symbol"].tolist()
    return tickers


@st.cache_data
def get_cur_risk_free_rate() -> float:
    """Gets the current yield on 10-yr T-Note as proxy for risk-free rate"""
    ten_year_treasury = yf.Ticker("^TNX")
    yield_rate = ten_year_treasury.history(period="1d")["Close"].iloc[-1]
    return yield_rate


def compute_default_values() -> dict:
    """Compute the default input values dynamically."""
    return {
        "risk_free_rate_input": get_cur_risk_free_rate(),
        "end_date": pd.Timestamp.today(),
        "start_date": pd.Timestamp.today() - pd.Timedelta(weeks=52),
    }


def reset_inputs_to_default() -> None:
    """Reset all sidebar input values to their default state."""
    for key, value in st.session_state.default_values.items():
        st.session_state[key] = value

    st.session_state.reset_flag = True
    st.rerun()
