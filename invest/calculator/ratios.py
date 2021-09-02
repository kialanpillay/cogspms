# Historic Earnings Growth Rate - 1
import numpy as np

np.seterr(all="ignore")


def historic_earnings_growth_rate(eps_list, n):
    """
    Returns the Historic Earnings Growth Rate

    Parameters
    ----------
    eps_list : list
        Earnings per share for consecutive years
    n : int
        Number of years

    Returns
    -------
    float
    """
    growth_rates = []
    for year in range(0, n - 1):
        growth_rate = eps_list[year + 1] / eps_list[year]
        growth_rates.append(growth_rate)
    return np.mean(growth_rates)


# Historic Earnings Compound Annual Growth Rate
def historic_earnings_cagr(eps_n, eps_prev_x, x):
    """
    Returns the Historic Earnings Compound Growth Rate

    Parameters
    ----------
    eps_n : list
        Earnings per share for year N (current year)
    x : int
        Number of years into the past
    eps_prev_x: Earnings per share for year N-x

    Returns
    -------
    float
    """
    if np.isnan(((eps_n / eps_prev_x) ** (1 / x))):
        return 0
    return ((eps_n / eps_prev_x) ** (1 / x)) - 1


# Historic Price to Earnings
def historic_price_to_earnings_share(price_list, eps_list):
    """
    Returns the Historic Price to Earnings

    Parameters
    ----------
    price_list : list
        Share prices over past years
    eps_list : list
        Earnings per share over past years

    Returns
    -------
    float
    """
    return np.mean(price_list) / np.mean(eps_list)


# Forward Earnings - 4
def forward_earnings(eps, historic_earnings_growth_rate_):
    """
    Returns the Historic Price to Earnings

    Parameters
    ----------
    eps : float
        Earnings per share of current year
    historic_earnings_growth_rate_ : float
        Historic Earning Growth Rate

    Returns
    -------
    float
    """

    return eps * historic_earnings_growth_rate_


# Forward Earnings Compound Annual Growth Rate - 5
def forward_earnings_cagr(forward_earnings_n, forward_earnings_prev_x, x):
    """
    Returns the Forward Earnings Compound Annual Growth Rate

    Parameters
    ----------
    forward_earnings_n : float
            Forward earnings for the current year
    forward_earnings_prev_x : float
        Forward Earnings for x years ago
    x: int
            Years into the past

    Returns
    -------
    """
    if np.isnan(((forward_earnings_n / forward_earnings_prev_x) ** (1 / x))):
        return 0
    return ((forward_earnings_n / forward_earnings_prev_x) ** (1 / x)) - 1


# Forward Price to Earnings - Rule 6 - Needs Rule 4
def forward_price_to_earnings(share_price, forward_earnings_):
    """
    Returns the Forward Price to Earnings

    Parameters
    ----------
    share_price : float
        Current share price
    forward_earnings_ : float
        Forward Earnings for current year

    Returns
    -------
    float
    """
    return share_price / forward_earnings_


# Price to Earnings Relative Sector - 7, 8
def pe_relative_sector(historic_price_to_earnings_share_, pe_sector_list):
    """
    Returns the Price to Earnings relative to the sector

    Parameters
    ----------
    historic_price_to_earnings_share_ : float
        Historic Price to Earnings of the share
    pe_sector_list : list
         Price to Earnings for the sector for past years

    Returns
    -------
    float
    """
    return historic_price_to_earnings_share_ / np.mean(pe_sector_list)


# Price to Earnings Relative Market - 7, 9
def pe_relative_market(historic_price_to_earnings_share_, pe_market):
    """
    Returns the Price to Earnings relative to the market

    Parameters
    ----------
    historic_price_to_earnings_share_ : float
        Historic Price to Earnings of the share
    pe_market : list
        Price to Earnings for the market for past years

    Returns
    -------
    float
    """
    return historic_price_to_earnings_share_ / np.mean(pe_market)


# Cost of Equity
def cost_of_equity(market_return_rate, risk_free_return_rate, share_beta):
    """
    Returns the Cost of Equity

    Parameters
    ----------
    market_return_rate : float
         Market rate of return for the current year
    risk_free_return_rate : float
        Risk free rate of return for the current year
    share_beta: float
        Beta of share on last day of the year
    Returns
    -------
    float
    """

    equity_risk_premium = market_return_rate - risk_free_return_rate
    return risk_free_return_rate + share_beta * equity_risk_premium


# Relative Debt to Equity
def relative_debt_to_equity(debt_equity, debt_equity_industry):
    """
    Returns the Relative Debt to Equity

    Parameters
    ----------
    debt_equity : float
         Debt Equity of the share
    debt_equity_industry : float
        Debt Equity of the industry

    Returns
    -------
    float
    """
    return debt_equity / debt_equity_industry


def current_pe_market(current_share_pe, current_market_pe):
    """
    Returns the Price to Earnings relative to the market for the current year

    Parameters
    ----------
    current_share_pe : float
            PE of the current share
    current_market_pe : float
        PE of the industry

    Returns
    -------
    float
    """
    current_pe = current_share_pe / current_market_pe
    return current_pe


def current_pe_sector(current_share_pe, current_sector_pe):
    """
    Returns the Price to Earnings relative to the market for the current year

    Parameters
    ----------
    current_share_pe : float
        PE of the current share
    current_sector_pe : float
        PE of the sector

    Returns
    -------
    float
    """
    return current_share_pe / current_sector_pe
