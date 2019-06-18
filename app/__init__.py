import os
import logging
import logging.handlers

from flask import Flask

if 'nt' != os.name:
    _log_path = '../my_logger.log'
else:
    _path = os.path.dirname(__file__)
    _log_path = os.path.join(_path, os.path.pardir, 'my_logger.log')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fhtime = logging.handlers.TimedRotatingFileHandler(_log_path, when='D', interval=1, backupCount=10)
fhtime.setFormatter(logging.Formatter("%(asctime)s-%(levelname)s-%(message)s"))
logger.addHandler(fhtime)


def register_blueprints(app):
    from app.api.v1_0 import api_bp_v1_0
    app.register_blueprint(api_bp_v1_0, url_prefix='/v1.0')

    # from app.api.v1_1 import api_bp_v1_1
    # app.register_blueprint(api_bp_v1_1, url_prefix='/v1.1')


def create_app():
    app = Flask(__name__)

    register_blueprints(app)

    return app

app = create_app()