import pandas as pd
import invest.calculator.ratios as ratios


# import invest.calculator.threshold as threshold


class Store:
    def __init__(self, main_data, all_companies,
                 consumer_companies,
                 general_companies, margin_of_safety, beta, years):
        self.main_data = main_data
        self.all_companies = all_companies
        self.consumer_companies = consumer_companies
        self.general_companies = general_companies
        self.margin_of_safety = margin_of_safety
        self.beta = beta
        self.years = years
        self.process()

    # newDf
    column_names = ["negative_earnings", "negative_shareholders_equity", "beta_classify", "acceptable_stock",
                    "current_PE_relative_share_market_to_historical", "current_PE_relative_share_sector_to_historical",
                    "forward_PE_current_to_historical", "roe_vs_coe",
                    "growth_cagr_vs_inflation", "relative_debt_to_equity"]
    share_data_frame = pd.DataFrame(columns=column_names)

    def process(self):

        # calculate ratios
        for company in self.all_companies:
            eps_year_list = []
            eps_list_3_years = []
            price_list_3_years = []
            pe_sector_list=[]
            pe_market_list=[]

            # preprocessing to gets lists etc
            year = 2012
            years = self.years  # year after data value being used , this case is using 2016 latest as final
            for i in range(year, years):
                maskEPS = (self.main_data['Date'] >= str(i) + '-' + '01-01') & (
                            self.main_data['Date'] <= str(i) + '12-31') & (self.main_data['Name'] == company)
                company_df_by_year = self.main_data.loc[maskEPS]
                # last_row_index = company_df_by_year.last_valid_index()
                eps = company_df_by_year.iloc[-1]['EPS']  # gets last row for frame, and EPS column
                eps_year_list.append(eps)  # add eps value to list- by year
                # print("i:"+str(i),"year:"+str(year),"years:"+str(years))
                mask_current_price = (self.main_data['Date'] >= '2016-01-01') & (
                            self.main_data['Date'] < '2017-01-01')& (self.main_data['Name'] == company)
                current_year_data = self.main_data.loc[mask_current_price]
                current_price = current_year_data.iloc[-1]['Price']

                mask_pe_sector_market= (self.main_data['Date'] >= '2014-01-01') & (self.main_data['Date'] < '2017-01-01') & (self.main_data['Name'] == company)
                pe_sector_3_years = self.main_data.loc[mask_pe_sector_market]
                pe_market_3_years = self.main_data.loc[mask_pe_sector_market]
                pe_sector_list = (pe_sector_3_years['PESector'].tolist()) #need to convert to int
                print(pe_sector_list)
                pe_market_list = (pe_market_3_years['PEMarket'].tolist()) #need to convert to int






            # historic_earnings_growth_rate
            historic_earnings_growth_rate = ratios.historic_earnings_growth_rate(eps_year_list, 5)
            print("Historic Earnings growth rate: ", historic_earnings_growth_rate)

            # historic_earnings_cagr
            historic_earnings_cagr = ratios.historic_earnings_cagr(eps_year_list[len(eps_year_list) - 1],
                                                                   eps_year_list[1], 3)  # pass it the last position
            print("HistoricEarnings Compound annual GrowthRate: ", historic_earnings_cagr)

            # historic_price_to_earnings_share
            maskPE = (self.main_data['Date'] >= '2014-01-01') & (self.main_data['Date'] < '2017-01-01')& (self.main_data['Name'] == company)
            company_df_3_years = self.main_data.loc[maskPE]
            price_list_3_years = (company_df_3_years['Price'].tolist())
            eps_list_3_years = (company_df_3_years['EPS'].tolist())
            historic_price_to_earnings_share = ratios.historic_price_to_earnings_share(price_list_3_years,
                                                                                       eps_list_3_years)
            print("HistoricPriceToEarnings:", historic_price_to_earnings_share)

            # forward_earnings_current_year
            forward_earnings_current_year = ratios.forward_earnings(eps_year_list[len(eps_year_list) - 1],
                                                           historic_earnings_growth_rate)  # for the current
            print("ForwardEarnings: ",forward_earnings_current_year)
            # forward earnings for 3 years ago
            historic_earnings_growth_rate_past = ratios.historic_earnings_growth_rate(eps_year_list,3) # intermediate, list from past can be 2013 since year is 3
            forward_earnings_past = ratios.forward_earnings(eps_year_list[1],
                                                            historic_earnings_growth_rate_past)  # intermediate
            forward_earnings_cagr = ratios.forward_earnings_cagr(forward_earnings_current_year, forward_earnings_past, 3)
            print("forward_earnings_cagr:", forward_earnings_cagr)


            forward_price_to_earnings = ratios.forward_price_to_earnings(current_price, forward_earnings_current_year)
            print("forward_price_to_earnings",forward_price_to_earnings)

            # #Price to earning relative
            pe_relative_sector = ratios.pe_relative_sector(historic_price_to_earnings_share,
                                                           pe_sector_list)  # consumer related data for sector for year. This value is historical
            print(" pe_relative_sector",pe_relative_sector)
            pe_relative_market = ratios.pe_relative_market(historic_price_to_earnings_share, pe_market_list)
            print(" pe_relative_market", pe_relative_market)



            # # return_on_equity = # only get ROE from main data for 2017
            # cost_of_equity = ratios.cost_of_equity(market_rate_of_return, risk_free_rate_of_return, beta)
            # relative_debt_equity = ratios.relative_debt_to_equity(d_e, d_e_industry)  # debt equity is from data directly
            #
            # # threshold
            # negative_earnings = threshold.negative_earnings(forward_earnings_current_year)
            # negative_shareholders_equity = threshold.negative_shareholders_equity(shareholders_equity)  # need value
            # beta_classify = threshold.beta_classify(share_beta, beta)
            # acceptable_stock = threshold.acceptable_stock(negative_earnings, negative_shareholders_equity, beta_classify)
            #
            # if acceptable_stock == True:  # only if stock is investable do you continue the process
            #
            #     pe_current_share_market = ratios.current_pe_market(current_share_pe,
            #                                                        current_market_pe)  # PE value for this year
            #     pe_current_share_sector = ratios.current_pe_sector(current_share_pe,
            #                                                        current_sector_pe)  # PE value for this year
            #     pe_relative_market = threshold.current_PE_relative_share_market(margin_of_safety, pe_current_share_market,
            #                                                                     pe_relative_market)  # current share PE must be passed in, current market PE must be passed in
            #
            #     pe_relative_sector = threshold.current_PE_relative_share_sector(margin_of_safety, pe_current_share_sector,
            #                                                                     pe_relative_sector)
            #
            #     forward_pe = threshold.forward_PE(margin_of_safety, forward_price_to_earnings,
            #                                       historic_price_to_earnings_share)
            #
            #     roe_coe = threshold.roe_coe(margin_of_safety, roe, coe)  # roe from data , need to find coe
            #     cagr_inflation = threshold.cagr_inflation(margin_of_safety, historic_earnings_cagr,
            #                                               inflation)  # or use forecast consensus if available
            #     relative_debt_to_equity = threshold.relative_debt_to_equity(margin_of_safety, relative_debt_equity)
            #
            #     # add row to dataframe
            #     company_row = {negative_earnings, negative_shareholders_equity, beta_classify, acceptable_stock,
            #                    pe_relative_market,
            #                    pe_relative_sector, forward_pe, roe_coe, cagr_inflation, relative_debt_to_equity}
            #     shares_data_frame = shares_data_frame.append(company_row, ignore_index=True)
            # else:
            #     company_row = {negative_earnings, negative_shareholders_equity, beta_classify,
            #                    acceptable_stock}  # only these values are calculated
            #     shares_data_frame = shares_data_frame.append(company_row, ignore_index=True)
