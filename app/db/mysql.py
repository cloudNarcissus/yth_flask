import json
from ast import literal_eval

import pymysql

from app.config import Config
from app.utils.common import addHead,del_teshu_char
from app.db.mq import mq

from app.utils.log import logger


class MysqlConnect(object):
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

        # return json.dumps(data, ensure_ascii=False)
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
        # self.log.py.debug('test')
        cur = None
        conn, conn_err = self._connect('utf8')
        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:
            cur = conn.cursor()
            cur.execute('call pro_dict_query()')

            result = self.parse_result_to_json(cur)
            return True, result
        except Exception as e:
            err = self._get_exception_msg(e)
            return False, err

        finally:
            cur.close()
            conn.close()

    def fun_alarm_list_exists(self, md5):
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
            sql = '''select fun_alarm_list_exists('%s')''' % md5
            cur.execute(sql)
            result = cur.fetchall()
            return True, result[0][0]
        except Exception as e:
            err = self._get_exception_msg(e)
            return False, err
        finally:
            cur.close()
            conn.close()

    def fun_action_list_getLastTime(self, md5):
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
            sql = '''select fun_action_list_getLastTime('%s')''' % md5
            cur.execute(sql)
            result = cur.fetchall()
            return True, result[0][0]
        except Exception as e:
            err = self._get_exception_msg(e)
            return False, err
        finally:
            cur.close()
            conn.close()

    def pro_alarm_list_add(self, params):
        """
        加入告警
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
            sql = 'call pro_alarm_list_add'
            sql += ('(' + (''' '%s',''' * len(params))[:-1] + ')') % (
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
                params.get('__alarmType'),
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
    def pro_alarm_list_add_4api(self,params):
        """
        加入告警
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
            sql = 'call pro_alarm_list_add'
            sql += ('(' + (''' '%s',''' * len(params))[:-1] + ')') % (
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
                params.get('__alarmType'),
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
                params.get('alarmlevel_query') if params.get('alarmlevel_query') is not None else '',
                del_teshu_char(params.get('fulltext_query')) if params.get('fulltext_query') is not None else '',
                params.get('actiontype') if params.get('actiontype') is not None else '',
                params.get('__alarmSour', 0),
                params.get('cz_status', 0),
                params.get('_interested', 0),
                params.get('__alarmType', 0),
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
    def pro_alarm_list_left(self, params):
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
                params.get('alarmlevel_query') if params.get('alarmlevel_query') is not None else '',
                params.get('fulltext_query') if params.get('fulltext_query') is not None else '',
                params.get('actiontype') if params.get('actiontype') is not None else '',
                params.get('__alarmType',0),
                params.get('__alarmSour', 0),
                params.get('_interested', 0)
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
    def pro_alarm_list_cz(self, params):
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

    @addHead()
    def pro_alarm_list_interested(self, params):
        """
        告警清单加入关注
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
            sql = 'call pro_alarm_list_interested("%s",%s)' % (params.get('__md5'), params.get('_interested'))

            cur.execute(sql)
            conn.commit()
            return True, 'update interested ok'
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()

    def pro_action_list_add(self, params):
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
                params.get('__unit'),
                params.get('__connectTime'),

                params.get('website_info_name'),
                params.get('account'),
                params.get('url'),
                params.get('ip'),
                params.get('smac'),
                params.get('sport'),
                params.get('__unitaddr'),
                params.get('__contact'),

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
            sql = '''call pro_action_list_query('%s')''' % params['__md5']
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
            return result[0].get('err'), result[0].get('msg'),
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
        :param 
        :return: 
        """
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = 'call pro_event_list_query'
            # 构造(%s,%s,...)
            sql += ('(' + (''' "%s",''' * len(params))[:-1] + ')') % (
                params.get('begin_day'),
                params.get('end_day'),
                params.get('event_status', 0),
                params.get('event_miji') if params.get('event_miji') is not None else '',
                params.get('event_type') if params.get('event_type') is not None else '',
                del_teshu_char(params.get('fulltext_query')) if params.get('fulltext_query') is not None else '',
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
    def pro_event_list_edit(self, params):
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = '''call pro_event_list_edit'''
            sql += ('(' + (''' "%s",''' * len(params))[:-1] + ')') % (
                params.get('event_id'),
                params.get('event_name'),
                params.get('event_type'),
                params.get('event_miji'),
                params.get('event_status'),
                params.get('remark'),
                params.get('add_user')
            )
            cur.execute(sql)
            conn.commit()
            result = self.parse_result_to_json(cur)
            return result[0].get('err'), result[0].get('msg'),
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()

    @addHead()
    def pro_event_list_drop(self, params):
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = '''call pro_event_list_drop'''
            sql += ('(' + (''' "%s",''' * len(params))[:-1] + ')') % (
                params.get('event_id')
            )
            cur.execute(sql)
            conn.commit()
            result = self.parse_result_to_json(cur)
            return result[0].get('err'), result[0].get('msg'),
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()

    @addHead()
    def pro_event_list_create_event_id(self):
        """
        获取event_id
        :return: 
        """
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = 'call pro_event_list_create_event_id()'
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
    def pro_cfg_keyword_add(self, params):
        """
        添加关键字
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
            sql = '''call pro_cfg_keyword_add'''
            sql += r'''('%s',%s,%s,"%s","%s","%s")''' % (
                params.get('keyword'),
                params.get('keylevel'),
                params.get('enabled'),
                params.get('remark'),
                params.get('add_user'),
                params.get('keytype')
            )
            cur.execute(sql)
            conn.commit()
            result = self.parse_result_to_json(cur)

            err = result[0].get('err')
            if err:  # 如果成功要发送mq消息
                mq.send_msg({"action": __name__})
            return err, result[0].get('msg')


        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()

    @addHead()
    def pro_cfg_keyword_batchadd(self, params):
        """
        批量添加关键字
        :param params: [{},{}]
        :return: err:true/false  msg:文字信息
        """
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:
            rows = params.get('keywords', [])

            cur = conn.cursor()
            success_num = 0  # 成功条数
            for keywordRow in rows:
                keyword = literal_eval(keywordRow).get('key')
                # keyword = literal_eval(keywordRow)
                sql = '''call pro_cfg_keyword_add'''
                sql += '''('%s',%s,%s,"%s","%s","%s")''' % (
                    keyword.get('keyword'),
                    keyword.get('keylevel'),
                    keyword.get('enabled'),
                    keyword.get('remark'),
                    keyword.get('add_user'),
                    keyword.get('keytype')
                )
                cur.execute(sql)
                conn.commit()
                result = self.parse_result_to_json(cur)
                if int(result[0].get('err')):
                    success_num += 1

            if success_num > 0:  # 如果成功要发送mq消息
                mq.send_msg({"action": __name__})

            return True, "成功添加:%d条数据" % success_num
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()

    @addHead()
    def pro_cfg_keyword_query(self, params):
        """
        查询事件清单
        :param 
        :return: 
        """
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = 'call pro_cfg_keyword_query'
            # 构造(%s,%s,...)
            sql += ('(' + (''' "%s",''' * len(params))[:-1] + ')') % (
                params.get('begin_day'),
                params.get('end_day'),
                params.get('keylevel', 0),
                params.get('enabled') if params.get('enabled') is not None else None,
                del_teshu_char(params.get('keyword')) if params.get('keyword') is not None else '',
                params.get('last_keylevel', 0),
                params.get('last_auid', 0),
                params.get('page_count', 0),
                params.get('order_by'),
                params.get('keytype'),
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
    def pro_cfg_keyword_edit(self, params):
        """
        更新关键字
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
            sql = '''call pro_cfg_keyword_edit'''
            sql += '''(%s,'%s',%s,%s,"%s","%s","%s")''' % (
                params.get('auid'),
                params.get('keyword'),
                params.get('keylevel'),
                params.get('enabled'),
                params.get('remark'),
                params.get('add_user'),
                params.get('keytype')
            )
            cur.execute(sql)
            conn.commit()
            result = self.parse_result_to_json(cur)

            err = result[0].get('err')
            if err:  # 如果成功要发送mq消息
                mq.send_msg({"action": __name__})

            return err, result[0].get('msg')
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()

    @addHead()
    def pro_cfg_keyword_edit_valid(self,params):
        """
        更新关键字的有效性
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
            sql = '''call pro_cfg_keyword_edit_valid'''
            sql += '''(%d,%d)''' % (
                params.get('auid'),
                params.get('valid')
            )
            cur.execute(sql)
            conn.commit()
            result = self.parse_result_to_json(cur)

            err = result[0].get('err')
            return err, result[0].get('msg')
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()


    @addHead()
    def pro_cfg_keyword_drop(self, params):
        """
        删除关键字
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
            sql = '''call pro_cfg_keyword_delete'''
            sql += '''(%s)''' % (
                params.get('auid')
            )
            cur.execute(sql)
            conn.commit()
            result = self.parse_result_to_json(cur)

            err = result[0].get('err')
            if err:  # 如果成功要发送mq消息
                mq.send_msg({"action": __name__})

            return err, result[0].get('msg')
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()

    @addHead()
    def pro_platform_edit(self, params):
        """
        #编辑平台的简称、别名
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
            sql = '''call pro_platform_edit(%d,"%s","%s","%s")'''%(
                params.get('platformid'),
                params.get('name'),
                params.get('nicname'),
                params.get('simname'),
            )
            cur.execute(sql)
            conn.commit()
            result = self.parse_result_to_json(cur)

            err = result[0].get('err')

            return err, result[0].get('msg')
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()

    @addHead()
    def pro_platform_query(self, params):
        """
        #查询平台的简称、别名
        :param params: 一堆参数
        :return: 
        """
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = '''call pro_platform_query()'''
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            return True,result
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
    def pro_tj_alarm_list_weigui(self, params):
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
    def pro_tj_alarm_list_level(self, params):
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
    def pro_tj_action_list_actiontype(self, params):
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

    # 5. 统计告警类型alarmtype
    def pro_tj_action_list_alarmtype(self, params):
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:

            cur = conn.cursor()
            sql = 'call pro_tj_action_list_alarmtype'
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
    def pro_tj_alarm_list_center(self, params):
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

        result1 = self.pro_tj_action_list_alarmtype(params)
        if result1[0]:
            result["alarmtype"] = result1[1]
        else:
            result["alarmtype"] = "error"

        return True, result

    # ------------------- 首页的统计 ---------------------

    def tj_frontpage_alarm_list(self, today, yesterday, monday, firstdayofmonth, diff_days, begin_day,end_day):
        """
        
        :param today: 
        :param yesterday: 
        :param monday: 
        :param firstdayofmonth: 
        :param diff_days: 系统安装日期到今天的相差天数
        :param begin_day: 用户传入的起始日期
        :param end_day: 用户传入的结束日期
        :return: 
        """
        cur = None
        conn, conn_err = self._connect('utf8')

        if conn is None:
            err = self.handle_connect_err(conn_err)
            return False, err

        try:
            cur = conn.cursor()

            summary = {
                "平台数":4,
                "告警量": {
                    "今日": 0,
                    "昨日": 0,
                    "本周": 0,
                    "本月": 0,
                    "日均": 0,
                    "峰值": 0
                },
                "处置量": {
                    "今日": 0,
                    "昨日": 0,
                    "本周": 0,
                    "本月": 0,
                    "日均": 0,
                    "峰值": 0
                },
                "违规量": {
                    "今日": 0,
                    "昨日": 0,
                    "本周": 0,
                    "本月": 0,
                    "日均": 0,
                    "峰值": 0
                }
            }

            alarm_ana={
                "告警量": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0
                },
                "违规量": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0
                },
                "处置量": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0
                }
            }

            # ------------------- 全部

            # 1. today
            sql = '''call tj_frontpage_alarm_list('%s','%s','')''' % (today, today)
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_today = int(result[0]['count_'])
            summary["告警量"]['今日'] = alarm_today

            # 2. yesterday
            sql = '''call tj_frontpage_alarm_list('%s','%s','')''' % (yesterday, yesterday)
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_yesterday = int(result[0]['count_'])
            summary["告警量"]['昨日'] = alarm_yesterday

            # 3. this week
            sql = '''call tj_frontpage_alarm_list('%s','%s','')''' % (monday, today)
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_week = int(result[0]['count_'])
            summary["告警量"]['本周'] = alarm_week

            # 4. this month
            sql = '''call tj_frontpage_alarm_list('%s','%s','')''' % (firstdayofmonth, today)
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_month = int(result[0]['count_'])
            summary["告警量"]['本月'] = alarm_month

            # 5. total -- 用来计算dayavg
            sql = '''call tj_frontpage_alarm_list('1970-01-01','1970-01-01','')'''
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_total = int(result[0]['count_'])
            alarm_day_avg = alarm_total / diff_days
            summary["告警量"]['日均'] = alarm_day_avg

            # 6. 日峰值
            sql = '''call tj_frontpage_alarm_list_day('')'''
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_day_max = int(result[0]['count_'])
            summary["告警量"]['峰值'] = alarm_day_max

            # 7. 自定义事件
            sql = '''call tj_frontpage_alarm_list('%s','%s','')'''%(begin_day,end_day)
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            all_cz = int(result[0]['count_'])
            summary["告警量"]['自定'] = all_cz


            # ------------------- 处置量

            # 2.1 处置量today
            sql = '''call tj_frontpage_alarm_list('%s','%s','cz')''' % (today, today)
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_today = int(result[0]['count_'])
            summary["处置量"]['今日'] = alarm_today

            # 2.2 yesterday
            sql = '''call tj_frontpage_alarm_list('%s','%s','cz')''' % (yesterday, yesterday)
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_yesterday = int(result[0]['count_'])
            summary["处置量"]['昨日'] = alarm_yesterday

            # 2.3 this week
            sql = '''call tj_frontpage_alarm_list('%s','%s','cz')''' % (monday, today)
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_week = int(result[0]['count_'])
            summary["处置量"]['本周'] = alarm_week

            # 2.4 this month
            sql = '''call tj_frontpage_alarm_list('%s','%s','cz')''' % (firstdayofmonth, today)
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_month = int(result[0]['count_'])
            summary["处置量"]['本月'] = alarm_month

            # 2.5 total -- 用来计算dayavg
            sql = '''call tj_frontpage_alarm_list('1970-01-01','1970-01-01','cz')'''
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_total = int(result[0]['count_'])
            alarm_day_avg = alarm_total / diff_days
            summary["处置量"]['日均'] = alarm_day_avg

            # 2.6. 日峰值
            sql = '''call tj_frontpage_alarm_list_day('cz')'''
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_day_max = int(result[0]['count_'])
            summary["处置量"]['峰值'] = alarm_day_max

            # 2.7. z自定义
            sql = '''call tj_frontpage_alarm_list('%s','%s','cz')''' % (begin_day, end_day)
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            cz_self = int(result[0]['count_'])
            summary["处置量"]['自定'] = cz_self


            # ------------------- 违规量

            # 3.1 处置量today
            sql = '''call tj_frontpage_alarm_list('%s','%s','wg')''' % (today, today)
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_today = int(result[0]['count_'])
            summary["违规量"]['今日'] = alarm_today

            # 3.2 yesterday
            sql = '''call tj_frontpage_alarm_list('%s','%s','wg')''' % (yesterday, yesterday)
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_yesterday = int(result[0]['count_'])
            summary["违规量"]['昨日'] = alarm_yesterday

            # 3.3 this week
            sql = '''call tj_frontpage_alarm_list('%s','%s','wg')''' % (monday, today)
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_week = int(result[0]['count_'])
            summary["违规量"]['本周'] = alarm_week

            # 3.4 this month
            sql = '''call tj_frontpage_alarm_list('%s','%s','wg')''' % (firstdayofmonth, today)
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_month = int(result[0]['count_'])
            summary["违规量"]['本月'] = alarm_month

            # 3.5 total -- 用来计算dayavg
            sql = '''call tj_frontpage_alarm_list('1970-01-01','1970-01-01','wg')'''
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_total = int(result[0]['count_'])
            alarm_day_avg = alarm_total / diff_days
            summary["违规量"]['日均'] = alarm_day_avg

            # 3.6. 日峰值
            sql = '''call tj_frontpage_alarm_list_day('wg')'''
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_day_max = int(result[0]['count_'])
            summary["违规量"]['峰值'] = alarm_day_max

            # 3.7. z自定义
            sql = '''call tj_frontpage_alarm_list('%s','%s','wg')''' % (begin_day, end_day)
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            wg_self = int(result[0]['count_'])
            summary["违规量"]['自定'] = wg_self


            # -----  按时间段，按平台分组

            sql = '''call tj_frontpage_alarm_platform('%s','%s')'''%(begin_day,end_day)
            cur.execute(sql)
            result = self.parse_result_to_json(cur)
            alarm_ana['告警量']["1"] = int(result[0]['count_p1_all'])
            alarm_ana['告警量']["2"] = int(result[0]['count_p2_all'])
            alarm_ana['告警量']["3"] = int(result[0]['count_p3_all'])
            alarm_ana['告警量']["4"] = int(result[0]['count_p4_all'])

            alarm_ana['违规量']["1"] = int(result[0]['count_p1_wg'])
            alarm_ana['违规量']["2"] = int(result[0]['count_p2_wg'])
            alarm_ana['违规量']["3"] = int(result[0]['count_p3_wg'])
            alarm_ana['违规量']["4"] = int(result[0]['count_p4_wg'])

            alarm_ana['处置量']["1"] = int(result[0]['count_p1_cz'])
            alarm_ana['处置量']["2"] = int(result[0]['count_p2_cz'])
            alarm_ana['处置量']["3"] = int(result[0]['count_p3_cz'])
            alarm_ana['处置量']["4"] = int(result[0]['count_p4_cz'])


            #--- 雷达图
            sql = '''call tj_frontpage_alarm_sour('%s','%s')''' % (begin_day, end_day)
            cur.execute(sql)
            leida_my = self.parse_result_to_json(cur)



            return True, summary ,alarm_ana,leida_my
        except Exception as e:
            err = self._get_exception_msg(e)
            logger.error(sql)
            logger.error(err)
            return False, err
        finally:
            cur.close()
            conn.close()




mc = MysqlConnect()

#
if __name__ == '__main__':
    mc = MysqlConnect()
    mc.tj_frontpage_alarm_list('2019-07-10', '2019-07-09', '2019-07-08', '2019-07-01',10)


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
