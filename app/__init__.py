import os


from flask import Flask



print("app.init.py--%s"%__name__)

def register_blueprints(app):
    from app.api.v1_0 import api_bp_v1_0
    from app.api.v1_0 import api_bp_ls
    app.register_blueprint(api_bp_v1_0, url_prefix='/v1.0')
    app.register_blueprint(api_bp_ls, url_prefix='/ls/v1.0')

    # from app.api.v1_1 import api_bp_v1_1
    # app.register_blueprint(api_bp_v1_1, url_prefix='/v1.1')


def create_app():
    app = Flask(__name__)

    register_blueprints(app)

    return app

app = create_app()