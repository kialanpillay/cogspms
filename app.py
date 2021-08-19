import argparse
import json
import time

import art
import numpy as np
import pandas as pd

import invest.evaluation.validation as validation
from invest.decision import investment_decision
from invest.prediction.main import future_share_price_performance
from invest.preprocessing.dataloader import load_data
from invest.preprocessing.simulation import simulate
from invest.store import Store

VERSION = 1.0


def main():
    companies_jcsev = json.load(open('data/jcsev.json'))['names']
    companies_jgind = json.load(open('data/jgind.json'))['names']
    companies = companies_jcsev + companies_jgind

    df_ = load_data()
    if args.noise:
        df = simulate(df_)
    else:
        df = df_

    prices_current_jgind = {}
    prices_current_jcsev = {}
    prices_initial_jgind = {}
    prices_initial_jcsev = {}
    share_betas_jgind = {}
    share_betas_jcsev = {}
    investable_shares_jgind = {}
    investable_shares_jcsev = {}

    start = time.time()

    for year in range(args.start, args.end):
        store = Store(df, companies, companies_jcsev, companies_jgind,
                      args.margin_of_safety, args.beta, year, args.extension)
        investable_shares_jgind[str(year)] = []
        prices_current_jgind[str(year)] = []
        prices_initial_jgind[str(year)] = []
        share_betas_jgind[str(year)] = []

        if args.gnn:
            df_future_performance = future_share_price_performance(year, horizon=args.horizon)
        else:
            df_future_performance = pd.DataFrame()
        for company in companies_jgind:
            if store.get_acceptable_stock(company):
                if not df_future_performance.empty:
                    future_performance = df_future_performance[company][0]
                else:
                    future_performance = None
                if investment_decision(store, company, future_performance, args.extension, args.ablation, args.network) \
                        == "Yes":
                    mask = (df_['Date'] >= str(year) + '-01-01') & (
                            df_['Date'] <= str(year) + '-12-31') & (df_['Name'] == company)
                    df_year = df_[mask]

                    investable_shares_jgind[str(year)].append(company)
                    prices_current_jgind[str(year)].append(df_year.iloc[args.holding_period]['Price'])
                    prices_initial_jgind[str(year)].append(df_year.iloc[0]['Price'])
                    share_betas_jgind[str(year)].append(df_year.iloc[args.holding_period]["ShareBeta"])

    print("\nJGIND {} - {}".format(args.start, args.end))
    print("-" * 50)
    print("\nInvestable Shares")
    for year in range(args.start, args.end):
        print(year, "IP.JGIND", len(investable_shares_jgind[str(year)]), investable_shares_jgind[str(year)])

    _, ip_cr_jgind, ip_aar_jgind, ip_tr_jgind, ip_sr_jgind = validation.process_metrics(df_,
                                                                                        prices_current_jgind,
                                                                                        prices_initial_jgind,
                                                                                        share_betas_jgind,
                                                                                        args.start, args.end, "JGIND")
    jgind_metrics_ = [ip_cr_jgind, ip_aar_jgind, ip_tr_jgind, ip_sr_jgind]
    if not args.noise:
        validation.process_benchmark_metrics(args.start, args.end, "JGIND", args.holding_period)

    for year in range(args.start, args.end):
        store = Store(df, companies, companies_jcsev, companies_jgind,
                      args.margin_of_safety, args.beta, year, args.extension)
        investable_shares_jcsev[str(year)] = []
        prices_current_jcsev[str(year)] = []
        prices_initial_jcsev[str(year)] = []
        share_betas_jcsev[str(year)] = []

        if args.gnn:
            df_future_performance = future_share_price_performance(year, horizon=args.horizon)
        else:
            df_future_performance = pd.DataFrame()
        for company in companies_jcsev:
            if store.get_acceptable_stock(company):
                if not df_future_performance.empty:
                    future_performance = df_future_performance[company][0]
                else:
                    future_performance = None
                if investment_decision(store, company, future_performance, args.extension, args.ablation, args.network) \
                        == "Yes":
                    mask = (df_['Date'] >= str(year) + '-01-01') & (
                            df_['Date'] <= str(year) + '-12-31') & (df['Name'] == company)
                    df_year = df_[mask]

                    investable_shares_jcsev[str(year)].append(company)
                    prices_current_jcsev[str(year)].append(df_year.iloc[args.holding_period]['Price'])
                    prices_initial_jcsev[str(year)].append(df_year.iloc[0]['Price'])
                    share_betas_jcsev[str(year)].append(df_year.iloc[args.holding_period]["ShareBeta"])

    end = time.time()

    print("-" * 50)
    print("\nJCSEV {} - {}".format(args.start, args.end))
    print("-" * 50)
    print("\nInvestable Shares")
    for year in range(args.start, args.end):
        print(year, "IP.JCSEV", len(investable_shares_jcsev[str(year)]), investable_shares_jcsev[str(year)])
    _, ip_cr_jcsev, ip_aar_jcsev, ip_tr_jcsev, ip_sr_jcsev = validation.process_metrics(df_,
                                                                                        prices_current_jcsev,
                                                                                        prices_initial_jcsev,
                                                                                        share_betas_jcsev,
                                                                                        args.start, args.end, "JCSEV")
    jcsev_metrics_ = [ip_cr_jcsev, ip_aar_jcsev, ip_tr_jcsev, ip_sr_jcsev]
    if not args.noise:
        validation.process_benchmark_metrics(args.start, args.end, "JCSEV", args.holding_period)

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
