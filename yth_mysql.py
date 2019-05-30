import config
import pymysql
import json
# from flask import Flask,Blueprint
# from flask_restful import reqparse, abort, Api, Resource
#
# #yth_mysql = Blueprint('yth_mysql',__name__)
# app = Flask(__name__)
# api = Api(app)

from yth_server import api, Resource, reqparse

import logging
import logging.handlers
import os
if 'nt' != os.name:
    _log_path = './es_logger.log'
else:
    _path = os.path.dirname(__file__)
    _log_path = os.path.join(_path, os.path.pardir, os.path.pardir, 'logs')

logger = logging.getLogger('yth_mysql')
logger.setLevel(logging.INFO)
fhtime = logging.handlers.TimedRotatingFileHandler(_log_path, when='D', interval=1, backupCount=10)
fhtime.setFormatter(logging.Formatter("%(asctime)s-%(levelname)s-%(message)s"))
logger.addHandler(fhtime)

config_path = 'config.json'

class mysqlConnect(object):
    conf = None

    def __init__(self, config_path,log):
        self.conf = config.Config(config_path)
        self.log = log

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

        return json.dumps(data, ensure_ascii=False)

    def pro_dict_query(self, args=None, output_args=None):
        """
        查询字典
        :param proc:
        :param args:
        :param output_args:
        :return:
        """
        cur = None
        conn, conn_err = self._connect('utf8')
        if conn is None:
            err = self.handle_connect_err(conn_err)
            return err,'conn is None!'

        has_output = output_args is not None
        try:
            cur = conn.cursor()
            cur.execute('call pro_dict_query()')
            # 这句需要写到最后  不然前一句不能取不到输出参数
            conn.commit()
            if has_output:
                # sql.insert(0, self._build_output_param(output_args))
                cur.execute(self._build_output_query(output_args))

            result = self.parse_result_to_json(cur)
            return 0,result
        except Exception as e:
            err = self._get_exception_msg(e)
            return err,'execute error！'

        finally:
            cur.close()
            conn.close()


#@yth_mysql.route('/yth_mysql')
@api.resource('/v1.0/dict/')
class getDict(Resource):
    '''
    获取字典
    '''

    def get(self):
        mc = mysqlConnect(config_path,logger)
        result = mc.pro_dict_query()
        if result[0] == 0:
            return result[1]
        else:
            logger.error(result[1])
            return result[1]


#
# if __name__ == '__main__':
#     app.run(host="0.0.0.0",port=10001)