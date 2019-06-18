# -*- coding:utf-8 -*-
#!/usr/bin/env python



from os.path import dirname, abspath, pardir, join
import string
import json

class Config(object):
    def __init__(self, filename):
        with open(filename,"r") as f:
            self.__json = json.load(f)

    def __parse_mq_hosts(self):
        hosts = self.__json['MQ']['hosts']
        host, port = hosts.split(':')
        return host, port

    def __parse_mq_credentials(self):
        creds = self.__json['MQ']['credentials']
        user, pwd = creds.split(':')
        return user, pwd

    def __parse_hbase_hosts(self):
        hosts = self.__json['HBASE']['hosts']
        host, port = hosts.split(':')
        return host, port

    def __parse_mysql_hosts(self):
        hosts = self.__json['MYSQL']['hosts']
        host, port = hosts.split(':')
        return host, port

    def __parse_mysql_credentials(self):
        creds = self.__json['MYSQL']['credentials']
        user, pwd = creds.split(':')
        return user, pwd

    def __parse_hive_hosts(self):
        hosts = self.__json['HIVE']['hosts']
        host, port = hosts.split(':')
        return host, port

    def __parse_hive_credentials(self):
        creds = self.__json['HIVE']['credentials']
        user, pwd = creds.split(':')
        return user, pwd

    def __parse_es_credentials(self):
        creds = self.__json['ElasticSearch']['credentials']
        user, pwd = creds.split(':')
        return user, pwd

    @property
    def mq_host(self):
        host, _ = self.__parse_mq_hosts()
        return host

    @property
    def mq_port(self):
        _, port = self.__parse_mq_hosts()
        return port

    @property
    def mq_user(self):
        user, _ = self.__parse_mq_credentials()
        return user

    @property
    def mq_pwd(self):
        _, pwd = self.__parse_mq_credentials()
        return pwd

    @property
    def hbase_host(self):
        host, _ = self.__parse_hbase_hosts()
        return host

    @property
    def hbase_port(self):
        _, port = self.__parse_hbase_hosts()
        return int(port)

    @property
    def mysql_host(self):
        host, _ = self.__parse_mysql_hosts()
        return host

    @property
    def mysql_port(self):
        _, port = self.__parse_mysql_hosts()
        return port

    @property
    def mysql_user(self):
        user, _ = self.__parse_mysql_credentials()
        return user

    @property
    def mysql_pwd(self):
        _, pwd = self.__parse_mysql_credentials()
        return pwd

    @property
    def mysql_db(self):
        return self.__json['MYSQL']['db']

    @property
    def mysql_encode(self):
        return self.__json['MYSQL']['encode']

    @property
    def hive_host(self):
        host, _ = self.__parse_hive_hosts()
        return host

    @property
    def hive_port(self):
        _, port = self.__parse_hive_hosts()
        return int(port)

    @property
    def hive_user(self):
        user, _ = self.__parse_hive_credentials()
        return user

    @property
    def hive_pwd(self):
        _, pwd = self.__parse_hive_credentials()
        return pwd

    @property
    def es_hosts(self):
        return  self.__json['ElasticSearch']['hosts']


    @property
    def es_user(self):
        user, _ = self.__parse_es_credentials()
        return user

    @property
    def es_pwd(self):
        _, pwd = self.__parse_es_credentials()
        return pwd

    @property
    def update_interval(self):
        return self.__json['UPDATE_INTERVAL']

if __name__ == '__main__':
    config = Config(abspath(join(dirname(__file__), pardir, 'config.json')))
    print (config.mq_host)
    print (config.mq_port)

    import os
    print (os.path.splitext(abspath(join(dirname(__file__), pardir, 'config')))[-1][1:])

    test_dict = {"1":"111"}
    print (test_dict["1"])
