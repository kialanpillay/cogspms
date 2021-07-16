# Historic Earnings Growth Rate - calc rule 1,
# n = how many years eps was given over
def historic_earnings_growth_rate(eps_list, n): # needs list as 2012,2013,2014 therefore ascending order
    num_years = n - 1
    year = 0
    growth_rates = []
    for num_years in eps_list:
        growth_rate = eps_list[year + 1] / eps_list[year]
        growth_rates.append(growth_rate)
        year += 1
    historic_earning_growth_rate = sum(growth_rates) / len(growth_rates)
    return historic_earning_growth_rate


# Historic Earnings Compound Annual Growth Rate
def historic_earnings_cagr(eps_n, eps_prev_x, x): # use 3 years ago for X
    cagr = ((eps_n / eps_prev_x) ** 1 / x) - 1
    return cagr


# Historic Price to Earnings
def historic_price_to_earnings_share(price_list, eps_list):
    price = sum(price_list)\len(price_list)
    eps = sum(eps_list)\len(eps_list)
    return price / eps


# Forward Earnings - calc rule 4 - needs function 1 answer as input
def forward_earnings(eps, historic_earnings_growth_rate):
    return eps * historic_earnings_growth_rate


# Forward Earnings Compound Annual Growth Rate - calc rule 5 - INVEST uses 3 years, therefore X should be 3
def forward_earnings_cagr(forward_earnings_n, forward_earnings_prev_x, x):
    return ((forward_earnings_n / forward_earnings_prev_x) ** 1 / x) - 1


# Forward Price to Earnings - calc rule 6 - needs rule 4 as input
def forward_price_to_earnings(share_price, forward_earnings):
    return share_price / forward_earnings


# Price to Earnings Relative Sector - calc rule 7, calc 8
def pe_relative_sector(historic_price_to_earnings_share, pe_sector):
    historic_pe_sector = sum(pe_sector) / len(pe_sector)
    return historic_price_to_earnings_share / historic_pe_sector


# Price to Earnings Relative Market - calc rule 7, calc 9
def pe_relative_market(historic_price_to_earnings_share, pe_market):
    historic_pe_market = sum(pe_market) / len(pe_market)
    return historic_price_to_earnings_share / historic_pe_market


# Return on Equity -calc rule 8, calc 10 - dont need
def return_on_equity(net_income, total_shareholder_equity):
    return net_income / total_shareholder_equity


# Cost of Equity
def cost_of_equity(market_return_rate, risk_free_return_rate, share_beta):
    equity_risk_premium = market_return_rate - risk_free_return_rate
    cost_of_equity = risk_free_return_rate + (share_beta * equity_risk_premium)
    return cost_of_equity


# Relative Debt to Equity - changed from paper formula
def relative_debt_to_equity(d_e, d_e_industry, ):
    relative_d_e = d_e / d_e_industry
    return relative_d_e


def current_pe_market(current_share_pe,current_market_pe):
    return current_share_pe/current_market_pe

def current_pe_sector(current_share_pe,current_sector_pe):
    return current_share_pe/current_sector_pe