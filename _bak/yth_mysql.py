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
    _log_path = './my_logger.log.py'
else:
    _path = os.path.dirname(__file__)
    _log_path = os.path.join(_path, 'my_logger.log.py')

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
            # log.py.error(conn_err)
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
            return True, result[0][0]
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
            return True, result[0][0]
        except Exception as e:
            err = self._get_exception_msg(e)
            return False, err
        finally:
            cur.close()
            conn.close()

    def pro_alarm_list_add(self,params):
        """
        加入告警
        :param params: 参数字典
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
            sql += ('(' + (''' "%s",''' * len(params))[:-1] + ')')%(
                params.get('yth_fileana_id'),
                params.get('__md5'),
                params.get('__connectTime'),
                params.get('__title'),
                params.get('__alarmLevel'),
                params.get('__alarmSour'),
                params.get('summary'),
                params.get('__alarmKey'),
                params.get('__document'),
                params.get('__industry'),
                params.get('__security'),
                params.get('__ips'),
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

    @addHead()
    def pro_alarm_list_query(self, params):
        """
        查询告警清单
        :param params: 参数字典
        :return: 
        """
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = 'call pro_alarm_list_query'
            # 构造(%s,%s,...)
            sql += ('(' + (''' "%s",''' * len(params))[:-1] + ')') % (
                params.get('begin_day'),
                params.get('end_day'),
                params.get('alarmlevel_query'),
                params.get('fulltext_query'),
                params.get('actiontype'),
                params.get('__alarmSour'),
                params.get('cz_status'),
                params.get('_interested'),
                params.get('orderby'),
                params.get('page_capa'),
                params.get('page_num'),
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

    @addHead()
    def pro_alarm_list_left(self,params):
        """
        查询左侧统计切换区
        :param params: 
        :return: 
        """
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = 'call pro_alarm_list_left'
            # 构造(%s,%s,...)
            sql += ('(' + (''' "%s",''' * len(params))[:-1] + ')') % (
                params.get('begin_day'),
                params.get('end_day'),
                params.get('alarmlevel_query'),
                params.get('fulltext_query'),
                params.get('platform'),
                params.get('__alarmSour')
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

    @addHead()
    def pro_alarm_list_cz(self,params):
        """
        加入告警行为表（子表）
        :param params:
        :return:
        """
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = 'call pro_alarm_list_cz'
            sql += ('(' + (''' "%s",''' * len(params))[:-1] + ')') % (
                params.get('cz_user'),
                params.get('__md5'),
                params.get('cz_status'),
                params.get('cz_summary'),
                params.get('cz_detail'),
            )
            # 构造(%s,%s,...)
            cur.execute(sql)
            conn.commit()
            return True, 'update ok'
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()

    def pro_action_list_add(self,params):
        """
        加入告警行为表（子表）
        :param params:
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
            sql += ('(' + (''' "%s",''' * len(params))[:-1] + ')') % (
                params.get('yth_base_id'),
                params.get('__md5'),
                params.get('platform'),
                params.get('actiontype'),
                params.get('redPoint'),
                params.get('unit'),
                params.get('__connectTime'),
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

    @addHead()
    def pro_action_list_query(self, params):
        """
        查询某个告警清单的行为追踪
        :param __md5: 
        :return: 
        """
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = '''call pro_action_list_query('%s')'''%params['__md5']
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

    @addHead()
    def pro_cz_list_query(self, params):
        """
        查询处置历史清单
        :param __md5: 
        :return: 
        """
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = '''call pro_cz_list_query('%s')''' % params['__md5']
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

    @addHead()
    def pro_event_list_add(self, params):
        """
        插入事件列表,同时将关联的行为插入
        :param params: 一堆参数
        :return: err:true/false  msg:文字信息
        """
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = '''call pro_event_list_add'''
            sql += ('(' + (''' "%s",''' * len(params))[:-1] + ')') % (
                params.get('__md5'),
                params.get('event_id'),
                params.get('event_name'),
                params.get('event_type'),
                params.get('event_miji'),
                params.get('event_status'),
                params.get('content'),
                params.get('remark'),
                params.get('add_user'),
                params.get('report')
            )
            cur.execute(sql)
            conn.commit()
            result = self.parse_result_to_json(cur)
            return result[0].get('err'),result[0].get('msg'),
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
        conn.close()

    @addHead()
    def pro_event_list_query(self, params):
        """
        查询事件清单
        :param __md5: 
        :return: 
        """
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = '''call pro_event_list_query('%s')''' % params['__md5']
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


    # ------------------- 告警中心的统计 ---------------------

    # 1. 统计处置数量
    def pro_tj_alarm_list_cz(self, params):
        """
        统计处置告警数
        :param params: 参数字典
        :return: 
        """
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = 'call pro_tj_alarm_list_cz'
            # 构造(%s,%s,...)
            sql += ('(' + (''' "%s",''' * len(params))[:-1] + ')') % (
                params.get('begin_day'),
                params.get('end_day'),
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

    # 2. 统计违规条目（违规的alarm数目）以及红点（未读的action）
    def pro_tj_alarm_list_weigui(self,params):
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = 'call pro_tj_alarm_list_weigui'
            # 构造(%s,%s,...)
            sql += ('(' + (''' "%s",''' * len(params))[:-1] + ')') % (
                params.get('begin_day'),
                params.get('end_day'),
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

    # 3. 统计告警等级
    def pro_tj_alarm_list_level(self,params):
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = 'call pro_tj_alarm_list_level'
            # 构造(%s,%s,...)
            sql += ('(' + (''' "%s",''' * len(params))[:-1] + ')') % (
                params.get('begin_day'),
                params.get('end_day'),
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

    # 4. 统计行为类型actiontype
    def pro_tj_action_list_actiontype(self,params):
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = 'call pro_tj_action_list_actiontype'
            # 构造(%s,%s,...)
            sql += ('(' + (''' "%s",''' * len(params))[:-1] + ')') % (
                params.get('begin_day'),
                params.get('end_day'),
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

    # 综合：将几个统计结果集都集成起来
    @addHead()
    def pro_tj_alarm_list_center(self,params):
        result = {}

        result1 = self.pro_tj_alarm_list_cz(params)
        if result1[0]:
            result["cz"] = result1[1]
        else:
            result["cz"] = "error"

        result1 = self.pro_tj_alarm_list_weigui(params)
        if result1[0]:
            result["weigui"] = result1[1]
        else:
            result["weigui"] = "error"

        result1 = self.pro_tj_alarm_list_level(params)
        if result1[0]:
            result["level"] = result1[1]
        else:
            result["level"] = "error"

        result1 = self.pro_tj_action_list_actiontype(params)
        if result1[0]:
            result["platform"] = result1[1]
        else:
            result["platform"] = "error"

        return True,result



@api.resource('/v1.0/dict/')
class Dict(Resource):
    '''
    获取字典
    '''
    def get(self):
        mc = mysqlConnect(config_path,logger)
        return mc.pro_dict_query()

@api.resource('/v1.0/alarmlist/cz/')
class AlarmListcz(Resource):
    '''
    处置告警清单
    '''

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cz_user', type=str, required=True) #处置用户
        parser.add_argument('cz_status', type=str,required=True) # NO: 未处置  PASS：处置为正常  JIMI: 处置为机密   MIMI: 处置为秘密    JUEMI：处置为绝密
        parser.add_argument('__md5', type=str,required=True)
        parser.add_argument('cz_summary', type=str, required=True) #涉密摘要 （处置摘要），改为正常的话要值为空
        parser.add_argument('cz_detail', type=str, required=True) #ui自行组织字段，用于在历史记录里面显示的

        mc = mysqlConnect(config_path, logger)
        params = parser.parse_args(strict=True)
        return mc.pro_alarm_list_cz(params)


@api.resource('/v1.0/alarmlist/left/')
class AlarmListLeft(Resource):
    '''
    查询告警清单左侧栏的统计切换区
    '''

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('begin_day', type=str, required=True)
        parser.add_argument('end_day', type=str, required=True)
        parser.add_argument('alarmlevel_query', type=str)
        parser.add_argument('fulltext_query', type=str)
        parser.add_argument('platform', type=int)
        parser.add_argument('__alarmSour', type=int)

        mc = mysqlConnect(config_path, logger)
        params = parser.parse_args(strict=True)
        return mc.pro_alarm_list_left(params)


@api.resource('/v1.0/alarmlist/tj/')
class AlarmListtj(Resource):
    '''
    统计处置数量
    '''
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('begin_day', type=str, required=True)
        parser.add_argument('end_day', type=str, required=True)
        mc = mysqlConnect(config_path, logger)
        params = parser.parse_args(strict=True)
        return mc.pro_tj_alarm_list_center(params)


@api.resource('/v1.0/alarmlist/')
class AlarmList(Resource):
    '''
    查询告警清单
    '''

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('begin_day', type=str, required=True)
        parser.add_argument('end_day', type=str, required=True)
        parser.add_argument('alarmlevel_query', type=str)
        parser.add_argument('fulltext_query', type=str)
        parser.add_argument('actiontype', type=str)
        parser.add_argument('__alarmSour', type=int)
        parser.add_argument('cz_status', type=int)
        parser.add_argument('_interested', type=int)
        parser.add_argument('orderby', type=str, required=True)
        parser.add_argument('page_capa', type=int, required=True)
        parser.add_argument('page_num', type=int, required=True)

        mc = mysqlConnect(config_path, logger)
        params = parser.parse_args(strict=True)
        return mc.pro_alarm_list_query(params)


@api.resource('/v1.0/actionlist/')
class ActionList(Resource):
    '''
    查询行为追踪
    '''
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('__md5', type=str, required=True)

        mc = mysqlConnect(config_path, logger)
        params = parser.parse_args(strict=True)
        return mc.pro_action_list_query(params)

@api.resource('/v1.0/czlist/')
class CzList(Resource):
    '''
    查询处置历史清单
    '''

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('__md5', type=str, required=True)

        mc = mysqlConnect(config_path, logger)
        params = parser.parse_args(strict=True)
        return mc.pro_cz_list_query(params)

@api.resource('/v1.0//eventlist/add')
class EventListAdd(Resource):
    '''
    插入事件列表,同时将关联的行为插入
    '''

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('event_id', type=str, required=True)#事件编号
        parser.add_argument('event_name', type=str, required=True)#事件名
        parser.add_argument('event_type', type=int, required=True)# 字典里有
        #
        # 1       违规外联
        # 2       互联网传输泄密
        # 3       网络攻击窃密
        # 4       违规存储 / 处理涉密信息
        #
        parser.add_argument('event_miji', type=str, required=True)#字典里有
        parser.add_argument('event_status', type=int, required=True) #字典里有 1.待处理 2.不移交  3移交未反馈  4移交已反馈
        parser.add_argument('content', type=str, required=True) # 内容 显示 文件名 或者 违规外联描述
        parser.add_argument('remark', type=str, required=True)# 备注
        parser.add_argument('add_user', type=str, required=True)  # 添加者
        parser.add_argument('report', type=str, required=True)  # 这是ui自行组织的json，用于打印报告

        mc = mysqlConnect(config_path, logger)
        params = parser.parse_args(strict=True)
        return mc.pro_event_list_add(params)



#
if __name__ == '__main__':
    mc = mysqlConnect(config_path, logger)
    print(mc.pro_dict_query())


    # params = {}
    # params['yth_fileana_id'] = '10000'
    # params['__md5'] = 'md5-1'
    # params['__connectTime'] = '2019-05-31'
    # params['__title'] ='这是个标题'
    # params['__alarmLevel']=5
    # params['__alarmSour']=2
    # params['unit']='王安科技'
    # params['summary']='''XXXXXXXXXX发生时间，涉密终端以XXXip地址通过网卡：xxx Adapter 直连互联网；本机地址：192.168.0.100 网管：192.168.0.1'''
    # params['__alarmKey']=''
    # params['__document']=''
    # params['__industry']=''
    # params['__security']=''
    # params['__ips']='192.168.0.1,192.168.0.2'
    # print(mc.pro_alarm_list_add(params))

