from flask_restful import Resource, reqparse

from . import api
from app.db.es import ec


@api.resource('/action/')
class SearchYthBase(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('begin_time', type=str)
    parser.add_argument('end_time', type=str)
    parser.add_argument('time_format', type=str)
    parser.add_argument('match_str', type=str)
    parser.add_argument('exact_query', type=bool)
    parser.add_argument('order', type=str)
    parser.add_argument('orderType', type=str)
    parser.add_argument('size', type=int, required=True)
    parser.add_argument('from', type=int, required=True)
    parser.add_argument('__actionType', type=str)
    parser.add_argument('_interested', type=bool)

    def post(self):
        params = self.parser.parse_args(strict=True)
        return ec.search_yth_base(params)



@api.resource('/action/one/')
class SearchYthBaseOne(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('index_id', type=str)

    def get(self):
        params = self.parser.parse_args(strict=True)
        return ec.query_yth_base_by_indexid(params)



@api.resource('/fileana/')
class SearchYthFileana(Resource):


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('begin_time', type=str)
        parser.add_argument('end_time', type=str)
        parser.add_argument('time_format', type=str)
        parser.add_argument('__md5', type=str)
        parser.add_argument('__security', type=str)
        parser.add_argument('__document', type=str)  # 公文
        parser.add_argument('__industry', type=list)  # 行业(list)
        parser.add_argument('match_str', type=str)
        parser.add_argument('exact_query', type=bool)
        parser.add_argument('_platform', type=int)
        parser.add_argument('__alarmKey')  # 关键字list
        parser.add_argument('order', type=str)
        parser.add_argument('orderType', type=str)
        parser.add_argument('size', type=int, required=True)
        parser.add_argument('from', type=int, required=True)
        parser.add_argument('_interested', type=bool)
        params = parser.parse_args(strict=True)
        return ec.search_yth_fileana(params)


@api.resource('/fileana/alarm/')
class AddAlarmToList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('index_id', type=str, required=True)
    parser.add_argument('__md5', type=str, required=True)
    parser.add_argument('__alarmSour', type=int, required=True)

    def post(self):
        params = self.parser.parse_args(strict=True)
        return ec.add_alarm_list(params)


@api.resource('/fileana/simdoc/')
class GetSimDoc(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('index_id', type=str, required=True)
    parser.add_argument('__md5', type=str, required=True)

    def post(self):
        params = self.parser.parse_args(strict=True)
        return ec.search_sim_doc(params)


@api.resource('/interested/')
class Interested(Resource):
    parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument('index_name', type=str)
        self.parser.add_argument('index_id', type=str)
        self.parser.add_argument('interested_or_cancel', type=bool)

        params = self.parser.parse_args(strict=True)
        return ec.update_interested(params)

    def get(self):
        self.parser.add_argument('index_name', type=str)
        self.parser.add_argument('size', type=int)
        self.parser.add_argument('from__', type=int)

        params = self.parser.parse_args(strict=True)
        return ec.get_interested(params)


@api.resource('/rarchildren/')
class RarChildren(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('__rootmd5s', type=str)

    def post(self):
        params = self.parser.parse_args(strict=True)
        return ec.query_yth_rarchildren(params)



@api.resource('/interested/list/')
class InterestedList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('index_name', type=str, required=True, choices=['yth_fileana', 'yth_base'])
    parser.add_argument('from', type=int, required=True)
    parser.add_argument('size', type=int, required=True)

    def get(self):
        params = self.parser.parse_args(strict=True)
        return ec.search_all_interested(params)



@api.resource('/fileana/view/')
class FileanaView(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('__md5', type=str, required=True)

    def get(self):
        params = self.parser.parse_args(strict=True)
        return ec.query_content_text(params)



