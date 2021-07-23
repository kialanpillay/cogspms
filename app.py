import argparse

import invest.networks.value_evaluation as value_eval_network
import invest.networks.quality_evaluation as quality_eval_network
import invest.networks.invest_recommendation as invest_recommendation_network
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
    df = data_loader.load_dummy_data()
    store = Store(df, all_companies_dummy, consumer_services_companies_dummy, general_industrials_companies_dummy,
                  args.margin_of_safety,
                  args.beta, 2017)

    value_decision = value_eval_network.value_network()
    quality_decision=  quality_eval_network.quality_network()
    invest_recommendation_network.investment_recommendation(value_decision,quality_decision)





if __name__ == '__main__':
    # input:  python3 app.py --margin_of_safety 0.10 --beta 0.2
    parser = argparse.ArgumentParser(description='Intelligent system for automated share evaluation',
                                     epilog='Version 0.1')
    parser.add_argument("--margin_of_safety", type=float, default=0.10)
    parser.add_argument("--beta", type=float, default=0.10)
    args = parser.parse_args()
    main(args)
