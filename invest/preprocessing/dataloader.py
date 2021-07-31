import pandas as pd


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
