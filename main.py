import argparse
# import store as f_c_store
import invest.preprocessing.dataloader as data_loader

consumer_services_companies=["ADVTECH", "CITY LODGE HOTELS", "CLICKS GROUP", "CURRO HOLDINGS", "CASHBUILD", "FAMOUS BRANDS", "ITALTILE",
          "LEWIS GROUP", "MR PRICE GROUP", "MASSMART", "PICK N PAY STORES", "SHOPRITE", "SPAR GROUP",
          "SUN INTERNATIONAL", "SPUR", "THE FOSCHINI GROUP", "TRUWORTHS INTL", "TSOGO SUN", "WOOLWORTHS HDG"]
general_industrials_companies=[ "AFRIMAT","BARLOWORLD","BIDVEST GROUP","GRINDROD","HUDACO","IMPERIAL","INVICTA","KAP INDUSTRIAL","MPACT", "MURRAY & ROBERTS",
          "NAMPAK","PPC","RAUBEX GROUP","REUNERT","SUPER GROUP","TRENCOR","WLSN.BAYLY HOLMES-OVCON"]
all_companies= ["ADVTECH", "CITY LODGE HOTELS", "CLICKS GROUP", "CURRO HOLDINGS", "CASHBUILD", "FAMOUS BRANDS", "ITALTILE",
          "LEWIS GROUP", "MR PRICE GROUP", "MASSMART", "PICK N PAY STORES", "SHOPRITE", "SPAR GROUP",
          "SUN INTERNATIONAL", "SPUR", "THE FOSCHINI GROUP", "TRUWORTHS INTL", "TSOGO SUN", "WOOLWORTHS HDG",
          "AFRIMAT","BARLOWORLD","BIDVEST GROUP","GRINDROD","HUDACO","IMPERIAL","INVICTA","KAP INDUSTRIAL","MPACT", "MURRAY & ROBERTS",
          "NAMPAK","PPC","RAUBEX GROUP","REUNERT","SUPER GROUP","TRENCOR","WLSN.BAYLY HOLMES-OVCON"]

#user input for margin of safety and beta
#input:  python3 main.py --margin_of_safety 0.10 --beta 0.2
parser = argparse.ArgumentParser(description="Specify margin of safety and beta threshold")
parser.add_argument("--margin_of_safety",type=float, default=0.10)
parser.add_argument("--beta",type=float, default=0.10)
args = parser.parse_args()
print(args.margin_of_safety, args.beta)
data_loader.load_data()
# store = f_c_store(main_data,consumer_sector_data,consumer_market_data,general_industrials_sector_data,
#                  general_industrials_market_data, all_companies,
#                  consumer_services_companies,
#                   general_industrials_companies, args.margin_of_safety, args.beta, year, inflation)
#


