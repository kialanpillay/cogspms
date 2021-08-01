# Historic Earnings Growth Rate - 1
import numpy as np


def historic_earnings_growth_rate(eps_list, n):
    growth_rates = []
    for year in range(0, n - 1):
        growth_rate = eps_list[year + 1] / eps_list[year]
        growth_rates.append(growth_rate)
    return np.mean(growth_rates)


# Historic Earnings Compound Annual Growth Rate
def historic_earnings_cagr(eps_n, eps_prev_x, x):
    if np.isnan(((eps_n / eps_prev_x) ** (1 / x))):
        return 0
    return ((eps_n / eps_prev_x) ** (1 / x)) - 1


# Historic Price to Earnings
def historic_price_to_earnings_share(price_list, eps_list):
    return np.mean(price_list) / np.mean(eps_list)


# Forward Earnings - 4
def forward_earnings(eps, historic_earnings_growth_rate_):
    return eps * historic_earnings_growth_rate_


# Forward Earnings Compound Annual Growth Rate - 5
def forward_earnings_cagr(forward_earnings_n, forward_earnings_prev_x, x):
    if np.isnan(((forward_earnings_n / forward_earnings_prev_x) ** (1 / x))):
        return 0
    return ((forward_earnings_n / forward_earnings_prev_x) ** (1 / x)) - 1


# Forward Price to Earnings - Rule 6 - Needs Rule 4
def forward_price_to_earnings(share_price, forward_earnings_):
    return share_price / forward_earnings_


# Price to Earnings Relative Sector - 7, 8
def pe_relative_sector(historic_price_to_earnings_share_, pe_sector_list):
    return historic_price_to_earnings_share_ / np.mean(pe_sector_list)


# Price to Earnings Relative Market - 7, 9
def pe_relative_market(historic_price_to_earnings_share_, pe_market):
    return historic_price_to_earnings_share_ / np.mean(pe_market)


# Return on Equity 8,10
def return_on_equity(net_income, total_shareholder_equity):
    return net_income / total_shareholder_equity


# Cost of Equity
def cost_of_equity(market_return_rate, risk_free_return_rate, share_beta):
    equity_risk_premium = market_return_rate - risk_free_return_rate
    return risk_free_return_rate + share_beta * equity_risk_premium


# Relative Debt to Equity
def relative_debt_to_equity(debt_equity, debt_equity_industry):
    return debt_equity / debt_equity_industry


def current_pe_market(current_share_pe, current_market_pe):
    current_pe = current_share_pe / current_market_pe
    return current_pe


def current_pe_sector(current_share_pe, current_sector_pe):
    return current_share_pe / current_sector_pe
