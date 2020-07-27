# -*- coding:utf-8 -*-
# !/usr/bin/env python

from os.path import dirname, abspath, pardir, join



class ConfigParser(object):
    def __init__(self, config_keys):
        self.__json = config_keys

    # def init_config_beginday(self, today):
    #     self.__json['yda.begin_day'] = today
    #     with open(self.filename, "w") as fp:
    #         fp.write(json.dumps(self.__json, indent=4))


    def __parse_mq_hosts(self):
        hosts = self.__json['yda.mq.hosts']
        host, port = hosts.split(':')
        return host, port

    def __parse_mq_credentials(self):
        creds = self.__json['yda.mq.credentials']
        user, pwd = creds.split(':')
        return user, pwd

    def __parse_hbase_hosts(self):
        hosts = self.__json['yda.hbase.hosts']
        host, port = hosts.split(':')
        return host, port

    def __parse_mysql_hosts(self):
        hosts = self.__json['yda.mysql.hosts']
        host, port = hosts.split(':')
        return host, port

    def __parse_mysql_credentials(self):
        creds = self.__json['yda.mysql.credentials']
        user, pwd = creds.split(':')
        return user, pwd

    def __parse_hive_hosts(self):
        hosts = self.__json['yda.hive.hosts']
        host, port = hosts.split(':')
        return host, port

    def __parse_hive_credentials(self):
        creds = self.__json['yda.hive.credentials']
        user, pwd = creds.split(':')
        return user, pwd

    def __parse_es_credentials(self):
        creds = self.__json['yda.elasticsearch.credentials']
        user, pwd = creds.split(':')
        return user, pwd

    def __parse_myls_hosts(self):
        hosts = self.__json['yda.myls.hosts']
        host, port = hosts.split(':')
        return host, port

    def __parse_myls_credentials(self):
        creds = self.__json['yda.myls.credentials']
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
    def hb_hosts(self):
        host, _ = self.__parse_hbase_hosts()
        return host

    @property
    def hb_port(self):
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
        return self.__json['yda.mysql.db']

    @property
    def mysql_encode(self):
        return self.__json['yda.mysql.encode']

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
        return self.__json['yda.elasticsearch.hosts']

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
        return self.__json['yda.update_interval']

    @property
    def begin_day(self):
        return self.__json['yda.begin_day']

    @property
    def myls_host(self):
        host, _ = self.__parse_myls_hosts()
        return host

    @property
    def myls_port(self):
        _, port = self.__parse_myls_hosts()
        return port

    @property
    def myls_user(self):
        user, _ = self.__parse_myls_credentials()
        return user

    @property
    def myls_pwd(self):
        _, pwd = self.__parse_myls_credentials()
        return pwd

    @property
    def myls_db(self):
        return self.__json['yda.myls.db']

    @property
    def myls_encode(self):
        return self.__json['yda.myls.encode']


if __name__ == '__main__':
    config = ConfigParser(abspath(join(dirname(__file__), pardir, 'config.json')))
    print(config.mq_host)
    print(config.mq_port)

    import os

    print(os.path.splitext(abspath(join(dirname(__file__), pardir, 'config')))[-1][1:])

    test_dict = {"1": "111"}
    print(test_dict["1"])
