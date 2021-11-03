import argparse
import os
import time

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn


def clean():
    if args.raw_folder and args.source == 'SB' and args.price == 'C':
        if not os.path.isfile(args.output + '_clean_truncated.csv') or not os.path.isfile(args.output + '_clean.csv'):
            start_time = time.time()
            clean_df = pd.DataFrame()
            dir_ = args.raw_folder + '_' + args.source
            for path in os.listdir(dir_):
                if path == ".DS_Store":
                    continue

                name = path[path.index("-") + 1:path.index("2") - 1]
                df = pd.read_csv(os.path.join(dir_, path), delimiter=';')
                if args.truncate and df.shape[0] < 3000:
                    continue
                clean_df[name] = pd.to_numeric(df['Closing (c)'])
                clean_df[name].fillna(0, inplace=True)

            clean_df = clean_df.reindex(index=clean_df.index[::-1])
            if args.truncate:
                output_file = args.output + "_clean_truncated.csv"
                clean_df.tail(3146).to_csv(output_file, index=False)
            else:
                output_file = args.output + "_clean.csv"
                clean_df.to_csv(output_file, index=False)
            print("Processing Time: {:5.2f}s".format(time.time() - start_time))

        if args.truncate:
            df = pd.read_csv(args.output + "_clean_truncated.csv")
        else:
            df = pd.read_csv(args.output + "_clean.csv")
        corr = df.corr()
        if args.plot:
            sn.set(font_scale=1)
            sn.heatmap(corr, annot=False, center=0, cmap='coolwarm', square=True)
            plt.savefig(os.path.join('img', 'JSE_corr.png'), dpi=300, bbox_inches='tight')

    elif args.raw_folder and args.source == 'SB' and args.price == 'VWAP':
        if not os.path.isfile(args.output + '_clean_truncated_VWAP.csv') \
                or not os.path.isfile(args.output + '_clean_VWAP.csv'):
            start_time = time.time()
            clean_df = pd.DataFrame()
            dir_ = args.raw_folder + '_' + args.source
            for path in os.listdir(dir_):
                if path == ".DS_Store":
                    continue

                name = path[path.index("-") + 1:path.index("2") - 1]
                df = pd.read_csv(os.path.join(dir_, path), delimiter=';')
                if args.truncate and df.shape[0] < 3000:
                    continue
                clean_df[name] = pd.to_numeric((df['Closing (c)'] + df['High (c)'] + df['Low (c)']) / 3)
                clean_df[name].fillna(0, inplace=True)

            clean_df = clean_df.reindex(index=clean_df.index[::-1])
            if args.truncate:
                output_file = args.output + "_clean_truncated_VWAP.csv"
                clean_df.tail(3146).to_csv(output_file, index=False)
            else:
                output_file = args.output + "_clean_VWAP.csv"
                clean_df.to_csv(output_file, index=False)
            print("Processing Time: {:5.2f}s".format(time.time() - start_time))

    elif args.raw_folder and args.source == 'IRESS':
        if not os.path.isfile(args.output):
            start_time = time.time()
            clean_df = pd.DataFrame()
            for path in os.listdir(args.raw_folder):
                if path == ".DS_Store":
                    continue
                name = path[0:path.index(".")]
                print(name)
                df = pd.read_csv(os.path.join(args.raw_folder, path), delimiter=';')
                clean_df[name] = pd.to_numeric(df['Close'])
                clean_df[name].fillna(0, inplace=True)

            clean_df.reindex(index=clean_df.index[::-1]).to_csv(args.output + "_GNN_clean.csv", index=False)
            print("Processing Time: {:5.2f}s".format(time.time() - start_time))

        df = pd.read_csv(args.output + "_GNN_clean.csv")
        print(df.head())

    elif "SP500" in args.raw:
        if not os.path.isfile(args.output):
            start_time = time.time()
            df = pd.read_csv(args.raw + '_raw.csv')
            clean_df = pd.DataFrame()
            names = df['Name'].unique()

            for name in names:
                df_ = pd.DataFrame(df.loc[df['Name'] == name]['close'].values, columns=[name])
                if df_.shape[0] == 1259:
                    clean_df = pd.concat([clean_df, df_], axis=1)

            clean_df.to_csv(args.output + "_clean.csv", index=False)
            print("Processing Time: {:5.2f}s".format(time.time() - start_time))

        df = pd.read_csv(args.output + "_clean.csv")
        sample_df = df[['AAPL', 'AMZN', 'FB', 'GOOGL', "MSFT", "XRAY"]]
        corr = sample_df.corr()
        if args.plot:
            sn.set(font_scale=0.5)
            sn.heatmap(corr, annot=False, center=0, cmap='coolwarm', square=True)
            plt.savefig(os.path.join('img', 'SP500_corr.png'), dpi=300, bbox_inches='tight')

    elif "INVEST" in args.raw:
        if not os.path.isfile(args.output):
            start_time = time.time()
            df = pd.read_csv(args.raw + '_raw.csv', delimiter=";")
            clean_df = pd.DataFrame()
            names = df['Company'].unique()

            for name in names:
                df_ = pd.DataFrame(df.loc[df['Company'] == name]['Close'].values, columns=[name])
                clean_df = pd.concat([clean_df, df_], axis=1)

            print(clean_df.shape)
            clean_df.to_csv(args.output + "_clean.csv", index=False)
            print("Processing Time: {:5.2f}s".format(time.time() - start_time))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw', type=str, default='')
    parser.add_argument('--raw_folder', type=str, default='data/JSE')
    parser.add_argument('--source', type=str, default='SB')
    parser.add_argument('--output', type=str, default='data/JSE')
    parser.add_argument('--price', type=str, default='C')
    parser.add_argument('--plot', type=bool, default=False)
    parser.add_argument('--truncate', type=bool, default=True)
    args = parser.parse_args()
    clean()
