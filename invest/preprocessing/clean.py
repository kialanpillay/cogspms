import argparse
import os
import time
from datetime import date

import numpy as np
import pandas as pd

from dataloader import load_data

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


def clean():
    if not os.path.isfile(args.output + '_clean.csv'):
        start_time = time.time()
        df = load_data()

        df_ = pd.read_csv(os.path.join(args.raw_folder, 'DebtEquity.csv'), delimiter=';')
        df['Debt/EquityIndustry'] = df_['Debt/Equity Industry'].loc[0]
        df['Debt/EquityIndustry'] = [x.replace(',', '.') for x in df['Debt/EquityIndustry']]

        df_ = pd.read_csv(os.path.join(args.raw_folder, 'EPS_SE.csv'), delimiter=';')
        df['EPS'] = np.nan
        df['ShareholdersEquity'] = np.nan
        for index, row in df_.iterrows():
            name = row['Company']
            start_year = str(date(int(row['Year']), 1, 1))
            end_year = str(date(int(row['Year']) + 1, 1, 1))
            mask = (df['Date'] >= start_year) & (df['Date'] < end_year) & (df['Name'] == name)
            df.loc[mask, 'EPS'] = row['EPS']
            df.loc[mask, 'EPS'] = [x.replace(',', '.') for x in df.loc[mask, 'EPS']]
            df.loc[mask, 'ShareholdersEquity'] = row['ShareholdersEquity']

        rate_files = ['InflationRate', 'MarketRateOfReturn', 'RiskFreeRateOfReturn']
        for rate in rate_files:
            df_ = pd.read_csv(os.path.join(args.raw_folder, rate + '.csv'), delimiter=';')
            df[rate] = np.nan
            for index, row in df_.iterrows():
                start_year = str(date(int(row['Year']), 1, 1))
                end_year = str(date(int(row['Year']) + 1, 1, 1))
                mask = (df['Date'] >= start_year) & (df['Date'] < end_year)
                df.loc[mask, rate] = row[rate]
                df.loc[mask, rate] = [x.replace(',', '.') for x in df.loc[mask, rate]]

        df_ = pd.read_csv(os.path.join(args.raw_folder, 'ShareBeta.csv'), delimiter=';')
        df_ = df_.reindex(index=df_.index[::-1])
        df_ = df_.reset_index()
        df['ShareBeta'] = np.nan
        for index, row in df_.iterrows():
            name = row['Company']
            start = row['Date'].replace("/", "-")
            try:
                end = df_['Date'].iloc[index + 1].replace("/", "-")
                if start > end:
                    mask = (df['Date'] >= start) & (df['Name'] == name)
                else:
                    mask = (df['Date'] >= start) & (df['Date'] < end) & (df['Name'] == name)
            except IndexError:
                mask = (df['Date'] >= start) & (df['Name'] == name)
            df.loc[mask, 'ShareBeta'] = row['Beta Monthly Leveraged']
            df.loc[mask, 'ShareBeta'] = [x.replace(',', '.') for x in df.loc[mask, 'ShareBeta']]

        df_ = pd.read_csv(os.path.join(args.raw_folder, 'PEMarket.csv'), delimiter=';')
        df_ = df_.reindex(index=df_.index[::-1])
        df_ = df_.reset_index()
        df['PEMarket'] = np.nan
        for index, row in df_.iterrows():
            start = str(row['Date']).replace("/", "-")
            try:
                end = str(df_['Date'].iloc[index + 1]).replace("/", "-")
                if start > end:
                    mask = (df['Date'] >= start)
                else:
                    mask = (df['Date'] >= start) & (df['Date'] < end)
            except IndexError:
                mask = (df['Date'] >= start)
            df.loc[mask, 'PEMarket'] = row['PE']
            df.loc[mask, 'PEMarket'] = [x.replace(',', '.') for x in df.loc[mask, 'PEMarket']]

        df['PESector'] = np.nan
        sectors = [('PESectorJCSEV.csv', companies_jcsev), ('PESectorJGIND.csv', companies_jgind)]

        for sector in sectors:
            df_ = pd.read_csv(os.path.join(args.raw_folder, sector[0]), delimiter=';')
            df_ = df_.reindex(index=df_.index[::-1])
            df_ = df_.reset_index()
            for index, row in df_.iterrows():
                start = str(row['Date']).replace("/", "-")
                try:
                    end = str(df_['Date'].iloc[index + 1]).replace("/", "-")
                    if start > end:
                        mask = (df['Date'] >= start) & (df['Name'].isin(sector[1]))
                    else:
                        mask = (df['Date'] >= start) & (df['Date'] < end) & (df['Name'].isin(sector[1]))
                except IndexError:
                    mask = (df['Date'] >= start)
                df.loc[mask, 'PESector'] = row['PE']
                df.loc[mask, 'PESector'] = [x.replace(',', '.') for x in df.loc[mask, 'PESector']]

        output_file = args.output + "_clean.csv"
        df.to_csv(output_file, index=False)
        print("Processing Time: {:5.2f}s".format(time.time() - start_time))


def merge():
    if True:
        start_time = time.time()
        df = pd.read_csv(os.path.join(args.raw_folder, 'CompanyHistoricData.csv'), delimiter=';')
        df = df.rename(columns={'Close': 'Price', 'Company': 'Name', 'Beta Weekly Unleveraged': 'ShareBeta'})
        for c in df.columns:
            if c == "Name" or c == "Date":
                continue
            if df[c].dtype == np.int64 or df[c].dtype == np.float64:
                continue
            df[c] = [x.replace(',', '.') for x in df[c].values]

        df_ = pd.read_csv(os.path.join(args.raw_folder, 'DebtEquity.csv'), delimiter=';')
        df['Debt/EquityIndustry'] = df_['Debt/EquityIndustry'].loc[0]
        df['Debt/EquityIndustry'] = [x.replace(',', '.') for x in df['Debt/EquityIndustry']]

        rate_files = ['InflationRate', 'MarketRateOfReturn', 'RiskFreeRateOfReturn']
        for rate in rate_files:
            df_ = pd.read_csv(os.path.join(args.raw_folder, rate + '.csv'), delimiter=';')
            df[rate] = np.nan
            for index, row in df_.iterrows():
                start_year = str(date(int(row['Year']), 1, 1))
                end_year = str(date(int(row['Year']) + 1, 1, 1))
                mask = (df['Date'] >= start_year) & (df['Date'] < end_year)
                df.loc[mask, rate] = row[rate]
                df.loc[mask, rate] = [x.replace(',', '.') for x in df.loc[mask, rate]]

        df_ = pd.read_csv(os.path.join(args.raw_folder, 'ALSI.csv'), delimiter=';')
        df_ = df_.reindex(index=df_.index[::-1])
        df_ = df_.reset_index()
        df['PEMarket'] = np.nan
        for index, row in df_.iterrows():
            start = str(row['Date'])
            try:
                end = str(df_['Date'].iloc[index + 1])
                if start > end:
                    mask = (df['Date'] >= start)
                else:
                    mask = (df['Date'] >= start) & (df['Date'] < end)
            except IndexError:
                mask = (df['Date'] >= start)
            df.loc[mask, 'PEMarket'] = row['PE']
            df.loc[mask, 'PEMarket'] = [x.replace(',', '.') for x in df.loc[mask, 'PEMarket']]

        df['PESector'] = np.nan
        sectors = [('JCSEV.csv', companies_jcsev), ('JGIND.csv', companies_jgind)]

        for sector in sectors:
            df_ = pd.read_csv(os.path.join(args.raw_folder, sector[0]), delimiter=';')
            df_ = df_.reindex(index=df_.index[::-1])
            df_ = df_.reset_index()
            for index, row in df_.iterrows():
                start = str(row['Date'])
                try:
                    end = str(df_['Date'].iloc[index + 1])
                    if start > end:
                        mask = (df['Date'] >= start) & (df['Name'].isin(sector[1]))
                    else:
                        mask = (df['Date'] >= start) & (df['Date'] < end) & (df['Name'].isin(sector[1]))
                except IndexError:
                    mask = (df['Date'] >= start)
                df.loc[mask, 'PESector'] = row['PE']
                df.loc[mask, 'PESector'] = [x.replace(',', '.') for x in df.loc[mask, 'PESector']]

        cols = []
        for path in sorted(os.listdir(args.raw_folder + '/Company')):
            if path == ".DS_Store":
                continue
            df_ = pd.read_csv(os.path.join(args.raw_folder, 'Company', path), delimiter=';')
            name = pd.unique(df_['Company'].values)[0]

            df_ = df_.drop(columns=['Company']).T.rename(
                columns={'Debt / Equity': 'Debt/Equity', 'Earnings / Share (c)': 'EPS',
                         'Price / Earnings': 'PEYear', 'Return On Average Equity %': 'ROAE',
                         'Return On Equity %': 'ROE', 'Ordinary Shareholders Equity at End of Year'
                         : 'ShareholdersEquity'})
            if len(cols) == 0:
                cols = df_.columns
            for column in df_.columns:
                if column not in df:
                    df[column] = np.nan
                for index, row in df_.iterrows():
                    start_year = str(date(int(index), 1, 1))
                    end_year = str(date(int(index) + 1, 1, 1))
                    mask = (df['Date'] >= start_year) & (df['Date'] < end_year) & (df['Name'] == name)
                    df.loc[mask, column] = row[column]

        for c in cols:
            df[c] = df[c].astype(str)
            df[c] = [x.replace(',', '.') for x in df[c].values]
        df['Date'] = [x.replace('/', '-') for x in df['Date'].values]
        df = df.reindex(index=df.index[::-1])

        output_file = args.output + "_clean.csv"
        df.to_csv(output_file, index=False)
        print("Processing Time: {:5.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw_folder', type=str, default='data/INVEST_IRESS_')
    parser.add_argument('--output', type=str, default='data/INVEST')
    args = parser.parse_args()
    merge()
