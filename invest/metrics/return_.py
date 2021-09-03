import numpy as np


def annual_return(pv, pv_, axis=None):
    """
    Returns annual return for a portfolio

    Parameters
    ----------
    pv : Union[int, numpy.ndarray]
       Portfolio value for previous year
    pv_ : Union[int, numpy.ndarray]
       Portfolio value for current year
    axis: int / None
        Array dimension
    Returns
    -------
    float
    """
    return np.abs(np.mean(pv_, axis) / np.mean(pv, axis)).astype(np.float64) - 1


def compound_return(pv, pv_, n, axis=None):
    """
    Returns Compound Return for a portfolio

    Parameters
    ----------
    pv : Union[int, numpy.ndarray]
          Portfolio value for previous year
    pv_ : Union[int, numpy.ndarray]
          Portfolio value for current year
    n: int
        Number of years return is compounded over
    axis: int / None
        Array dimension
    Returns
    -------
    float
    """
    return (np.abs(np.mean(pv_, axis) / np.mean(pv, axis)) ** (1 / n)).astype(np.float64) - 1


def average_annual_return(returns, axis=None):
    """
    Returns average annual return for a portfolio

    Parameters
    ----------
    returns : Union[list, numpy.ndarray]
       List of annual returns
    axis: int / None
        Array dimension
    Returns
    -------
    float
    """
    return np.mean(returns, axis).astype(np.float64)


def treynor_ratio(portfolio_return, risk_free_rate, beta):
    """
    Returns the Treynor ratio for a portfolio

    Parameters
    ----------
    portfolio_return : float
       Portfolio Return in percentage
    risk_free_rate: Union[float, numpy.ndarray]
        Risk free rate of return in percentage
    beta: Union[float, numpy.ndarray]
        Beta of portfolio
    Returns
    -------
    float
    """
    return ((portfolio_return / 100) - (risk_free_rate / 100)) / beta


def sharpe_ratio(portfolio_return, risk_free_rate, sigma):
    """
    Returns the Sharpe Ratio for a portfolio

    Parameters
    ----------
    portfolio_return : float
       Portfolio Return in percentage
    risk_free_rate: Union[float, numpy.ndarray]
        Risk free rate of return in percentage
    sigma: float
        standard deviation of portfolio's excess return
    Returns
    -------
    float
    """
    return ((portfolio_return / 100) - (risk_free_rate / 100)) / sigma
