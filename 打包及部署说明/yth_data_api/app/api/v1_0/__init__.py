from flask import Blueprint
from flask_restful import Api

api_bp_v1_0 = Blueprint("api_bp_v1_0", __name__)
api_bp_ls = Blueprint("api_bp_ls", __name__)

api = Api(api_bp_v1_0, catch_all_404s=True)
api_ls = Api(api_bp_ls, catch_all_404s=True)


#from app.api.v1_0.yth import es_resource, hbase_resource, mysql_resource
from . import yth
from . import ls