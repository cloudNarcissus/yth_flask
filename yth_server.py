from flask import Flask, Blueprint, jsonify
from flask_restful import reqparse, abort, Api, Resource

#yth_mysql = Blueprint('yth_mysql',__name__)
app = Flask(__name__)
api = Api(app)


def error_handler(e):
    print(repr(e))
    return jsonify({
        'message': e.description
    }), e.code


app.register_error_handler(500, error_handler)
app.register_error_handler(404, error_handler)
