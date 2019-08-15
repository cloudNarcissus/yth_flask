import os
import consul



class ConsulKVConfig(object):
    def __init__(self,host =None ,port =None):
        params = {}
        if host is not None:
            params['host'] = host
        if port is not None:
            params['port'] = port
        self.consul = consul.Consul(**params)


