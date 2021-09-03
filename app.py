import argparse
import time

import art
import numpy as np

from invest.decision import investment_portfolio
from invest.preprocessing.dataloader import load_data

VERSION = 1.0


def main():
    start = time.time()
    df_ = load_data()
    jgind_portfolio = investment_portfolio(df_, args, "JGIND", True)
    jcsev_portfolio = investment_portfolio(df_, args, "JCSEV", True)
    end = time.time()

    jgind_metrics_ = list(jgind_portfolio["ip"].values())[2::]
    jcsev_metrics_ = list(jcsev_portfolio["ip"].values())[2::]

    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("\nExperiment Time: ""{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
    return jgind_metrics_, jcsev_metrics_


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Intelligent system for automated share evaluation',
                                     epilog='Version 1.0')
    parser.add_argument("--start", type=int, default=2015)
    parser.add_argument("--end", type=int, default=2018)
    parser.add_argument("--margin_of_safety", type=float, default=0.10)
    parser.add_argument("--beta", type=float, default=1.00)
    parser.add_argument("--extension", type=str2bool, default=False)
    parser.add_argument("--noise", type=str2bool, default=False)
    parser.add_argument("--ablation", type=str2bool, default=False)
    parser.add_argument("--network", type=str, default='v')
    parser.add_argument("--gnn", type=str2bool, default=False)
    parser.add_argument("--holding_period", type=int, default=-1)
    parser.add_argument("--horizon", type=int, default=10)
    args = parser.parse_args()

    print(art.text2art("INVEST"))
    print("Insaaf Dhansay & Kialan Pillay")
    print("© University of Cape Town 2021")
    print("Version {}".format(VERSION))
    print("=" * 50)

    if args.noise:
        jgind_metrics = []
        jcsev_metrics = []
        for i in range(0, 10):
            ratios_jgind, ratios_jcsev = main()
            jgind_metrics.append(ratios_jgind)
            jcsev_metrics.append(ratios_jcsev)
        jgind_averaged_metrics = np.mean(jgind_metrics, axis=0)
        jcsev_averaged_metrics = np.mean(jcsev_metrics, axis=0)

        for i in range(0, 2):
            jgind_averaged_metrics[i] *= 100
            jcsev_averaged_metrics[i] *= 100
        print("JGIND", [round(v, 2) for v in jgind_averaged_metrics])
        print("JCSEV", [round(v, 2) for v in jcsev_averaged_metrics])
    else:
        main()
