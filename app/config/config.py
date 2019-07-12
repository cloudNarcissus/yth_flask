import os

current_dir = os.path.dirname(__file__)
app_dir = os.path.join(current_dir,"..")
root_dir = os.path.join(app_dir,"..")
import sys
sys.path.append(current_dir)
sys.path.append(app_dir)
sys.path.append(root_dir)
from app.utils.config_parser import ConfigParser
#from ..utils.config_parser import ConfigParser

_path = os.path.split(os.path.abspath(__file__))[0]
_cfg_file = os.path.join(_path, os.path.pardir, os.path.pardir, 'config.json')

_cfg_parser = ConfigParser(_cfg_file)


class Config(object):
    es_hosts = _cfg_parser.es_hosts
    mysql_host = _cfg_parser.mysql_host
    mysql_port = _cfg_parser.mysql_port
    mysql_db = _cfg_parser.mysql_db
    mysql_user = _cfg_parser.mysql_user
    mysql_pwd = _cfg_parser.mysql_pwd
    mysql_encode = _cfg_parser.mysql_encode
    hb_hosts = _cfg_parser.hbase_host
    mq_host = _cfg_parser.mq_host
    mq_port=_cfg_parser.mq_port
    mq_pwd=_cfg_parser.mq_pwd
    mq_user=_cfg_parser.mq_user


    begin_day = _cfg_parser.begin_day


    def init_config_beginday(self):
        from app.utils.common import today
        _cfg_parser.init_config_beginday(today())
        return today()


if __name__ == '__main__':
    cfg = Config()
    today = cfg.init_config_beginday()

    print("已设置统计数据起始日期为>%s"%today)
