# Historic Earnings Growth Rate - calc rule 1,
# n = how many years eps was given over
def historic_earnings_growth_rate(eps_list,n):
    num_years = n-1
    year = 0
    growth_rates = []
    for num_years in eps_list:
        growth_rate = eps_list[year+1]/eps_list[year]
        growth_rates.append(growth_rate)
        year+=1
    historic_earning_growth_rate = sum(growth_rates) / len(growth_rates)

# Historic Earnings Compound Annual Growth Rate
def historic_earnings_cagr(eps_n, eps_prev_x, x):
    cagr = ((eps_n / eps_prev_x) ** 1 / x) - 1
    return cagr


# Historic Price to Earnings
def historic_price_to_earnings(price, eps):
    return price / eps


# Forward Earnings - calc rule 4 - needs function 1 answer as input
def forward_earnings(eps,historic_earnings_growth_rate):
    return eps*historic_earnings_growth_rate

# Forward Earnings Compound Annual Growth Rate - calc rule 5 - INVEST uses 3 years, therefore X should be 3
def forward_earnings_cagr(forward_earnings_n,forward_earnings_prev_x,x):
    return ((forward_earnings_n/forward_earnings_prev_x)**1/x)-1


# Forward Price to Earnings - calc rule 6 - needs rule 4 as input
def forward_price_to_earnings(share_price,forward_earnings):
    return share_price/forward_earnings



# Price to Earnings Relative Sector - calc rule 7, calc 8
def pe_relative_sector(historic_pe_share, historic_pe_sector):
    return historic_pe_share / historic_pe_sector


# Price to Earnings Relative Market - calc rule 7, calc 9
def pe_relative_market(historic_pe_share, historic_pe_market):
    return historic_pe_share / historic_pe_market


# Return on Equity -calc rule 8, calc 10
def return_on_equity(net_income, total_shareholder_equity):
    return net_income / total_shareholder_equity


# Cost of Equity
def cost_of_equity(market_return_rate, risk_free_return_rate, share_beta):
    equity_risk_premium = market_return_rate - risk_free_return_rate
    cost_of_equity = risk_free_return_rate + (share_beta * equity_risk_premium)
    return cost_of_equity


# Relative Debt to Equity
def relative_debt_to_equity(total_liability, total_shareholder_equity, d_e_industry, ):
    d_e = total_liability / total_shareholder_equity
    relative_d_e = d_e / d_e_industry
    return relative_d_e
