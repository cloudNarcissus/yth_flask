from flask_restful import Resource, reqparse

from app.api.v1_0 import api_ls
from app.db.mysql import mc


@api_ls.resource('/dict/')
class Dict(Resource):
    '''
    获取字典
    '''

    def get(self):
        return mc.pro_dict_query()