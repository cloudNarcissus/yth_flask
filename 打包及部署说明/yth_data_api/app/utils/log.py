import os
import logging.handlers
if 'nt' != os.name:
    _log_path = './yth_logger.log'
else:
    _path = os.path.dirname(__file__)
    _log_path = os.path.join(_path, os.path.pardir, 'my_logger.log')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fhtime = logging.handlers.TimedRotatingFileHandler(_log_path, when='D', interval=1, backupCount=10)
fhtime.setFormatter(logging.Formatter("%(asctime)s-%(levelname)s-%(message)s"))
logger.addHandler(fhtime)
