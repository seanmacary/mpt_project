import numpy as np

def portfolio_performance(weights, returns, cov_matrix):
    port_return = np.dot(weights, returns)
    port_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return port_return, port_std


def negative_sharpe_ratio(weights, returns, cov_matrix, risk_free_rate):
    port_return, port_std = portfolio_performance(weights, returns, cov_matrix)
    sharpe_ratio = (port_return - risk_free_rate) / port_std
    return -sharpe_ratio


def portfolio_variance(weights, cov_matrix):
    return np.dot(weights.T, np.dot(cov_matrix, weights))


def minimize_variance(weights, cov_matrix):
    return portfolio_variance(weights, cov_matrix)
