import os
import time
from functools import reduce
import consul

from app.utils.log import logger
from app.utils.config_parser import ConfigParser


class ConsulConn(object):
    def __init__(self, host=None, port=None):
        params = {}
        if host is not None:
            params['host'] = host
        if port is not None:
            params['port'] = port
        self.cs = consul.Consul(**params)

    def get_kv_config(self,key_prefix="yda",key=None):

        if key is None:
            return reduce(lambda x, y: {**x, **y}, [{i['Key']: i['Value'].decode("utf-8")} for i in
                                                    self.cs.kv.get(key=key_prefix, recurse=True)[1]])
        else:
            return reduce(lambda x, y: {**x, **y}, [{i['Key']: i['Value'].decode("utf-8")} for i in
                                                    self.cs.kv.get(key=key_prefix, recurse=True)[1]]).get(key)



while True:
    try:
        consulconn = ConsulConn(host="192.168.10.136")
        break
    except Exception as e:
        i = i + 1
        if i == 5:
            logger.error('ConsulConn Error,程序退出')
            exit(-1)
        time.sleep(30)

keys = consulconn.get_kv_config(key_prefix="yda")
Config = ConfigParser(keys)



