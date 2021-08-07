import argparse
import json
import time
import numpy as np
import pandas as pd

import invest.evaluation.validation as validation
from invest.decision import investment_decision
from invest.prediction.main import future_share_price_performance
from invest.preprocessing.dataloader import load_data
from invest.preprocessing.simulation import simulate
from invest.store import Store


def main():
    companies_jcsev = json.load(open('data/jcsev.json'))['names']
    companies_jgind = json.load(open('data/jgind.json'))['names']
    companies = companies_jcsev + companies_jgind

    df_ = load_data()
    if args.noise:
        df = simulate(df_)
    else:
        df = df_

    prices_current_jgind = {"2017": [], "2016": [], "2015": []}
    prices_current_jcsev = {"2017": [], "2016": [], "2015": []}
    prices_initial_jgind = {"2017": [], "2016": [], "2015": []}
    prices_initial_jcsev = {"2017": [], "2016": [], "2015": []}
    share_betas_jgind = {"2017": [], "2016": [], "2015": []}
    share_betas_jcsev = {"2017": [], "2016": [], "2015": []}
    investable_shares_jgind = {"2017": [], "2016": [], "2015": []}
    investable_shares_jcsev = {"2017": [], "2016": [], "2015": []}

    start = time.time()

    for year in range(2015, 2018):
        store = Store(df, companies, companies_jcsev, companies_jgind,
                      args.margin_of_safety, args.beta, year, args.extension)
        if args.gnn:
            df_future_performance = future_share_price_performance(year)
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
                    mask = (df['Date'] >= str(year) + '-01-01') & (
                            df['Date'] <= str(year) + '-12-31') & (df['Name'] == company)
                    df_year = df[mask]

                    investable_shares_jgind[str(year)].append(company)
                    prices_current_jgind[str(year)].append(df_year.iloc[-1]['Price'])
                    prices_initial_jgind[str(year)].append(df_year.iloc[0]['Price'])
                    share_betas_jgind[str(year)].append(df_year.iloc[-1]["ShareBeta"])

    for year in range(2015, 2018):
        print(year, "IP.JGIND", len(investable_shares_jgind[str(year)]), investable_shares_jgind[str(year)])
    ratios_jgind = []
    ip_ar_jgind, ip_cr_jgind, ip_aar_jgind, ip_tr_jgind, ip_sr_jgind = validation.process_metrics(df_,
                                                                                                  prices_current_jgind,
                                                                                                  prices_initial_jgind,
                                                                                                  share_betas_jgind,
                                                                                                  2015, 2018, "JGIND")
    ratios_jgind.extend([ip_cr_jgind*100, ip_aar_jgind*100, ip_tr_jgind, ip_sr_jgind])

    validation.process_benchmark_metrics(2015, 2018, "JGIND")

    for year in range(2015, 2018):
        store = Store(df, companies, companies_jcsev, companies_jgind,
                      args.margin_of_safety, args.beta, year, args.extension)
        if args.gnn:
            df_future_performance = future_share_price_performance(year)
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
                    mask = (df['Date'] >= str(year) + '-01-01') & (
                            df['Date'] <= str(year) + '-12-31') & (df['Name'] == company)
                    df_year = df[mask]

                    investable_shares_jcsev[str(year)].append(company)
                    prices_current_jcsev[str(year)].append(df_year.iloc[-1]['Price'])
                    prices_initial_jcsev[str(year)].append(df_year.iloc[0]['Price'])
                    share_betas_jcsev[str(year)].append(df_year.iloc[-1]["ShareBeta"])

    end = time.time()

    for year in range(2015, 2018):
        print(year, "IP.JCSEV", len(investable_shares_jcsev[str(year)]), investable_shares_jcsev[str(year)])
    ratios_jcsev = []
    ip_ar_jcsev, ip_cr_jcsev, ip_aar_jcsev, ip_tr_jcsev, ip_sr_jcsev = validation.process_metrics(df_,
                                                                                                  prices_current_jcsev,
                                                                                                  prices_initial_jcsev,
                                                                                                  share_betas_jcsev,
                                                                                                  2015, 2018, "JCSEV")
    ratios_jcsev.extend([ip_cr_jcsev*100, ip_aar_jcsev*100, ip_tr_jcsev, ip_sr_jcsev])

    validation.process_benchmark_metrics(2015, 2018, "JCSEV")
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Experiment time taken: ""{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
    return ratios_jgind, ratios_jcsev  # return ratio list excluding aar for simulation


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
                                     epilog='Version 0.1')
    parser.add_argument("--margin_of_safety", type=float, default=0.10)
    parser.add_argument("--beta", type=float, default=1.00)
    parser.add_argument("--extension", type=str2bool, default=False)
    parser.add_argument("--noise", type=str2bool, default=False)
    parser.add_argument("--ablation", type=str2bool, default=False)
    parser.add_argument("--network", type=str, default='v')
    parser.add_argument("--gnn", type=str2bool, default=False)
    args = parser.parse_args()
    if args.noise:
        jgind_ratios = []
        jcsev_ratios = []
        for i in range(0, 10):
            ratios_jgind, ratios_jcsev = main()
            jgind_ratios.append(ratios_jgind)
            jcsev_ratios.append(ratios_jcsev)
        jgind_averaged_ratios = np.mean(jgind_ratios, axis=0)
        jcsev_averaged_ratios=np.mean(jcsev_ratios, axis=0)
        print(jgind_averaged_ratios)
        print(jcsev_averaged_ratios)








    else:
        main()
