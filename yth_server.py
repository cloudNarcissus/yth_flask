from flask import Flask, Blueprint, jsonify
from flask_restful import reqparse, abort, Api, Resource

#yth_mysql = Blueprint('yth_mysql',__name__)
app = Flask(__name__)
api = Api(app)


# def error500(e):
#     return jsonify({
#         'message': repr(e)
#     }), 500
#
#
# api.handle_error = error500