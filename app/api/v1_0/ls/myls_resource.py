from flask_restful import Resource, reqparse

from app.api.v1_0 import api_ls
from app.db.myls import mc


@api_ls.resource('/alarmtype/')
class AlarmType(Resource):
    '''
    查询告警类型分布
    '''

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('begin_day', type=int, required=True)  # 起始时间
        parser.add_argument('end_day', type=int,required=True)      # 结束时间

        parser.add_argument('province', type=str) #省编码（6位）
        parser.add_argument('city', type=str)  # 市编码（6）
        parser.add_argument('district',type=str)  # 区编码（6）

        params = parser.parse_args(strict=True)
        return mc.pro_alarm_alarmtype(params)


@api_ls.resource('/alarmtypelevel/')
class AlarmTypeLevel(Resource):
    '''
    告警级别分布 及 处置情况 （有3个图）
    '''

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('begin_day', type=int, required=True)  # 起始时间
        parser.add_argument('end_day', type=int,required=True)      # 结束时间

        parser.add_argument('province', type=str) #省编码（6位）
        parser.add_argument('city', type=str)  # 市编码（6）
        parser.add_argument('district',type=str)  # 区编码（6）

        params = parser.parse_args(strict=True)
        return mc.pro_alarm_alarmtypelevel(params)





@api_ls.resource('/alarmcztrend/')
class AlarmCzTrend(Resource):
    '''
    处置趋势 ， 所谓趋势，就是按天给出数据（没有数据的天，不出现！）
    '''

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('begin_day', type=int, required=True)  # 起始时间
        parser.add_argument('end_day', type=int,required=True)      # 结束时间

        parser.add_argument('province', type=str) #省编码（6位）
        parser.add_argument('city', type=str)  # 市编码（6）
        parser.add_argument('district',type=str)  # 区编码（6）

        params = parser.parse_args(strict=True)
        return mc.pro_alarm_alarmcztrend(params)



@api_ls.resource('/alarmczstatus/')
class AlarmCzStatus(Resource):
    '''
    # 4. 处置结果密级分布
    '''

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('begin_day', type=int, required=True)  # 起始时间
        parser.add_argument('end_day', type=int,required=True)      # 结束时间

        parser.add_argument('province', type=str) #省编码（6位）
        parser.add_argument('city', type=str)  # 市编码（6）
        parser.add_argument('district',type=str)  # 区编码（6）

        params = parser.parse_args(strict=True)
        return mc.pro_alarm_alarmczstatus(params)


@api_ls.resource('/alarmmap/')
class AlarmMap(Resource):
    '''
    # 5. 报警地图以及处置分布
    '''

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('begin_day', type=int, required=True)  # 起始时间
        parser.add_argument('end_day', type=int,required=True)      # 结束时间

        parser.add_argument('province', type=str) #省编码（6位）
        parser.add_argument('city', type=str)  # 市编码（6）
        parser.add_argument('district',type=str)  # 区编码（6）

        params = parser.parse_args(strict=True)
        return mc.pro_alarm_map(params)


@api_ls.resource('/eventtrend/')
class EventTrend(Resource):
    '''
    事件趋势 ， 所谓趋势，就是按天给出数据（没有数据的天，不出现！）
    '''

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('begin_day', type=int, required=True)  # 起始时间
        parser.add_argument('end_day', type=int,required=True)      # 结束时间

        parser.add_argument('province', type=str) #省编码（6位）
        parser.add_argument('city', type=str)  # 市编码（6）
        parser.add_argument('district',type=str)  # 区编码（6）

        params = parser.parse_args(strict=True)
        return mc.pro_event_trend(params)

