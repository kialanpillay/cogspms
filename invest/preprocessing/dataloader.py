import pandas as pd

companies = ["ADVTECH", "CITY LODGE HOTELS", "CLICKS GROUP", "CURRO HOLDINGS", "CASHBUILD", "FAMOUS BRANDS", "ITALTILE",
             "LEWIS GROUP", "MR PRICE GROUP", "MASSMART", "PICK N PAY STORES", "SHOPRITE", "SPAR GROUP",
             "SUN INTERNATIONAL", "SPUR", "THE FOSCHINI GROUP", "TRUWORTHS INTL", "TSOGO SUN", "WOOLWORTHS HDG",
             "AFRIMAT", "BARLOWORLD", "BIDVEST GROUP", "GRINDROD", "HUDACO", "IMPERIAL", "INVICTA", "KAP INDUSTRIAL",
             "MPACT", "MURRAY & ROBERTS",
             "NAMPAK", "PPC", "RAUBEX GROUP", "REUNERT", "SUPER GROUP", "TRENCOR", "WLSN.BAYLY HOLMES-OVCON"]


def load_data(filename='data/INVEST_clean.csv'):
    return pd.read_csv(filename, sep=',')


def load_dummy_data():
    df = pd.read_csv("data/dummy_data_use.csv", sep=';')
    df['PEMarket'] = [x.replace(',', '.') for x in df['PEMarket']]
    df['PESector'] = [x.replace(',', '.') for x in df['PESector']]
    df['MarketRateOfReturn'] = [x.replace(',', '.') for x in df['MarketRateOfReturn']]
    df['RiskFreeRateOfReturn'] = [x.replace(',', '.') for x in df['RiskFreeRateOfReturn']]
    df['ShareBeta'] = [x.replace(',', '.') for x in df['ShareBeta']]
    df['ShareholdersEquity'] = [x.replace(',', '.') for x in df['ShareholdersEquity']]
    df['InflationRate'] = [x.replace(',', '.') for x in df['InflationRate']]
    return df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
