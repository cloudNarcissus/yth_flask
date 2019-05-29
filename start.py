from flask import Flask
from yth_base import yth_base
from yth_mysql import yth_mysql
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
app.register_blueprint(yth_base)
app.register_blueprint(yth_mysql)
api = Api(app)


if __name__ == '__main__':

    app.run(host="0.0.0.0",port=10001)