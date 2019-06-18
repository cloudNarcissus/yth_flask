from urllib.parse import quote

from flask import make_response
from flask_restful import Resource, reqparse

from . import api
from app.db.hbase import hbc



@api.resource('/filedownload/')
class Filedownload(Resource):
    '''
    下载文件
    '''
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('__md5', type=str,required=True)
        params = self.parser.parse_args(strict=True)

        file = hbc.dowmload_wdp_files(params)
        if file[0]:
            filename = file[1]['filename']
            content = file[1]['content']
            resp = make_response(content)
            resp.headers.extend({'Content-Disposition': 'attachment;filename=' + quote(filename)})
            return resp
        else:
            return {
                'message': file[1],
                'data': None
            }

