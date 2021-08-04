import argparse
import json
import time

import invest.evaluation.validation as validation
from invest.networks.invest_recommendation import investment_recommendation
from invest.networks.quality_evaluation import quality_network
from invest.networks.value_evaluation import value_network
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
        for company in companies_jgind:
            if store.get_acceptable_stock(company):
                if investment_decision(store, company) == "Yes":
                    mask = (df['Date'] >= str(year) + '-01-01') & (
                            df['Date'] <= str(year) + '-12-31') & (df['Name'] == company)
                    df_year = df[mask]

                    investable_shares_jgind[str(year)].append(company)
                    prices_current_jgind[str(year)].append(df_year.iloc[-1]['Price'])
                    prices_initial_jgind[str(year)].append(df_year.iloc[0]['Price'])
                    share_betas_jgind[str(year)].append(df_year.iloc[-1]["ShareBeta"])

    for year in range(2015, 2018):
        print(year, "IP.JGIND", len(investable_shares_jgind[str(year)]), investable_shares_jgind[str(year)])

    validation.process_metrics(df_, prices_current_jgind, prices_initial_jgind, share_betas_jgind,
                               2015, 2018, "JGIND")
    validation.process_benchmark_metrics(2015, 2018, "JGIND")

    for year in range(2015, 2018):
        store = Store(df, companies, companies_jcsev, companies_jgind,
                      0.1, args.beta, year, args.extension)
        for company in companies_jcsev:
            if store.get_acceptable_stock(company):
                if investment_decision(store, company) == "Yes":
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

    validation.process_metrics(df_, prices_current_jcsev, prices_initial_jcsev, share_betas_jcsev,
                               2015, 2018, "JCSEV")
    validation.process_benchmark_metrics(2015, 2018, "JCSEV")
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    print("Experiment time taken: ""{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))


def investment_decision(store, company):
    pe_relative_market = store.get_pe_relative_market(company)
    pe_relative_sector = store.get_pe_relative_sector(company)
    forward_pe = store.get_forward_pe(company)

    roe_vs_coe = store.get_roe_vs_coe(company)
    relative_debt_equity = store.get_relative_debt_equity(company)
    cagr_vs_inflation = store.get_cagr_vs_inflation(company)
    systematic_risk = store.get_systematic_risk(company)

    value_decision = value_network(pe_relative_market, pe_relative_sector, forward_pe)
    quality_decision = quality_network(roe_vs_coe, relative_debt_equity, cagr_vs_inflation,
                                       systematic_risk, args.extension)
    if args.ablation and args.network == 'v':
        if value_decision in ["Cheap", "FairValue"]:
            return "Yes"
        else:
            return "No"
    if args.ablation and args.network == 'q':
        if quality_decision in ["High", "Medium"]:
            return "Yes"
        else:
            return "No"
    return investment_recommendation(value_decision, quality_decision)


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
    args = parser.parse_args()
    main()
