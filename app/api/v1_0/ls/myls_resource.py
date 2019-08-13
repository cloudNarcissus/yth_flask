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