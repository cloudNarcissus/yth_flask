# from flask_restful import reqparse, abort, Api, Resource
#
# app = Flask(__name__)
# api = Api(app)

from yth_server import app


if __name__ == '__main__':

    app.run(host="0.0.0.0",port=10086, debug=True)