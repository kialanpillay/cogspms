import math

import numpy as np

import invest.metrics.return_ as return_metrics


def process_metrics(df, df_benchmark, prices_current_dict, prices_initial_dict, share_betas_dict, start_year,
                    end_year, index_code):
    annual_returns = []
    total_return = 0
    for year in range(start_year, end_year):
        return_ = sum(prices_current_dict[str(year)]) - sum(prices_initial_dict[str(year)])
        total_return += return_
        if np.abs(return_) > 0:
            annual_return = return_metrics.annual_return(np.array(prices_initial_dict[str(year)]),
                                                         np.array(prices_current_dict[str(year)]))
        else:
            annual_return = 0
        annual_returns.append(annual_return)

    pv = sum(prices_initial_dict[str(start_year)])
    y = start_year
    while pv == 0 or y == end_year:
        y += 1
        pv = sum(prices_initial_dict[str(y)])
    pv_ = pv + total_return
    n = end_year - start_year
    compound_return = return_metrics.compound_return(pv, pv_, n)
    average_annual_return = return_metrics.average_annual_return(annual_returns)
    print('Index {} | CR {:5.3f}% | AAR {:5.3f}%'.format(index_code, compound_return * 100,
                                                         average_annual_return * 100))
    process_risk_adjusted_return_metrics(df, df_benchmark, share_betas_dict, 2015, 2018, compound_return,
                                         average_annual_return, annual_returns, index_code)


def process_risk_adjusted_return_metrics(df, df_benchmark, share_betas_dict,
                                         start_year, end_year, compound_return, average_annual_return,
                                         annual_returns, index_code):
    portfolio_return = compound_return * 100
    betas = []
    for year in range(start_year, end_year):
        betas += share_betas_dict[str(year)]
    beta_portfolio = np.mean(betas)
    mask = (df['Date'] >= str(end_year - 1) + '-01-01') & (df['Date'] <= str(end_year - 1) + '-12-31')
    df_year = df[mask]
    risk_free_rate = df_year.iloc[-1]['RiskFreeRateOfReturn']
    treynor_ratio = return_metrics.treynor_ratio(portfolio_return, risk_free_rate, beta_portfolio)

    mask = df_benchmark['IndexCode'] == index_code
    benchmark_data = df_benchmark.loc[mask]
    annual_returns_benchmark = benchmark_data['AR'].values

    average_annual_return_benchmark = np.mean(annual_returns_benchmark) / 100
    delta = average_annual_return - average_annual_return_benchmark
    excess_returns = []
    for i, annual_return in enumerate(annual_returns):
        excess_returns.append(annual_return - annual_returns_benchmark[i] / 100)

    v = 0
    for e in excess_returns:
        v += (e - delta) ** 2
    standard_deviation_excess_return = math.sqrt(v)
    sharpe_ratio = return_metrics.sharpe_ratio(portfolio_return, risk_free_rate, standard_deviation_excess_return)
    print('Index {} | Treynor Ratio {:5.5f} | Sharpe Ratio: {:5.5f}'.format(index_code, treynor_ratio, sharpe_ratio))
