from flask import Blueprint
from flask_restful import Api

api_bp_v1_0 = Blueprint("api_bp_v1_0", __name__)

api = Api(api_bp_v1_0, catch_all_404s=True)

from . import es_resource, mysql_resource
