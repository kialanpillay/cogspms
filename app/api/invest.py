import json
import logging

from flask import jsonify, make_response
from flask_restx import Resource, Namespace, reqparse, fields

from invest.evaluation import validation
from invest.networks.invest_recommendation import investment_recommendation
from invest.networks.quality_evaluation import quality_network
from invest.networks.value_evaluation import value_network
from invest.preprocessing.dataloader import load_data
from invest.store import Store

namespace = Namespace('invest')

logging.basicConfig(format="%(asctime)s - [%(levelname)s] %(message)s",
                    datefmt="%d-%b-%y %H:%M:%S",
                    level=logging.INFO)

invest_resource = namespace.model("invest", {
    "start": fields.Integer(required=True),
    "end": fields.Integer(required=True),
    "margin": fields.Float(required=False),
    "beta": fields.Float(required=False)
})

parser = reqparse.RequestParser()
parser.add_argument('start', type=int)
parser.add_argument('end', type=int)
parser.add_argument('margin', type=float, default=0.1)
parser.add_argument('beta', type=float, default=0.2)

companies_jcsev = json.load(open('data/jcsev.json'))['names']
companies_jgind = json.load(open('data/jgind.json'))['names']
companies = companies_jcsev + companies_jgind
companies_dict = {"JCSEV": companies_jcsev, "JGIND": companies_jgind}

df = load_data()


def investment_decision(store, company, future_performance=None):
    pe_relative_market = store.get_pe_relative_market(company)
    pe_relative_sector = store.get_pe_relative_sector(company)
    forward_pe = store.get_forward_pe(company)

    roe_vs_coe = store.get_roe_vs_coe(company)
    relative_debt_equity = store.get_relative_debt_equity(company)
    cagr_vs_inflation = store.get_cagr_vs_inflation(company)
    systematic_risk = store.get_systematic_risk(company)

    value_decision = value_network(pe_relative_market, pe_relative_sector, forward_pe, future_performance)
    quality_decision = quality_network(roe_vs_coe, relative_debt_equity, cagr_vs_inflation,
                                       systematic_risk)
    return investment_recommendation(value_decision, quality_decision)


def investment_portfolio(data, index_code):
    start_year = data['start']
    end_year = data['end']
    margin_of_safety = data['margin']
    beta = data['beta']
    prices = {}
    prices_ = {}
    betas = {}
    investable_shares = {}

    for year in range(start_year, end_year):
        store = Store(df, companies, companies_jcsev, companies_jgind,
                      margin_of_safety, beta, year, False)
        investable_shares[str(year)] = []
        prices[str(year)] = []
        prices_[str(year)] = []
        betas[str(year)] = []
        for company in companies_dict[index_code]:
            if store.get_acceptable_stock(company):
                if investment_decision(store, company) == "Yes":
                    mask = (df['Date'] >= str(year) + '-01-01') & (
                            df['Date'] <= str(year) + '-12-31') & (df['Name'] == company)
                    df_year = df[mask]

                    investable_shares[str(year)].append(company)
                    prices[str(year)].append(df_year.iloc[0]['Price'])
                    prices_[str(year)].append(df_year.iloc[-1]['Price'])
                    betas[str(year)].append(df_year.iloc[-1]["ShareBeta"])

    ip_ar, ip_cr, ip_aar, ip_treynor, ip_sharpe = validation.process_metrics(df,
                                                                             prices_,
                                                                             prices,
                                                                             betas,
                                                                             start_year, end_year,
                                                                             index_code)
    benchmark_ar, benchmark_cr, benchmark_aar, benchmark_treynor, benchmark_sharpe = \
        validation.process_benchmark_metrics(start_year, end_year, index_code)

    portfolio = {
        "shares": investable_shares,
        "annualReturns": ip_ar,
        "compoundReturn": ip_cr,
        "averageAnnualReturn": ip_aar,
        "treynor": ip_treynor,
        "sharpe": ip_sharpe,
        "benchmarkAnnualReturns": benchmark_ar,
        "benchmarkCompoundReturn": benchmark_cr,
        "benchmarkAverageAnnualReturn": benchmark_aar,
        "benchmarkTreynor": benchmark_treynor,
        "benchmarkSharpe": benchmark_sharpe,
    }
    return portfolio


@namespace.route("/")
@namespace.header("Access-Control-Allow-Origin", "*")
class Invest(Resource):

    @namespace.response(200, "Success", headers={"Access-Control-Allow-Origin": "*",
                                                 "Access-Control-Allow-Headers": "*",
                                                 "Access-Control-Allow-Methods": "GET, OPTIONS"})
    def options(self):
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    @namespace.expect(invest_resource)
    @namespace.response(200, "Success")
    @namespace.response(400, "Bad Request")
    def get(self):
        args = parser.parse_args()
        if args['start'] >= args['end']:
            response = jsonify(
                {
                    'code': 400,
                    'status': "Bad Request",
                }
            )
        else:
            jgind = investment_portfolio(args, "JGIND")
            jcsev = investment_portfolio(args, "JCSEV")
            response = jsonify(
                {
                    'code': 200,
                    'status': "OK",
                    'ip': {
                        'jgind': jgind,
                        'jcsev': jcsev
                    },
                }
            )
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
