import os
import time
from functools import reduce

import consul



from app.utils.log import logger




class ConsulConn(object):
    def __init__(self,host =None ,port =None):
        params = {}
        if host is not None:
            params['host'] = host
        if port is not None:
            params['port'] = port
            self.consul = consul.Consul(**params)

    def get_kv_config(self, key):
        index, data = self.consul.kv.get(key)

        print(reduce(lambda x,y:{**x,**y},[ {i['Key']:i['Value'].decode("utf-8")} for i in c.kv.get(key="common",recurse=True)[1] ]) )


        print(c.kv.get("common.mongodb.host")[1].len)

        raise Exception("Invalid level!")('Required kv config: <%s> which is not configured!' % key)
        return data['Value']



class Config(object):
    # 供模块调用的配置项及其他一些常量
    while True:
        try:
            consulconn = ConsulConn()
        except Exception as e:
            i = i + 1
            if i == 5:
                log.error('程序退出')
            exit(-1)
            time.sleep(30)


    es_hosts = consulconn.es_hosts
    mysql_host = _cfg_parser.mysql_host
    mysql_port = _cfg_parser.mysql_port
    mysql_db = _cfg_parser.mysql_db
    mysql_user = _cfg_parser.mysql_user
    mysql_pwd = _cfg_parser.mysql_pwd
    mysql_encode = _cfg_parser.mysql_encode
    hb_hosts = _cfg_parser.hbase_host
    hb_port = _cfg_parser.hbase_port
    mq_host = _cfg_parser.mq_host
    mq_port = _cfg_parser.mq_port
    mq_pwd = _cfg_parser.mq_pwd
    mq_user = _cfg_parser.mq_user

    myls_host = _cfg_parser.myls_host
    myls_port = _cfg_parser.myls_port
    myls_db = _cfg_parser.myls_db
    myls_user = _cfg_parser.myls_user
    myls_pwd = _cfg_parser.myls_pwd
    myls_encode = _cfg_parser.myls_encode

    begin_day = _cfg_parser.begin_day

    RESTFUL_HOST = getattr(c_cfg, 'restful_host')
    RESTFUL_PORT = getattr(c_cfg, 'restful_port')
    MONGODB_HOSTS = '%s:%s' % (getattr(c_cfg, 'mongodb_host'), getattr(c_cfg,
    'mongodb_port'))
    MONGODB_DB_NAME = 'DataCenter'
    MQ_HOST = getattr(c_cfg, 'mq_host')
    MQ_PORT = int(getattr(c_cfg, 'mq_port'))
    MQ_USERNAME = getattr(c_cfg, 'mq_username')
    MQ_PASSWORD = getattr(c_cfg, 'mq_password')