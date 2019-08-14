import logging

import pymysql

from app.utils.common import addHead
from app.config import Config

logger = logging.getLogger(__name__)



class MylsConnect(object):
    def __init__(self):
        self.conf = Config
        self.log = logger

    def _connect(self, encoding='utf8mb4'):
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
                host=self.conf.myls_host,
                port=int(self.conf.myls_port),
                user=self.conf.myls_user,
                password=self.conf.myls_pwd,
                database=self.conf.myls_db,
                charset=self.conf.myls_encode
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

        # return json.dumps(data, ensure_ascii=False)
        return data

    # 线程作业：告警数据抽取
    def job_import_ls_alarm(self):
        """
        告警数据抽取
        :param params: 参数字典
        :return: 
        """
        cur = None
        conn, conn_err = self._connect('utf8mb4')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err
        sql = ''
        try:

            cur = conn.cursor()
            sql = 'call job_import_ls_alarm()'

            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            return True, result
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()




    # -------- 查询告警处置统计 -----------------------#

    # 1. 查询告警类型分布
    @addHead()
    def pro_alarm_alarmtype(self, params):
        """
        统计处置告警数
        :param params: 参数字典
        :return: 
        """
        cur = None
        conn, conn_err = self._connect('utf8mb4')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err
        sql = ''
        try:

            cur = conn.cursor()
            sql = 'call pro_alarm_alarmtype(%d,%d,"%s","%s","%s")'%(
                params.get('begin_day'),
                params.get('end_day'),

                params.get('province') if params.get('province') is not None else '',
                params.get('city') if params.get('city') is not None else '',
                params.get('district') if params.get('district') is not None else '',

            )

            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            return True, result
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()


    # 2. 查询告警级别分布 及 处置情况 （有3个图）
    @addHead()
    def pro_alarm_alarmtypelevel(self, params):
        """
        查询告警级别分布 及 处置情况 （有3个图）
        :param params: 参数字典
        :return: 
        """
        cur = None
        conn, conn_err = self._connect('utf8mb4')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err
        sql = ''
        try:

            cur = conn.cursor()
            sql = 'call pro_alarm_alarmtype_alarmlevel(%d,%d,"%s","%s","%s")'%(
                params.get('begin_day'),
                params.get('end_day'),

                params.get('province') if params.get('province') is not None else '',
                params.get('city') if params.get('city') is not None else '',
                params.get('district') if params.get('district') is not None else '',

            )

            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            return True, result
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()


    # 3. 查询处置率变化趋势（以天展示，没有数据的那天就没有记录）
    @addHead()
    def pro_alarm_alarmcztrend(self, params):
        """
        处置趋势 ， 所谓趋势，就是按天给出数据（没有数据的天，不出现！）
        :param params: 参数字典
        :return: 
        """
        cur = None
        conn, conn_err = self._connect('utf8mb4')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err
        sql = ''
        try:

            cur = conn.cursor()
            sql = 'call pro_alarm_cz_trend(%d,%d,"%s","%s","%s")' % (
                params.get('begin_day'),
                params.get('end_day'),

                params.get('province') if params.get('province') is not None else '',
                params.get('city') if params.get('city') is not None else '',
                params.get('district') if params.get('district') is not None else '',

            )

            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            return True, result
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()


    # 4. 处置结果密级分布
    @addHead()
    def pro_alarm_alarmczstatus(self, params):
        """
        处置结果密级分布
        :param params: 参数字典
        :return: 
        """
        cur = None
        conn, conn_err = self._connect('utf8mb4')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err
        sql = ''
        try:

            cur = conn.cursor()
            sql = 'call pro_alarm_cz_status(%d,%d,"%s","%s","%s")' % (
                params.get('begin_day'),
                params.get('end_day'),

                params.get('province') if params.get('province') is not None else '',
                params.get('city') if params.get('city') is not None else '',
                params.get('district') if params.get('district') is not None else '',

            )

            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            return True, result
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()


    # 5. 告警地图
    def pro_alarm_map(self, params):
        """
        查询地图，分为两级（省和市）
        :param params: 参数字典
        :return: 
        """
        cur = None
        conn, conn_err = self._connect('utf8mb4')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err
        sql = ''
        try:

            cur = conn.cursor()
            sql = 'call pro_alarm_map(%d,%d,"%s","%s","%s")' % (
                params.get('begin_day'),
                params.get('end_day'),

                params.get('province') if params.get('province') is not None else '',
                params.get('city') if params.get('city') is not None else '',
                params.get('district') if params.get('district') is not None else '',

            )

            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            return True, result
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()







mc = MylsConnect()