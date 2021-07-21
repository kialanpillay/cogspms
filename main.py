import argparse

import invest.preprocessing.dataloader as data_loader
from invest.store import Store
import invest.networks.value_evaluation as value_eval_network


consumer_services_companies = ["ADVTECH", "CITY LODGE HOTELS", "CLICKS GROUP", "CURRO HOLDINGS", "CASHBUILD",
                               "FAMOUS BRANDS", "ITALTILE",
                               "LEWIS GROUP", "MR PRICE GROUP", "MASSMART", "PICK N PAY STORES", "SHOPRITE",
                               "SPAR GROUP",
                               "SUN INTERNATIONAL", "SPUR", "THE FOSCHINI GROUP", "TRUWORTHS INTL", "TSOGO SUN",
                               "WOOLWORTHS HDG"]
general_industrials_companies = ["AFRIMAT", "BARLOWORLD", "BIDVEST GROUP", "GRINDROD", "HUDACO", "IMPERIAL", "INVICTA",
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
# input:  python3 main.py --margin_of_safety 0.10 --beta 0.2
parser = argparse.ArgumentParser(description="Specify margin of safety and beta threshold")
parser.add_argument("--margin_of_safety", type=float, default=0.10)
parser.add_argument("--beta", type=float, default=0.10)
args = parser.parse_args()
df = data_loader.load_dummy_data()
store = Store(df, all_companies_dummy, consumer_services_companies_dummy, general_industrials_companies_dummy,
              args.margin_of_safety,
              args.beta, 2017)


value_eval_network.value_network()

