import pandas as pd
import invest.calculator.ratios as ratios
import invest.calculator.threshold as threshold






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



    def process(self):
        # newDf
        global shares_data_frame
        column_names = ["negative_earnings", "negative_shareholders_equity", "beta_classify", "acceptable_stock",
                        "current_PE_relative_share_market_to_historical",
                        "current_PE_relative_share_sector_to_historical",
                        "forward_PE_current_to_historical", "roe_vs_coe",
                        "growth_cagr_vs_inflation", "relative_debt_to_equity"]
        share_data_frame = pd.DataFrame(columns=column_names)


        # calculate ratios
        for company in self.all_companies:
            eps_year_list = []
            eps_list_3_years = []
            price_list_3_years = []
            pe_sector_list = []
            pe_market_list = []

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
                        self.main_data['Date'] < '2017-01-01') & (self.main_data['Name'] == company)
                current_year_data = self.main_data.loc[mask_current_price]
                current_price = current_year_data.iloc[-1]['Price']

                mask_pe_sector_market = (self.main_data['Date'] >= '2014-01-01') & (
                            self.main_data['Date'] < '2017-01-01') & (self.main_data['Name'] == company)
                pe_sector_3_years = self.main_data.loc[mask_pe_sector_market]
                pe_market_3_years = self.main_data.loc[mask_pe_sector_market]
                pe_sector_list_string = pe_sector_3_years['PESector'].to_numpy()
                pe_market_list_string = pe_market_3_years['PEMarket'].to_numpy()
                for item in pe_sector_list_string:
                    pe_sector_list.append(float(item))

                for item in pe_market_list_string:
                    pe_market_list.append(float(item))

            # historic_earnings_growth_rate
            historic_earnings_growth_rate = ratios.historic_earnings_growth_rate(eps_year_list, 5)
            print("Historic Earnings growth rate (Calc1):", historic_earnings_growth_rate)

            # historic_earnings_cagr
            historic_earnings_cagr = ratios.historic_earnings_cagr(eps_year_list[len(eps_year_list) - 1],
                                                                   eps_year_list[1], 3)  # pass it the last position
            print("HistoricEarnings Compound annual GrowthRate (Calc2): ", historic_earnings_cagr)

            # historic_price_to_earnings_share
            maskPE = (self.main_data['Date'] >= '2014-01-01') & (self.main_data['Date'] < '2017-01-01') & (
                        self.main_data['Name'] == company)
            company_df_3_years = self.main_data.loc[maskPE]
            price_list_3_years = (company_df_3_years['Price'].to_numpy())
            eps_list_3_years = (company_df_3_years['EPS'].to_numpy())
            historic_price_to_earnings_share = ratios.historic_price_to_earnings_share(price_list_3_years,
                                                                                       eps_list_3_years)
            print("HistoricPriceToEarnings:(Calc3):", historic_price_to_earnings_share)

            # forward_earnings_current_year
            forward_earnings_current_year = ratios.forward_earnings(eps_year_list[len(eps_year_list) - 1],
                                                                    historic_earnings_growth_rate)  # for the current
            print("ForwardEarnings:(Calc4) ", forward_earnings_current_year)
            # forward earnings for 3 years ago
            historic_earnings_growth_rate_past = ratios.historic_earnings_growth_rate(eps_year_list,
                                                                                      3)  # intermediate, list from past can be 2013 since year is 3
            forward_earnings_past = ratios.forward_earnings(eps_year_list[1],
                                                            historic_earnings_growth_rate_past)  # intermediate
            forward_earnings_cagr = ratios.forward_earnings_cagr(forward_earnings_current_year, forward_earnings_past,
                                                                 3)
            print("forward_earnings_cagr (Calc5):", forward_earnings_cagr)

            forward_price_to_earnings = ratios.forward_price_to_earnings(current_price, forward_earnings_current_year)
            print("forward_price_to_earnings (Calc6):", forward_price_to_earnings)

            # Price to earning relative
            pe_relative_sector = ratios.pe_relative_sector(historic_price_to_earnings_share,
                                                           pe_sector_list)
            print(" pe_relative_sector (Calc7):", pe_relative_sector)
            pe_relative_market = ratios.pe_relative_market(historic_price_to_earnings_share, pe_market_list)
            print(" pe_relative_market (Calc7):", pe_relative_market)

            # ROE
            roe_current = current_year_data.iloc[-1]['ROE']
            print("ROE (Calc8):", roe_current)

            # cost of equity
            market_rate_of_return = current_year_data.iloc[-1]['MarketRateOfReturn']
            risk_free_rate_of_return = current_year_data.iloc[-1]['RiskFreeRateOfReturn']
            share_beta = current_year_data.iloc[-1]['Share Beta']
            cost_of_equity = ratios.cost_of_equity(float(market_rate_of_return), float(risk_free_rate_of_return),
                                                   float(share_beta))
            print("COE (Calc9):", cost_of_equity)

            # relative debt to equity
            d_e = current_year_data.iloc[-1]['Debt/Equity']
            d_e_industry = current_year_data.iloc[-1]['Debt Equity/Industry']
            relative_debt_equity = ratios.relative_debt_to_equity(float(d_e), float(
                d_e_industry))  # debt equity is from data directly
            print("Relative debt to equity (Calc10):", relative_debt_equity)

            # threshold
            # negative_earnings
            negative_earnings = threshold.negative_earnings(forward_earnings_current_year)
            print("negative_earnings (Rule1):", negative_earnings)

            # negative_shareholders_equity
            shareholders_equity = current_year_data.iloc[-1]['Shareholders Equity']
            negative_shareholders_equity = threshold.negative_shareholders_equity(float(shareholders_equity))
            print("negative_shareholders_equity (Rule2):", negative_shareholders_equity)

            # beta
            beta_classify = threshold.beta_classify(float(share_beta), self.beta)
            print("Specified Beta (Rule3):", beta_classify)

            # acceptable stock
            # acceptable_stock = threshold.acceptable_stock(negative_earnings, negative_shareholders_equity, beta_classify)
            acceptable_stock = True
            print("acceptable stock (Rule4):", acceptable_stock)

            if acceptable_stock == True:  # only if stock is investable do you continue the process
                current_share_pe = current_year_data.iloc[-1]['PE']
                current_market_pe = current_year_data.iloc[-1]['PEMarket']

                current_sector_pe = current_year_data.iloc[-1]['PESector']

                pe_current_share_market = ratios.current_pe_market(float(current_share_pe),
                                                                   float(current_market_pe))  # PE value for this year

                pe_current_share_sector = ratios.current_pe_sector(float(current_share_pe),
                                                                   float(current_sector_pe))  # PE value for this year
                pe_relative_market = threshold.current_PE_relative_share_market(self.margin_of_safety,
                                                                                pe_current_share_market,
                                                                                pe_relative_market)  # current share PE must be passed in, current market PE must be passed in
                print("pe_relative_market (Rule4):", pe_relative_market)
                pe_relative_sector = threshold.current_PE_relative_share_sector(self.margin_of_safety,
                                                                                pe_current_share_sector,
                                                                                pe_relative_sector)
                print("pe_relative_sector (Rule4):", pe_relative_sector)

                # forward_pe
                forward_pe = threshold.forward_PE(self.margin_of_safety, forward_price_to_earnings,
                                                  historic_price_to_earnings_share)
                print("ForwardPE (Rule6):", forward_pe)

                # ROE vs COE
                roe_coe = threshold.roe_coe(self.margin_of_safety, roe_current, cost_of_equity)
                print("ROE vs COE (Rule 7):", roe_coe)

                # CAGR inflation
                inflation = current_year_data.iloc[-1]['Inflation Rate']
                cagr_inflation = threshold.cagr_inflation(self.margin_of_safety, historic_earnings_cagr,float(inflation)
                                                          ) # or use forecast consensus if available
                print("CAGR vs Inflation (Rule 8):",cagr_inflation)

                relative_debt_to_equity = threshold.relative_debt_to_equity(self.margin_of_safety, relative_debt_equity)
                print("Relative Debt Equity:(Rule 9):",relative_debt_to_equity)

                # add row to dataframe
                company_row = {negative_earnings, negative_shareholders_equity, beta_classify, acceptable_stock,
                               pe_relative_market,
                               pe_relative_sector, forward_pe, roe_coe, cagr_inflation, relative_debt_to_equity}
                shares_data_frame = shares_data_frame.append(company_row, ignore_index=True)

            else:
                company_row = {negative_earnings, negative_shareholders_equity, beta_classify,
                               acceptable_stock}  # only these values are calculated
                shares_data_frame = shares_data_frame.append(company_row, ignore_index=True)
        print(shares_data_frame)
