from flask_restful import Resource, reqparse

from . import api
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
                            required=True)  # NO: 未处置  PASS：处置为正常  JIMI: 处置为机密   MIMI: 处置为秘密    JUEMI：处置为绝密
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
        parser.add_argument('platform', type=int)
        parser.add_argument('__alarmSour', type=int)

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
        parser.add_argument('_interested', type=bool, required=True)
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
class EventListAdd(Resource):
    '''
    插入事件列表,同时将关联的行为插入
    '''

    def post(self):
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
        parser.add_argument('content', type=str, required=True)  # 内容 显示 文件名 或者 违规外联描述
        parser.add_argument('remark', type=str, required=True)  # 备注
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
