import argparse
import os
import time

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn


def clean(arguments):
    if args.raw_folder:
        if not os.path.isfile(arguments.output):
            start_time = time.time()
            clean_df = pd.DataFrame()
            for path in os.listdir(arguments.raw_folder):
                name = path[path.index("-") + 1:path.index("2") - 1]
                df = pd.read_csv(os.path.join(arguments.raw_folder, path), delimiter=';')
                clean_df[name] = pd.to_numeric(df['Closing (c)'])
                clean_df[name].fillna(0, inplace=True)

            clean_df.reindex(index=clean_df.index[::-1]).to_csv(arguments.output + "_clean.csv", index=False)
            print("Processing Time: {:5.2f}s".format(time.time() - start_time))

        df = pd.read_csv(arguments.output + "_clean.csv")
        sample_df = df[['PROSUS', 'ANGGOLD', 'NEDBANK', 'SASOL', "VODACOM", "BHP"]]
        corr = sample_df.corr()
        if arguments.plot:
            sn.heatmap(corr, annot=True)
            plt.show()

    if "SP500" in args.raw:
        if not os.path.isfile(arguments.output):
            start_time = time.time()
            df = pd.read_csv(arguments.raw)
            clean_df = pd.DataFrame()
            names = df['Name'].unique()

            for name in names:
                df_ = pd.DataFrame(df.loc[df['Name'] == name]['close'].values, columns=[name])
                if df_.shape[0] == 1259:
                    clean_df = pd.concat([clean_df, df_], axis=1)

            clean_df.to_csv(arguments.output + "_clean.csv", index=False)
            print("Processing Time: {:5.2f}s".format(time.time() - start_time))

        df = pd.read_csv(arguments.output + "_clean.csv")
        sample_df = df[['AAPL', 'AMZN', 'FB', 'GOOGL', "MSFT", "XRAY"]]
        corr = sample_df.corr()
        if arguments.plot:
            sn.heatmap(corr, annot=True)
            plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw', type=str, default='data/all_stocks_5yr.csv')
    parser.add_argument('--raw_folder', type=str, default='data/JSE')
    parser.add_argument('--output', type=str, default='data/JSE')
    parser.add_argument('--plot', type=bool, default=False)
    parser.add_argument('--noise', type=bool, default=False)
    args = parser.parse_args()
    clean(args)
