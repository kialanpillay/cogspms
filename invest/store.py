import numpy as np
import pandas as pd

import invest.calculator.ratios as ratios
import invest.calculator.threshold as threshold


class Store:
    def __init__(self, main_data, companies, companies_jcsev, companies_jgind, margin_of_safety,
                 beta, years, extension):
        self.df_main = main_data
        self.companies = companies
        self.companies_jcsev = companies_jcsev
        self.companies_jgind = companies_jgind
        self.margin_of_safety = margin_of_safety
        self.beta = beta
        self.years = years
        self.extension = extension
        self.column_names = ["company_name", "negative_earnings", "negative_shareholders_equity", "beta_classify",
                             "acceptable_stock",
                             "current_PE_relative_share_market_to_historical",
                             "current_PE_relative_share_sector_to_historical",
                             "forward_PE_current_to_historical", "roe_vs_coe",
                             "growth_cagr_vs_inflation", "relative_debt_to_equity", "systematic_risk"]
        self.df_shares = pd.DataFrame(columns=self.column_names)
        self.process()

    def process(self):
        for company in self.companies:
            eps_year_list = []
            pe_sector_list = []
            pe_market_list = []

            start_year = self.years - 4
            end_year = self.years
            df_current_year = None
            current_price = None
            for i in range(start_year, end_year):
                mask_eps = (self.df_main['Date'] >= str(i) + '-01-01') & (
                        self.df_main['Date'] <= str(i) + '-12-31') & (self.df_main['Name'] == company)
                company_df_by_year = self.df_main.loc[mask_eps]

                eps = company_df_by_year.iloc[-1]['EPS']
                eps_year_list.append(eps)

                mask_current_price = (self.df_main['Date'] >= str(end_year - 1) + '-' + '01-01') & (
                        self.df_main['Date'] < str(end_year) + '-' + '01-01') & (self.df_main['Name'] == company)
                df_current_year = self.df_main.loc[mask_current_price]
                current_price = df_current_year.iloc[-1]['Price']

                mask_pe_sector_market = (self.df_main['Date'] >= str(end_year - 3) + '-' + '01-01') & (
                        self.df_main['Date'] < str(end_year) + '-' + '01-01') & (self.df_main['Name'] == company)
                pe_sector_3_years = self.df_main.loc[mask_pe_sector_market]
                pe_market_3_years = self.df_main.loc[mask_pe_sector_market]
                for v in pe_sector_3_years['PESector'].to_numpy():
                    if not np.isnan(v):
                        pe_sector_list.append(float(v))

                for v in pe_market_3_years['PEMarket'].to_numpy():
                    if not np.isnan(v):
                        pe_market_list.append(float(v))

            # historic_earnings_growth_rate
            growth_years_n = end_year - start_year
            historic_earnings_growth_rate = ratios.historic_earnings_growth_rate(eps_year_list, growth_years_n)

            # historic_earnings_cagr
            historic_earnings_cagr = ratios.historic_earnings_cagr(eps_year_list[-1], eps_year_list[-4], 3)

            # historic_price_to_earnings_share
            mask_pe = (self.df_main['Date'] >= str(end_year - 1) + '-01-01') & (
                    self.df_main['Date'] < str(end_year) + '-01-01') & (self.df_main['Name'] == company)
            df_company_3_years = self.df_main.loc[mask_pe]
            price_list_3_years = df_company_3_years['Price'].to_numpy()
            eps_list_3_years = df_company_3_years['EPS'].to_numpy()
            historic_price_to_earnings_share = ratios.historic_price_to_earnings_share(price_list_3_years,
                                                                                       eps_list_3_years)
            forward_earnings_current_year = ratios.forward_earnings(eps_year_list[-1], historic_earnings_growth_rate)

            historic_earnings_growth_rate_past = ratios.historic_earnings_growth_rate(eps_year_list, 3)
            # intermediate, list from past can be 2013 since year is 3

            forward_earnings_past = ratios.forward_earnings(eps_year_list[-1],
                                                            historic_earnings_growth_rate_past)  # intermediate
            forward_earnings_cagr = ratios.forward_earnings_cagr(forward_earnings_current_year, forward_earnings_past,
                                                                 3)

            forward_price_to_earnings = ratios.forward_price_to_earnings(current_price, forward_earnings_current_year)

            # PE Relative
            pe_relative_market = ratios.pe_relative_market(historic_price_to_earnings_share, pe_market_list)
            pe_relative_sector = ratios.pe_relative_sector(historic_price_to_earnings_share, pe_sector_list)

            # ROE
            roe_current = df_current_year.iloc[-1]['ROE']

            # COE
            market_rate_of_return = df_current_year.iloc[-1]['MarketRateOfReturn']
            risk_free_rate_of_return = df_current_year.iloc[-1]['RiskFreeRateOfReturn']
            share_beta = df_current_year.iloc[-1]['ShareBeta']
            cost_of_equity = ratios.cost_of_equity(float(market_rate_of_return), float(risk_free_rate_of_return),
                                                   float(share_beta))

            # Relative Debt/Equity
            debt_equity = df_current_year.iloc[-1]['Debt/Equity']
            debt_equity_industry = df_current_year.iloc[-1]['Debt/EquityIndustry']
            relative_debt_equity = ratios.relative_debt_to_equity(float(debt_equity), float(
                debt_equity_industry))

            # Threshold
            negative_earnings = threshold.negative_earnings(forward_earnings_current_year)
            shareholders_equity = df_current_year.iloc[-1]['ShareholdersEquity']
            negative_shareholders_equity = threshold.negative_shareholders_equity(float(shareholders_equity))
            beta_classify = threshold.beta_classify(float(share_beta), self.beta)
            acceptable_stock = threshold.acceptable_stock(negative_earnings, negative_shareholders_equity,
                                                          beta_classify)

            if acceptable_stock:
                current_share_pe = df_current_year.iloc[-1]['PE']
                current_market_pe = df_current_year.iloc[-1]['PEMarket']

                current_sector_pe = df_current_year.iloc[-1]['PESector']

                pe_current_share_market = ratios.current_pe_market(float(current_share_pe),
                                                                   float(current_market_pe))  # PE value for this year

                pe_current_share_sector = ratios.current_pe_sector(float(current_share_pe),
                                                                   float(current_sector_pe))  # PE value for this year
                pe_relative_market_ = threshold.current_pe_relative_share_market(self.margin_of_safety,
                                                                                 pe_current_share_market,
                                                                                 pe_relative_market)
                pe_relative_sector_ = threshold.current_pe_relative_share_sector(self.margin_of_safety,
                                                                                 pe_current_share_sector,
                                                                                 pe_relative_sector)
                # Forward PE
                forward_pe = threshold.forward_pe(self.margin_of_safety, forward_price_to_earnings,
                                                  historic_price_to_earnings_share)

                # ROE vs COE
                roe_coe = threshold.roe_coe(self.margin_of_safety, roe_current, cost_of_equity)

                # CAGR inflation
                inflation = df_current_year.iloc[-1]['InflationRate']
                cagr_inflation = threshold.cagr_inflation(self.margin_of_safety, historic_earnings_cagr,
                                                          float(inflation))

                relative_debt_to_equity = threshold.relative_debt_to_equity(self.margin_of_safety, relative_debt_equity)

                if self.extension:
                    systematic_risk = threshold.systematic_risk_classification(float(share_beta))
                else:
                    systematic_risk = None

                company_row = {"company_name": company,
                               "negative_earnings": negative_earnings,
                               "negative_shareholders_equity": negative_shareholders_equity,
                               "beta_classify": beta_classify,
                               "acceptable_stock": acceptable_stock,
                               "current_PE_relative_share_market_to_historical": pe_relative_market_,
                               "current_PE_relative_share_sector_to_historical": pe_relative_sector_,
                               "forward_PE_current_to_historical": forward_pe, "roe_vs_coe": roe_coe,
                               "growth_cagr_vs_inflation": cagr_inflation,
                               "relative_debt_to_equity": relative_debt_to_equity,
                               "systematic_risk": systematic_risk}
                self.df_shares = self.df_shares.append(company_row, ignore_index=True)
            else:
                company_row = {"company_name": company,
                               "negative_earnings": negative_earnings,
                               "negative_shareholders_equity": negative_shareholders_equity,
                               "beta_classify": beta_classify,
                               "acceptable_stock": acceptable_stock}
                self.df_shares = self.df_shares.append(company_row, ignore_index=True)

    def get_acceptable_stock(self, company):
        return self.df_shares.loc[self.df_shares['company_name'] == company, "acceptable_stock"].iloc[0]

    def get_pe_relative_market(self, company):
        return self.df_shares.loc[self.df_shares['company_name'] == company,
                                  "current_PE_relative_share_market_to_historical"].iloc[0]

    def get_pe_relative_sector(self, company):
        return self.df_shares.loc[self.df_shares['company_name'] == company,
                                  "current_PE_relative_share_sector_to_historical"].iloc[0]

    def get_forward_pe(self, company):
        return self.df_shares.loc[self.df_shares['company_name'] == company, "forward_PE_current_to_historical"].iloc[0]

    def get_roe_vs_coe(self, company):
        return self.df_shares.loc[self.df_shares['company_name'] == company, "roe_vs_coe"].iloc[0]

    def get_relative_debt_equity(self, company):
        return self.df_shares.loc[self.df_shares['company_name'] == company, "relative_debt_to_equity"].iloc[0]

    def get_cagr_vs_inflation(self, company):
        return self.df_shares.loc[self.df_shares['company_name'] == company, "growth_cagr_vs_inflation"].iloc[0]

    def get_systematic_risk(self, company):
        return self.df_shares.loc[self.df_shares['company_name'] == company, "systematic_risk"].iloc[0]
