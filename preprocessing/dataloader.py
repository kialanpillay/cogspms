import pandas as pd

df = pd.read_csv("/Users/insaafdhansay/desktop/cogspms/preprocessing/data/invest_data.csv", sep=';')
#print(df.columns)
companies= ["ADVTECH", "CITY LODGE HOTELS", "CLICKS GROUP", "CURRO HOLDINGS", "CASHBUILD", "FAMOUS BRANDS", "ITALTILE",
          "LEWIS GROUP", "MR PRICE GROUP", "MASSMART", "PICK N PAY STORES", "SHOPRITE", "SPAR GROUP",
          "SUN INTERNATIONAL", "SPUR", "THE FOSCHINI GROUP", "TRUWORTHS INTL", "TSOGO SUN", "WOOLWORTHS HDG",
          "AFRIMAT","BARLOWORLD","BIDVEST GROUP","GRINDROD","HUDACO","IMPERIAL","INVICTA","KAP INDUSTRIAL","MPACT", "MURRAY & ROBERTS",
          "NAMPAK","PPC","RAUBEX GROUP","REUNERT","SUPER GROUP","TRENCOR","WLSN.BAYLY HOLMES-OVCON"]
final_df = df.loc[df['Name'].isin(companies)]

print(final_df['Name'].unique())
#print(final_df['Name'].nun ique())


# functions to pass it data for X period of time- one year
