import pandas as pd


def load_data(filename='data/INVEST_clean.csv'):
    return pd.read_csv(filename, sep=',')
