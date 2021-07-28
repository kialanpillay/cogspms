import math

import numpy as np
import pandas as pd

import invest.metrics.return_ as return_metrics


def process_metrics(df, df_benchmark, prices_current_dict, prices_initial_dict, share_betas_dict, start_year,
                    end_year, index_code):
    annual_returns = []
    for year in range(start_year, end_year):
        annual_return = return_metrics.annual_return(np.array(prices_initial_dict[str(year)]),
                                                     np.array(prices_current_dict[str(year)]))
        annual_returns.append(annual_return)
    n = end_year - start_year
    compound_return = return_metrics.compound_return(np.array(prices_initial_dict[str(start_year)]),
                                                     np.array(prices_current_dict[str(end_year - 1)]), n)
    average_annual_return = return_metrics.average_annual_return(np.array(prices_initial_dict[str(start_year)]),
                                                                 np.array(prices_current_dict[str(end_year - 1)]), n)

    print('Index {} | CR {:5.3f}% | AAR {:5.3f}%'.format(index_code, compound_return * 100, average_annual_return * 100))
    process_risk_adjusted_return_metrics(df, df_benchmark, share_betas_dict, 2017, compound_return,
                                         average_annual_return, annual_returns, index_code)


def process_risk_adjusted_return_metrics(df, df_benchmark, share_betas_dict,
                                         year, compound_return, average_annual_return,
                                         annual_returns, index_code):
    portfolio_return = compound_return * 100
    beta_portfolio = np.mean(share_betas_dict[str(year)])
    mask = (df['Date'] >= str(year) + '-01-01') & (df['Date'] <= str(year) + '-12-31')
    df_year = df[mask]
    risk_free_rate = df_year.iloc[-1]['RiskFreeRateOfReturn']
    treynor_ratio = return_metrics.treynor_ratio(portfolio_return, risk_free_rate, beta_portfolio)
    # 2017

    mask = df_benchmark['IndexCode'] == index_code
    benchmark_data = df_benchmark.loc[mask]
    annual_returns_benchmark = benchmark_data['AR'].values
    average_annual_return_benchmark = pd.unique(benchmark_data['AAR'])[0]
    average_annual_excess_return = average_annual_return - average_annual_return_benchmark
    excess_returns = []
    for i, annual_return in enumerate(annual_returns):
        excess_returns.append(annual_return - annual_returns_benchmark[i])

    v = 0
    for e in excess_returns:
        v += (e - average_annual_excess_return) ** 2
    standard_deviation_excess_return = math.sqrt(v)
    sharpe_ratio = return_metrics.sharpe_ratio(portfolio_return, risk_free_rate, standard_deviation_excess_return)
    print('Index {} | Treynor Ratio {:5.5f} | Sharpe Ratio: {:5.5f}'.format(index_code, treynor_ratio, sharpe_ratio))
