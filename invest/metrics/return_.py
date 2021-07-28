import numpy as np


def annual_return(pv, pv_, axis=None):
    return np.mean(np.abs(pv_ / pv), axis).astype(np.float64) - 1


def compound_return(pv, pv_, n, axis=None):
    return (np.mean(np.abs(pv_ / pv), axis) ** (1 / n)).astype(np.float64) - 1


def average_annual_return(pv, pv_, n, axis=None):
    return (np.mean(np.abs(pv_ / pv), axis) / n).astype(np.float64)


def treynor_ratio(portfolio_return, risk_free_rate, beta):
    return (portfolio_return - risk_free_rate) / beta


def sharpe_ratio(portfolio_return, risk_free_rate, sigma):
    return (portfolio_return - risk_free_rate) / sigma
