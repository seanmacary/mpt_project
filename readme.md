# Portfolio Optimization & Sharpe Ratio Analysis

A beginner quantitative finance project that uses historical stock data to build an optimal portfolio. The project leverages Modern Portfolio Theory (MPT) concepts, calculating expected returns, the covariance matrix, and the Sharpe ratio to construct the efficient frontier. An interactive Streamlit web app is provided to showcase the analysis and allow users to adjust parameters dynamically.

## Overview

This project demonstrates how to:
- **Fetch historical stock data** using the `yfinance` library.
- **Calculate portfolio metrics** such as expected returns, risk (variance/standard deviation), and the Sharpe ratio.
- **Optimize portfolio weights** to maximize the Sharpe ratio or minimize variance under constraints.
- **Construct the efficient frontier** to visualize the trade-off between risk and return.
- **Implement a Streamlit web app** for an interactive, user-friendly interface.

## Features

- **Dynamic Data Collection:** Automatically fetches the latest stock data based on user input.
- **Portfolio Metrics Computation:** Calculates expected returns and the covariance matrix to derive portfolio risk and performance.
- **Optimization Techniques:** Uses SciPy’s optimization routines (SLSQP) with constraints (e.g., full investment, no short-selling) to determine the optimal portfolio.
- **Efficient Frontier Visualization:** Plots the efficient frontier alongside the user's chosen portfolio, highlighting optimal risk-return trade-offs.
- **Liquidity & Fundamental Filters (Optional):** Potential to filter stocks based on liquidity (e.g., average trading volume, market capitalization) and fundamental metrics (e.g., P/E ratio).

