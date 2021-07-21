import pandas as pd

companies = ["ADVTECH", "CITY LODGE HOTELS", "CLICKS GROUP", "CURRO HOLDINGS", "CASHBUILD", "FAMOUS BRANDS", "ITALTILE",
             "LEWIS GROUP", "MR PRICE GROUP", "MASSMART", "PICK N PAY STORES", "SHOPRITE", "SPAR GROUP",
             "SUN INTERNATIONAL", "SPUR", "THE FOSCHINI GROUP", "TRUWORTHS INTL", "TSOGO SUN", "WOOLWORTHS HDG",
             "AFRIMAT", "BARLOWORLD", "BIDVEST GROUP", "GRINDROD", "HUDACO", "IMPERIAL", "INVICTA", "KAP INDUSTRIAL",
             "MPACT", "MURRAY & ROBERTS",
             "NAMPAK", "PPC", "RAUBEX GROUP", "REUNERT", "SUPER GROUP", "TRENCOR", "WLSN.BAYLY HOLMES-OVCON"]


def load_data():
    df = pd.read_csv("/Users/insaafdhansay/desktop/cogspms/invest/preprocessing/data/invest_data.csv", sep=';')
    mask = (df['Date'] > '2012-01-01')
    int_df = df.loc[df['Name'].isin(companies)]  # 36 Shares
    final_df = int_df.loc[mask]
    print(final_df['Name'].unique())
    print(final_df['Name'].nunique())
    print(final_df)


def load_dummy_data():
    df = pd.read_csv("/Users/insaafdhansay/desktop/cogspms/invest/preprocessing/data/dummy_data_use.csv", sep=';')

    df['PEMarket'] = [x.replace(',', '.') for x in df['PEMarket']]
    df['PESector'] = [x.replace(',', '.') for x in df['PESector']]
    df['MarketRateOfReturn'] = [x.replace(',', '.') for x in df['MarketRateOfReturn']]
    df['RiskFreeRateOfReturn'] = [x.replace(',', '.') for x in df['RiskFreeRateOfReturn']]
    df['Share Beta'] = [x.replace(',', '.') for x in df['Share Beta']]
    df['Shareholders Equity'] = [x.replace(',', '.') for x in df['Shareholders Equity']]
    df['Inflation Rate'] = [x.replace(',', '.') for x in df['Inflation Rate']]
    df_trimmed = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    return df_trimmed
