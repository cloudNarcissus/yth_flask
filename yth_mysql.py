import config
import pymysql


# from flask import Flask,Blueprint
# from flask_restful import reqparse, abort, Api, Resource
#
# #yth_mysql = Blueprint('yth_mysql',__name__)
# app = Flask(__name__)
# api = Api(app)
from add_head import addHead
from yth_server import api, Resource, reqparse

import logging
import logging.handlers
import os
if 'nt' != os.name:
    _log_path = './my_logger.log'
else:
    _path = os.path.dirname(__file__)
    _log_path = os.path.join(_path, 'my_logger.log')

logger = logging.getLogger('yth_mysql')
logger.setLevel(logging.INFO)
fhtime = logging.handlers.TimedRotatingFileHandler(_log_path, when='D', interval=1, backupCount=10)
fhtime.setFormatter(logging.Formatter("%(asctime)s-%(levelname)s-%(message)s"))
logger.addHandler(fhtime)

config_path = 'config.json'

class mysqlConnect(object):
    conf = None

    def __init__(self, config_path,logger):
        self.conf = config.Config(config_path)
        self.log = logger

    def _connect(self, encoding='utf8'):
        """
        连接数据库
        :param encoding:
        :return:
        """
        conn = None
        conn_err = None
        try:
            conn = pymysql.connect(
                # connect_timeout=int(self.conf.timeout),
                host=self.conf.mysql_host,
                port=int(self.conf.mysql_port),
                user=self.conf.mysql_user,
                password=self.conf.mysql_pwd,
                database=self.conf.mysql_db,
                charset=self.conf.mysql_encode
            )
            return conn, conn_err
        except pymysql.Error as e:
            conn_err = repr(e)
            # log.error(conn_err)
            return conn, conn_err

    def _get_exception_msg(self, e):

        if len(e.args) < 2:
            err = 'unknown db error'
            return err
        msg = e.args[1]
        idx = msg.find('DB-Lib')
        if idx != -1:
            msg = msg[0:idx]
        err = msg
        return err

    def handle_connect_err(self, conn_err):
        msg = conn_err
        print('无法连接到数据库: {err}'.format(err=msg))
        return msg

    # 把查询出来的数据搞成  json: [{}] 结构  # 认为只有一个结果集
    def parse_result_to_json(self, cur):
        data = []

        if cur.description is not None:
            columns = [None if desc is None or not desc or len(desc) == 1 else desc[0] for desc in
                       cur.description]
            for row in cur:
                temp = dict()
                for i in range(len(columns)):
                    val = row[i]
                    # ignore None value, otherwise you'll get a 'None' string
                    if val is not None:
                        val = str(val)
                    key = columns[i]
                    temp[key] = val
                data.append(temp)

        #return json.dumps(data, ensure_ascii=False)
        return data

    @addHead()
    def pro_dict_query(self):
        """
        查询字典
        :param proc:
        :param args:
        :param output_args:
        :return:err,json
        """
        cur = None
        conn, conn_err = self._connect('utf8')
        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False,err

        try:
            cur = conn.cursor()
            cur.execute('call pro_dict_query()')

            result = self.parse_result_to_json(cur)
            return True,result
        except Exception as e:
            err = self._get_exception_msg(e)
            return False,err

        finally:
            cur.close()
            conn.close()

    def fun_alarm_list_exists(self,__md5):
        """
        查询alarm_list是否存在某个md5的条目
        :return:bool
        """
        cur = None
        conn, conn_err = self._connect('utf8')
        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:
            cur = conn.cursor()
            sql = '''select fun_alarm_list_exists('%s')'''%__md5
            cur.execute(sql)
            result = cur.fetchall()
            return True, result
        except Exception as e:
            err = self._get_exception_msg(e)
            return False, err
        finally:
            cur.close()
            conn.close()

    def fun_action_list_getLastTime(self,__md5):
        """
        获取action_list上次最大时间
        :param __md5:
        :return: varchar
        """
        cur = None
        conn, conn_err = self._connect('utf8')
        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:
            cur = conn.cursor()
            sql = '''select fun_action_list_getLastTime('%s')''' % __md5
            cur.execute(sql)
            result = cur.fetchall()
            return True, result
        except Exception as e:
            err = self._get_exception_msg(e)
            return False, err
        finally:
            cur.close()
            conn.close()

    def pro_alarm_list_add(self,params_dict):
        """
        加入告警
        :param params_dict: 参数字典
        :return:
        """
        cur = None
        conn, conn_err = self._connect('utf8')


        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False,err

        try:

            cur = conn.cursor()
            sql = 'call pro_alarm_list_add'
            sql += ('(' + (''' "%s",''' * len(params_dict))[:-1] + ')')%(
                params_dict.get('yth_fileana_id'),
                params_dict.get('__md5'),
                params_dict.get('__connectTime'),
                params_dict.get('__title'),
                params_dict.get('__alarmLevel'),
                params_dict.get('__alarmSour'),
                params_dict.get('summary'),
                params_dict.get('__alarmKey'),
                params_dict.get('__document'),
                params_dict.get('__industry'),
                params_dict.get('__security'),
                params_dict.get('__ips'),
             )
            # 构造(%s,%s,...)
            cur.execute(sql)
            conn.commit()
            return True, '插入成功'
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()

    def pro_action_list_add(self,params_dict):
        """
        加入告警行为表（子表）
        :param params_dict:
        :return:
        """
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = 'call pro_action_list_add'
            sql += ('(' + (''' "%s",''' * len(params_dict))[:-1] + ')') % (
                params_dict.get('yth_base_id'),
                params_dict.get('__md5'),
                params_dict.get('platform'),
                params_dict.get('actiontype'),
                params_dict.get('redPoint'),
                params_dict.get('unit'),
                params_dict.get('__connectTime'),
            )
            # 构造(%s,%s,...)
            cur.execute(sql)
            conn.commit()
            return True, '插入成功'
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()



@api.resource('/v1.0/dict/')
class getDict(Resource):
    '''
    获取字典
    '''

    def get(self):
        mc = mysqlConnect(config_path,logger)
        return mc.pro_dict_query()



#
if __name__ == '__main__':
    mc = mysqlConnect(config_path, logger)
    print(mc.pro_dict_query())


    # params_dict = {}
    # params_dict['yth_fileana_id'] = '10000'
    # params_dict['__md5'] = 'md5-1'
    # params_dict['__connectTime'] = '2019-05-31'
    # params_dict['__title'] ='这是个标题'
    # params_dict['__alarmLevel']=5
    # params_dict['__alarmSour']=2
    # params_dict['unit']='王安科技'
    # params_dict['summary']='''XXXXXXXXXX发生时间，涉密终端以XXXip地址通过网卡：xxx Adapter 直连互联网；本机地址：192.168.0.100 网管：192.168.0.1'''
    # params_dict['__alarmKey']=''
    # params_dict['__document']=''
    # params_dict['__industry']=''
    # params_dict['__security']=''
    # params_dict['__ips']='192.168.0.1,192.168.0.2'
    # print(mc.pro_alarm_list_add(params_dict))

