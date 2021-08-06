from flask_restx import Api

from .invest import namespace as invest

api = Api(
    title='INVEST API',
    version='1.0',
)
api.add_namespace(invest)
