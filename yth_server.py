from flask import Flask,Blueprint
from flask_restful import reqparse, abort, Api, Resource

#yth_mysql = Blueprint('yth_mysql',__name__)
app = Flask(__name__)
api = Api(app)


@app.errorhandler(500)
def xx(e):
    return str(e),500