import pandas as pd
import statistics
import invest.metrics.return_ as return_metrics
import math

def process_ratios(data,benchmark_data,prices_current_dict,prices_initial_dict,share_betas_dict,start_year,end_year,index):
    annual_returns =[]

        for year in range(start_year,end_year):
            annual_return = return_metrics.annual_return(self.investment_initial_prices_dict[str(year)],self.investment_current_prices_dict[str(year)])
            annual_returns.append(annual_return)
    n= end_year-start_year
    compound_return = return_metrics.compound_return(self.investment_initial_prices_dict[str(start_year)],self.investment_current_prices_dict[str(end_year-1)],n)
    average_annual_return = return.metrics.average_annual_return(self.investment_initial_prices_dict[str(start_year)],self.investment_current_prices_dict[str(end_year-1)],n)
    process_risk_adjusted_return_ratios(data,benchmark_data,prices_current_dict,prices_initial_dict,share_betas_dict,2017,start_year,end_year,compound_return,average_annual_return,annual_returns,index)


def process_risk_adjusted_return_ratios(data,benchmark_data,prices_current_dict,prices_initial_dict,share_betas_dict,year,start_year,end_year,compound_return,average_annual_return,annual_returns,index):

    portfolio_return = compound_return
    beta_portfolio = statistics.mean(share_betas_dict[str(year)])
    mask_year = (df['Date'] >= str(year) + '-' + '12-01') & (
            df['Date'] <= str(year) + '12-31'))
    data_year = df[mask_year]
    risk_free_rate = data_year.iloc[-1]['RiskFreeRateOfReturn']
    treynor_ratio = return_metrics.treynor_ratio(portfolio_return,risk_free_rate,beta_portfolio) #worked out for 2017

    #sharpe ratio -use compound, need portfolio excess returns 6.43
    mask_index = data_benchmark['benchmark'] == index
    benchmark_data = data_benchmark.loc[mask_index]
    average_annual_return_benchmark_arr = benchmark_data['AAR'].unique()
    average_annual_excess_return = average_annual_return_benchmark_arr
    excess_return_list = []
    annual_return_i=0
    for year in range (start_year,end_year):
        mask_year = benchmark_data['year'] ==str(year)
        benchmark_data_year = data_benchmark.loc[mask_year]
        benchmark_annual_return =benchmark_data_year['AR']
        excess_return_list.append(annual_returns[annual_return_i]-benchmark_annual_return)
        annual_return_i+=1
    sum=0
    for excess_return in excess_return_list:
        sum+=(excess_return-average_annual_return_benchmark_arr)**2
     standard_deviation_excess_return = math.sqrt(sum)
    sharpe_ratio = return_metrics.sharpe_ratio(portfolio_return,risk_free_rate,standard_deviation_excess_return)

        
        









































# get investment portfolio from app main
# need year to be passed in too,
#
# loop through data set and get the closing price for each company, store in list, work out annaul return etc etc
#
# get risk free rate
# get beta of each stock
# work out treynor and sharpe89sw4r
