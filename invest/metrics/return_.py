import numpy as np


def annual_return(pv, pv_, axis=None):
    return np.abs(np.mean(pv_, axis) / np.mean(pv, axis)).astype(np.float64) - 1


def compound_return(pv, pv_, n, axis=None):
    return (np.abs(np.mean(pv_, axis) / np.mean(pv, axis)) ** (1 / n)).astype(np.float64) - 1


def average_annual_return(returns, axis=None):
    return np.mean(returns, axis).astype(np.float64)


def treynor_ratio(portfolio_return, risk_free_rate, beta):
    return ((portfolio_return / 100) - (risk_free_rate / 100)) / beta


def sharpe_ratio(portfolio_return, risk_free_rate, sigma):
    return ((portfolio_return / 100) - (risk_free_rate / 100)) / sigma
