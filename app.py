import argparse

import invest.networks.invest_recommendation as invest_recommendation_network
import invest.networks.quality_evaluation as quality_eval_network
import invest.networks.value_evaluation as value_eval_network
import invest.preprocessing.dataloader as data_loader
from invest.store import Store


def main(arguments):
    consumer_services_companies = ["ADVTECH", "CITY LODGE HOTELS", "CLICKS GROUP", "CURRO HOLDINGS", "CASHBUILD",
                                   "FAMOUS BRANDS", "ITALTILE",
                                   "LEWIS GROUP", "MR PRICE GROUP", "MASSMART", "PICK N PAY STORES", "SHOPRITE",
                                   "SPAR GROUP",
                                   "SUN INTERNATIONAL", "SPUR", "THE FOSCHINI GROUP", "TRUWORTHS INTL", "TSOGO SUN",
                                   "WOOLWORTHS HDG"]
    general_industrials_companies = ["AFRIMAT", "BARLOWORLD", "BIDVEST GROUP", "GRINDROD", "HUDACO", "IMPERIAL",
                                     "INVICTA",
                                     "KAP INDUSTRIAL", "MPACT", "MURRAY & ROBERTS",
                                     "NAMPAK", "PPC", "RAUBEX GROUP", "REUNERT", "SUPER GROUP", "TRENCOR",
                                     "WLSN.BAYLY HOLMES-OVCON"]
    all_companies = ["ADVTECH", "CITY LODGE HOTELS", "CLICKS GROUP", "CURRO HOLDINGS", "CASHBUILD", "FAMOUS BRANDS",
                     "ITALTILE",
                     "LEWIS GROUP", "MR PRICE GROUP", "MASSMART", "PICK N PAY STORES", "SHOPRITE", "SPAR GROUP",
                     "SUN INTERNATIONAL", "SPUR", "THE FOSCHINI GROUP", "TRUWORTHS INTL", "TSOGO SUN", "WOOLWORTHS HDG",
                     "AFRIMAT", "BARLOWORLD", "BIDVEST GROUP", "GRINDROD", "HUDACO", "IMPERIAL", "INVICTA",
                     "KAP INDUSTRIAL", "MPACT", "MURRAY & ROBERTS",
                     "NAMPAK", "PPC", "RAUBEX GROUP", "REUNERT", "SUPER GROUP", "TRENCOR", "WLSN.BAYLY HOLMES-OVCON"]
    all_companies_dummy = ["SPUR"]
    consumer_services_companies_dummy = ["SPUR"]
    general_industrials_companies_dummy = []
    extension=False
    df = data_loader.load_dummy_data()
    investment_portfolio = []

    for year in range (2015,2018):
        store = Store(df, all_companies_dummy, consumer_services_companies_dummy, general_industrials_companies_dummy,
                      args.margin_of_safety,
                      args.beta, year,extension)
        for company in all_companies:
            if store.get_acceptable_stock(company) == True:

            #get all necessary values from pandas data frame - value network
                pe_relative_market= store.get_pe_relative_market(company)
                pe_relative_sector= store.get_pe_relative_sector(company)
                forward_pe = store.get_forward_pe(company)

                #get all necessary values from pandas data frame - quality network
                roe_vs_coe = store.get_roe_vs_coe(company)
                rel_DE = store.get_rel_DE(company)
                cagr_vs_inflation = store.get_cagr_vs_inflation(company)
                systematic_risk = store.get_systematic_risk(company)

                #running bayesian networks
                value_decision = value_eval_network.value_network(pe_relative_market,pe_relative_sector,forward_pe)
                quality_decision = quality_eval_network.quality_network(roe_vs_coe,rel_DE,cagr_vs_inflation,systematic_risk,extension)
                decision = invest_recommendation_network.investment_recommendation(value_decision, quality_decision)
                if(decision=="Yes"):
                    investment_portfolio.append(company)



if __name__ == '__main__':
    # input:  python3 app.py --margin_of_safety 0.10 --beta 0.2
    parser = argparse.ArgumentParser(description='Intelligent system for automated share evaluation',
                                     epilog='Version 0.1')
    parser.add_argument("--margin_of_safety", type=float, default=0.10)
    parser.add_argument("--beta", type=float, default=0.10)
    args = parser.parse_args()
    main(args)
