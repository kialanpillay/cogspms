import json
import logging

from flask import jsonify, make_response
from flask_restx import Resource, Namespace, reqparse, fields

from invest.decision import investment_portfolio
from invest.preprocessing.dataloader import load_data

df = load_data()

namespace = Namespace('invest')

logging.basicConfig(format="%(asctime)s - [%(levelname)s] %(message)s",
                    datefmt="%d-%b-%y %H:%M:%S",
                    level=logging.INFO)

invest_resource_model = namespace.model("INVEST Resource", {
    "start": fields.Integer(required=True),
    "end": fields.Integer(required=True),
    "margin": fields.Float(required=False),
    "beta": fields.Float(required=False)
})

metrics_model = namespace.model("IP Metrics", {
    "shares": fields.List(fields.String(required=True)),
    "annualReturns": fields.List(fields.Float(required=True)),
    "compoundReturn": fields.Float(required=True),
    "averageAnnualReturn": fields.Float(required=True),
    "treynor": fields.Float(required=True),
    "sharpe": fields.Float(required=True),
})

benchmark_metrics_model = namespace.model("Benchmark Metrics", {
    "annualReturns": fields.List(fields.Float(required=True)),
    "compoundReturn": fields.Float(required=True),
    "averageAnnualReturn": fields.Float(required=True),
    "treynor": fields.Float(required=True),
    "sharpe": fields.Float(required=True),
})

jgind_model = namespace.model("JGIND", {
    "ip": fields.Nested(metrics_model),
    "benchmark": fields.Nested(benchmark_metrics_model)
})

jcsev_model = namespace.model("JCSEV", {
    "ip": fields.Nested(metrics_model),
    "benchmark": fields.Nested(benchmark_metrics_model)
})

portfolio_model = namespace.model("Portfolio", {
    "jgind": fields.Nested(jgind_model),
    "jcsev": fields.Nested(jcsev_model),
})

invest_response_model = namespace.model("INVEST Response", {
    "portfolio": fields.Nested(portfolio_model)
})


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    else:
        return False


parser = reqparse.RequestParser()
parser.add_argument('start', type=int)
parser.add_argument('end', type=int)
parser.add_argument('margin', type=float, default=0.1)
parser.add_argument('beta', type=float, default=0.2)
parser.add_argument("extension", type=str2bool, default=False)
parser.add_argument("noise", type=str2bool, default=False)
parser.add_argument("ablation", type=str2bool, default=False)
parser.add_argument("network", type=str, default='v')
parser.add_argument("gnn", type=str2bool, default=False)
parser.add_argument("period", type=int, default=-1)
parser.add_argument("horizon", type=int, default=10)

companies_jcsev = json.load(open('data/jcsev.json'))['names']
companies_jgind = json.load(open('data/jgind.json'))['names']
companies = companies_jcsev + companies_jgind
companies_dict = {"JCSEV": companies_jcsev, "JGIND": companies_jgind}


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

    @namespace.expect(invest_resource_model)
    @namespace.response(200, "Success", invest_response_model)
    @namespace.response(400, "Bad Request")
    def get(self):
        args = parser.parse_args()
        args['margin_of_safety'] = args['margin']
        args['holding_period'] = args['period']
        if args['start'] >= args['end']:
            response = jsonify(
                {
                    'code': 400,
                    'status': "Bad Request",
                }
            )
        else:
            jgind = investment_portfolio(df, args, "JGIND")
            jcsev = investment_portfolio(df, args, "JCSEV")
            response = jsonify(
                {
                    'code': 200,
                    'status': "OK",
                    'portfolio': {
                        'jgind': jgind,
                        'jcsev': jcsev
                    },
                }
            )
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
