from flask_restful import Resource, reqparse

from app.api.v1_0 import api
from app.db.mysql import mc


@api.resource('/dict/')
class Dict(Resource):
    '''
    获取字典
    '''

    def get(self):
        return mc.pro_dict_query()


@api.resource('/alarmlist/cz/')
class AlarmListcz(Resource):
    '''
    处置告警清单
    '''

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cz_user', type=str, required=True)  # 处置用户
        parser.add_argument('cz_status', type=str,
                            required=True,choices=['NO', 'PASS','JIMI','MIMI','JUEMI','NEIBU'])  # NO: 未处置  PASS：处置为正常  JIMI: 处置为机密   MIMI: 处置为秘密    JUEMI：处置为绝密
        parser.add_argument('__md5', type=str, required=True)
        parser.add_argument('cz_summary', type=str, required=True)  # 涉密摘要 （处置摘要），改为正常的话要值为空
        parser.add_argument('cz_detail', type=str, required=True)  # ui自行组织字段，用于在历史记录里面显示的

        params = parser.parse_args(strict=True)
        return mc.pro_alarm_list_cz(params)


@api.resource('/alarmlist/left/')
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
        parser.add_argument('actiontype', type=str)
        parser.add_argument('__alarmType', type=int)
        parser.add_argument('__alarmSour', type=int)
        parser.add_argument('_interested', type=int)
        parser.add_argument('__security', type=str)
        parser.add_argument('__alarmKey', type=str)

        params = parser.parse_args(strict=True)
        return mc.pro_alarm_list_left(params)


@api.resource('/alarmlist/tj/')
class AlarmListtj(Resource):
    '''
    统计处置数量
    '''

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('begin_day', type=str, required=True)
        parser.add_argument('end_day', type=str, required=True)

        params = parser.parse_args(strict=True)
        return mc.pro_tj_alarm_list_center(params)


@api.resource('/alarmlist/')
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
        parser.add_argument('__alarmType', type=int)
        parser.add_argument('orderby', type=str, required=True)
        parser.add_argument('page_capa', type=int, required=True)
        parser.add_argument('page_num', type=int, required=True)

        parser.add_argument('__security', type=str)
        parser.add_argument('__alarmKey', type=str)

        params = parser.parse_args(strict=True)
        return mc.pro_alarm_list_query(params)


@api.resource('/alarmlist/interested/')
class AlarmListInterested(Resource):
    '''
    关注告警清单
    '''

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('__md5', type=str, required=True)
        parser.add_argument('_interested', type=int, required=True)
        params = parser.parse_args(strict=True)
        return mc.pro_alarm_list_interested(params)



@api.resource('/actionlist/')
class ActionList(Resource):
    '''
    查询行为追踪
    '''

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('__md5', type=str, required=True)

        params = parser.parse_args(strict=True)
        return mc.pro_action_list_query(params)


@api.resource('/czlist/')
class CzList(Resource):
    '''
    查询处置历史清单
    '''

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('__md5', type=str, required=True)

        params = parser.parse_args(strict=True)
        return mc.pro_cz_list_query(params)


@api.resource('/eventlist/')
class EventList(Resource):
    '''
    插入事件列表,同时将关联的行为插入
    '''

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('__md5', type=str, required=True)  # 告警的md5
        parser.add_argument('event_id', type=str, required=True)  # 事件编号
        parser.add_argument('event_name', type=str, required=True)  # 事件名
        parser.add_argument('event_type', type=int, required=True)  # 字典里有
        #
        # 1       违规外联
        # 2       互联网传输泄密
        # 3       网络攻击窃密
        # 4       违规存储 / 处理涉密信息
        #
        parser.add_argument('event_miji', type=str, required=True)  # 字典里有
        parser.add_argument('event_status', type=int, required=True)  # 字典里有 1.待处理 2.不移交  3移交未反馈  4移交已反馈
        parser.add_argument('content', type=str, required=True)  # 内容 显示 文件名 或者 违规外联描述
        parser.add_argument('remark', type=str)  # 备注
        parser.add_argument('add_user', type=str, required=True)  # 添加者
        parser.add_argument('report', type=str, required=True)  # 这是ui自行组织的json，用于打印报告

        params = parser.parse_args(strict=True)
        return mc.pro_event_list_add(params)

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('begin_day', type=str, required=True)  # 事件编号
        parser.add_argument('end_day', type=str, required=True)  # 事件名
        parser.add_argument('event_type', type=int)  # 字典里有 , 默认0或不传
        #
        # 1       违规外联
        # 2       互联网传输泄密
        # 3       网络攻击窃密
        # 4       违规存储 / 处理涉密信息
        #
        parser.add_argument('event_miji', type=str)  # 字典里有 默认不传
        parser.add_argument('event_status', type=int)  #默认0，或不传 字典里有 1.待处理 2.不移交  3移交未反馈  4移交已反馈
        parser.add_argument('fulltext_query', type=str)  # 关键字查询(事件名 违规内容 备注)
        parser.add_argument('page_capa', type=int, required=True)  # 每页的容量（400）
        parser.add_argument('page_num', type=int, required=True)  # 跳页数（ 首页为0 ，第二页是1 ）
        params = parser.parse_args(strict=True)
        return mc.pro_event_list_query(params)

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('event_id', type=str, required=True)  # 事件编号
        parser.add_argument('event_name', type=str, required=True)  # 事件名
        parser.add_argument('event_type', type=int, required=True)  # 字典里有
        #
        # 1       违规外联
        # 2       互联网传输泄密
        # 3       网络攻击窃密
        # 4       违规存储 / 处理涉密信息
        #
        parser.add_argument('event_miji', type=str, required=True)  # 字典里有
        parser.add_argument('event_status', type=int, required=True)  # 字典里有 1.待处理 2.不移交  3移交未反馈  4移交已反馈
        parser.add_argument('remark', type=str)  # 备注
        parser.add_argument('add_user', type=str, required=True)  # 添加者
        params = parser.parse_args(strict=True)
        return mc.pro_event_list_edit(params)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('event_id', type=str, required=True)  # 事件编号
        params = parser.parse_args(strict=True)
        return mc.pro_event_list_drop(params)


@api.resource('/eventid/')
class EventID(Resource):
    def get(self):
        return mc.pro_event_list_create_event_id()


@api.resource('/keyword/')
class Keyword(Resource):
    '''
    关键字操作
    '''

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('keyword', type=str, required=True)  # 关键字、正则表达式
        parser.add_argument('keylevel', type=str, required=True)  # 等级
        parser.add_argument('enabled', type=int, required=True)  # -1 0  1
        parser.add_argument('remark', type=str)  # 备注
        parser.add_argument('add_user', type=str, required=True)  # 添加者
        parser.add_argument('keytype', type=int, required=True,choices=[1,2])  # 1:关键词  2：正则表达式

        params = parser.parse_args(strict=True)
        return mc.pro_cfg_keyword_add(params)

    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('begin_day',type=str, required=True)
        parser.add_argument('end_day',type=str, required=True)
        parser.add_argument('keylevel',type=int)
        parser.add_argument('enabled',type=int)
        parser.add_argument('keyword',type=str)
        parser.add_argument('last_keylevel',type=int)
        parser.add_argument('last_auid',type=int)
        parser.add_argument('page_count',type=int)
        parser.add_argument('order_by',type=str, required=True)
        parser.add_argument('keytype',type=int)

        params = parser.parse_args(strict=True)
        return mc.pro_cfg_keyword_query(params)

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('auid', type=int, required=True)  # 关键字id
        parser.add_argument('keyword', type=str, required=True)  # 关键字、正则表达式
        parser.add_argument('keylevel', type=str, required=True)  # 等级
        parser.add_argument('enabled', type=int, required=True)  # -1 0  1
        parser.add_argument('remark', type=str, required=True)  # 备注
        parser.add_argument('add_user', type=str, required=True)  # 添加者
        parser.add_argument('keytype', type=int, required=True, choices=[1, 2])  # 1:关键词  2：正则表达式

        params = parser.parse_args(strict=True)
        return mc.pro_cfg_keyword_edit(params)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('auid', type=int, required=True)  # 关键字id

        params = parser.parse_args(strict=True)
        return mc.pro_cfg_keyword_drop(params)


@api.resource('/keyword/valid/')
class KeywordValid(Resource):
    '''
    关键字有效性
    '''
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('auid', type=int)  # 关键字的auid
        parser.add_argument('valid', type=int)  # 是否有效

        params = parser.parse_args(strict=True)
        return mc.pro_cfg_keyword_edit_valid(params)






@api.resource('/keyword/batch/')
class KeywordBatch(Resource):
    '''
    批量添加关键字
    '''
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('keywords', required=True,action='append')  # 若干关键字组成的json串[{},{}]
        params = parser.parse_args(strict=True)
        return mc.pro_cfg_keyword_batchadd(params)



@api.resource('/platform/')
class Platform(Resource):
    '''
    平台的更新和查询
    '''
    def get(self):
         return mc.pro_platform_query()


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('platformid',type=int, required=True)  # 平台id
        parser.add_argument('name',type=str, required=True)  # 名称
        parser.add_argument('nicname',type=str, required=True)  # 别名
        parser.add_argument('simname',type=str, required=True)  # 简称
        params = parser.parse_args(strict=True)
        return mc.pro_platform_edit(params)




@api.resource('/alarmlist/add/')
class AlarmListAdd(Resource):
    '''
    添加告警清单
    '''

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('yth_fileana_id', type=str)
        parser.add_argument('__md5', type=str,)
        parser.add_argument('__connectTime', type=str)
        parser.add_argument('__title', type=str)
        parser.add_argument('__alarmLevel', type=int)
        parser.add_argument('summary', type=str)
        parser.add_argument('__alarmKey', type=str)
        parser.add_argument('__document', type=str)
        parser.add_argument('__industry', type=str)
        parser.add_argument('__security', type=str)
        parser.add_argument('__ips', type=str)
        parser.add_argument('__alarmType', type=int)
        parser.add_argument('__alarmSour', type=int)


        params = parser.parse_args(strict=True)
        return mc.pro_alarm_list_add_4api(params)




@api.resource('/ud/wdpfiletask/')
class WdpFileTask(Resource):
    """wdp_file_task的操作"""

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('n', type=int)
        params = parser.parse_args(strict=True)
        return mc.ud_wdp_file_task_query(params)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('file_md5', type=str)
        params = parser.parse_args(strict=True)
        return mc.ud_wdp_file_task_delete(params)


@api.resource('/ud/tasktmp/')
class TaskTmp(Resource):
    """task_tmp的操作"""
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid', type=str)
        parser.add_argument('md5', type=str)
        parser.add_argument('root_md5', type=str)
        parser.add_argument('parent_md5', type=str)
        params = parser.parse_args(strict=True)
        return mc.ud_task_tmp_add(params)

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid', type=str)
        params = parser.parse_args(strict=True)
        return mc.ud_task_tmp_search(params)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid', type=str)
        parser.add_argument('md5', type=str)
        params = parser.parse_args(strict=True)
        return mc.ud_task_tmp_delete(params)


@api.resource('/ud/fileanares/')
class FileanaRes(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('md5', type=str)
        params = parser.parse_args(strict=True)
        return mc.ud_file_ana_res_insert(params)


@api.resource('/ud/anares/')
class anaRes(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid', type=str)
        parser.add_argument('md5', type=str)
        parser.add_argument('root_md5', type=str)
        parser.add_argument('parent_md5', type=str)
        parser.add_argument('fileinfo', type=str) #jsondump转成的字符串
        parser.add_argument('__deepinfo', type=str)#base64编码的深度分析结果字符串
        parser.add_argument('__handleStatus', type=int)
        params = parser.parse_args(strict=True)
        return mc.ud_ana_res_insert(params)

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid', type=str)
        params = parser.parse_args(strict=True)
        return mc.ud_ana_res_search(params)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('uuid', type=str)
        params = parser.parse_args(strict=True)
        return mc.ud_ana_res_delete(params)