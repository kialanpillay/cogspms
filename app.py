import argparse

import pandas as pd

import invest.evaluation.validation as validation
from invest.networks.invest_recommendation import investment_recommendation
from invest.networks.quality_evaluation import quality_network
from invest.networks.value_evaluation import value_network
from invest.preprocessing.dataloader import load_data
from invest.store import Store


def main():
    companies_jcsev = ["ADVTECH", "CITY LODGE HOTELS", "CLICKS GROUP", "CURRO HOLDINGS", "CASHBUILD",
                       "FAMOUS BRANDS", "ITALTILE",
                       "LEWIS GROUP", "MR PRICE GROUP", "MASSMART", "PICK N PAY STORES", "SHOPRITE",
                       "SPAR GROUP",
                       "SUN INTERNATIONAL", "SPUR", "THE FOSCHINI GROUP", "TRUWORTHS INTL", "TSOGO SUN",
                       "WOOLWORTHS HDG"]
    companies_jgind = ["AFRIMAT", "BARLOWORLD", "BIDVEST GROUP", "GRINDROD", "HUDACO", "IMPERIAL",
                       "INVICTA",
                       "KAP INDUSTRIAL", "MPACT", "MURRAY & ROBERTS",
                       "NAMPAK", "PPC", "RAUBEX GROUP", "REUNERT", "SUPER GROUP", "TRENCOR",
                       "WLSN.BAYLY HOLMES-OVCON"]
    companies = ["ADVTECH", "CITY LODGE HOTELS", "CLICKS GROUP", "CURRO HOLDINGS", "CASHBUILD", "FAMOUS BRANDS",
                 "ITALTILE",
                 "LEWIS GROUP", "MR PRICE GROUP", "MASSMART", "PICK N PAY STORES", "SHOPRITE", "SPAR GROUP",
                 "SUN INTERNATIONAL", "SPUR", "THE FOSCHINI GROUP", "TRUWORTHS INTL", "TSOGO SUN", "WOOLWORTHS HDG",
                 "AFRIMAT", "BARLOWORLD", "BIDVEST GROUP", "GRINDROD", "HUDACO", "IMPERIAL", "INVICTA",
                 "KAP INDUSTRIAL", "MPACT", "MURRAY & ROBERTS",
                 "NAMPAK", "PPC", "RAUBEX GROUP", "REUNERT", "SUPER GROUP", "TRENCOR", "WLSN.BAYLY HOLMES-OVCON"]

    df = load_data()
    df_benchmark = pd.read_csv('data/benchmark_data.csv', delimiter=';', index_col=False)

    prices_current_jgind = {"2017": [], "2016": [], "2015": []}
    prices_current_jcsev = {"2017": [], "2016": [], "2015": []}
    prices_initial_jgind = {"2017": [], "2016": [], "2015": []}
    prices_initial_jcsev = {"2017": [], "2016": [], "2015": []}
    share_betas_jgind = {"2017": [], "2016": [], "2015": []}
    share_betas_jcsev = {"2017": [], "2016": [], "2015": []}
    investable_shares_jgind = {"2017": [], "2016": [], "2015": []}
    investable_shares_jcsev = {"2017": [], "2016": [], "2015": []}

    for year in range(2015, 2018):
        store = Store(df, companies, companies_jcsev, companies_jgind,
                      args.margin_of_safety,
                      args.beta, year, args.extension)
        for company in companies:
            if store.get_acceptable_stock(company):
                pe_relative_market = store.get_pe_relative_market(company)
                pe_relative_sector = store.get_pe_relative_sector(company)
                forward_pe = store.get_forward_pe(company)

                roe_vs_coe = store.get_roe_vs_coe(company)
                relative_debt_equity = store.get_relative_debt_equity(company)
                cagr_vs_inflation = store.get_cagr_vs_inflation(company)
                systematic_risk = store.get_systematic_risk(company)

                value_decision = value_network(pe_relative_market, pe_relative_sector, forward_pe)
                quality_decision = quality_network(roe_vs_coe, relative_debt_equity, cagr_vs_inflation,
                                                   systematic_risk, args.extension)
                decision = investment_recommendation(value_decision, quality_decision)
                if decision == "Yes":

                    mask = (df['Date'] >= str(year) + '-01-01') & (
                            df['Date'] <= str(year) + '-12-31') & (df['Name'] == company)
                    df_year = df[mask]
                    share_beta = df_year.iloc[-1]["ShareBeta"]
                    price_current = df_year.iloc[-1]['Price']
                    price_initial = df_year.iloc[0]['Price']

                    if company in companies_jcsev:
                        investable_shares_jcsev[str(year)].append(company)
                        prices_current_jcsev[str(year)].append(price_current)
                        prices_initial_jcsev[str(year)].append(price_initial)
                        share_betas_jcsev[str(year)].append(share_beta)
                    else:
                        investable_shares_jgind[str(year)].append(company)
                        prices_current_jgind[str(year)].append(price_current)
                        prices_initial_jgind[str(year)].append(price_initial)
                        share_betas_jgind[str(year)].append(share_beta)

    for year in range(2015, 2018):
        print(year, "JGIND", investable_shares_jgind[str(year)])
        print(year, "JCSEV", investable_shares_jcsev[str(year)])
    validation.process_metrics(df, df_benchmark, prices_current_jcsev, prices_initial_jcsev, share_betas_jcsev, 2015,
                               2018, "JCSEV")
    validation.process_metrics(df, df_benchmark, prices_current_jgind, prices_initial_jgind, share_betas_jgind, 2015,
                               2018, "JGIND")


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Intelligent system for automated share evaluation',
                                     epilog='Version 0.1')
    parser.add_argument("--margin_of_safety", type=float, default=0.10)
    parser.add_argument("--beta", type=float, default=0.10)
    parser.add_argument("--extension", type=str2bool, default=False)
    args = parser.parse_args()
    main()
