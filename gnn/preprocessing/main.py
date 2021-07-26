import argparse
import os
import time

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn


def clean(arguments):
    if args.raw_folder and args.source == 'SB':
        if not os.path.isfile(arguments.output):
            start_time = time.time()
            clean_df = pd.DataFrame()
            dir_ = arguments.raw_folder + '_' + arguments.source
            for path in os.listdir(dir_):
                if path == ".DS_Store":
                    continue
                name = path[path.index("-") + 1:path.index("2") - 1]
                df = pd.read_csv(os.path.join(dir_, path), delimiter=';')
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

    if args.raw_folder and args.source == 'IRESS':
        if not os.path.isfile(arguments.output):
            start_time = time.time()
            clean_df = pd.DataFrame()
            dir_ = arguments.raw_folder + '_' + arguments.source
            for path in os.listdir(arguments.raw_folder + '_' + arguments.source):
                if path == ".DS_Store":
                    continue
                name = path[0:path.index(".")]
                print(name)
                df = pd.read_csv(os.path.join(dir_, path), delimiter=';')
                clean_df[name] = pd.to_numeric(df['Close'])

            clean_df.reindex(index=clean_df.index[::-1]).to_csv(arguments.output + "_clean.csv", index=False)
            print("Processing Time: {:5.2f}s".format(time.time() - start_time))

        df = pd.read_csv(arguments.output + "_daily_clean.csv")
        print(df.head())

    if "SP500" in args.raw:
        if not os.path.isfile(arguments.output):
            start_time = time.time()
            df = pd.read_csv(arguments.raw + '.csv')
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
    parser.add_argument('--raw', type=str, default='')
    parser.add_argument('--raw_folder', type=str, default='data/JSE')
    parser.add_argument('--source', type=str, default='SB')
    parser.add_argument('--output', type=str, default='data/JSE')
    parser.add_argument('--plot', type=bool, default=False)
    parser.add_argument('--noise', type=bool, default=False)
    args = parser.parse_args()
    clean(args)
