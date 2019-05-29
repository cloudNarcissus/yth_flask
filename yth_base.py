from elasticsearch import Elasticsearch
from elasticsearch_dsl import query, aggs, function
import logging.handlers
import time


from flask import Flask,Blueprint
from flask_restful import reqparse, abort, Api, Resource

yth_base = Blueprint('yth_base',__name__)
app = Flask(__name__)
api = Api(app)

from MyException.error import Success,NotFound

import os
if 'nt' != os.name:
    _log_path = './es_logger.log'
else:
    _path = os.path.dirname(__file__)
    _log_path = os.path.join(_path, os.path.pardir, os.path.pardir, 'logs')

import config
config_path = 'config.json'

logger = logging.getLogger('yth_base')
logger.setLevel(logging.INFO)
fhtime = logging.handlers.TimedRotatingFileHandler(_log_path, when='D', interval=1, backupCount=10)
fhtime.setFormatter(logging.Formatter("%(asctime)s-%(levelname)s-%(message)s"))
logger.addHandler(fhtime)


# 查询参数结构体
class Parameter(object):
    def __init__(self):
        self.query = dict()
        self.query['exact_query'] = False
        self.set_order('__connectTime','desc')

    def list_all_members(self):
        for name,value in vars(self).items():
            print('%s=%s'%(name,value))

    def return_all_members(self):
        L = []
        for name,value in vars(self).items():
            L.append('%s=%s'%(name,value))
        return L

    def set_time(self, begin, end, time_format=None):
        # 输入时间段、时间格式，时间格式默认为yyyy-MM-dd
        self.query['begin_time'] = begin
        self.query['end_time'] = end
        self.query['format'] = 'yyyy-MM-dd'
        if format is not None:
            self.query['time_format'] = time_format
        self.query['exact_query'] = False

    def set_from_size(self, from_, size):
        self.query['from'] = from_
        self.query['size'] = size

    def set_match_str(self, qstr):
        # 输入查询语句框内查询内容
        self.query['match_str'] = qstr

    def set_order(self, order, orderType):
        """
        当前有按挖掘时间 和 默认 相关度打分模式
        :param order:  按时间填写字符串 __connectTime， 默认填写 __bornTime
        :return:
        """
        self.query['order'] = order
        self.query['orderType'] = orderType

    # 行为分类#http,im,netdisk,email,filetransfer,other,csmp,docaudit,website
    def set_actionType(self,actionType):
        self.query['__actionType'] = actionType

    # 平台
    def set_platform(self,platform):
        self.query['__platform'] = platform


    def set_industry(self, industry):
        # 输入行业名称，参数为list格式
        if isinstance(industry, list) is False:
            print("industry input must be list!!")
        self.query['__industry'] = industry

    def set_document(self, document):
        # 输入版式名称
        self.query['__document'] = document

    def set_security(self, security):
        # 输入密级
        self.query['__security'] = security

    def set_alarm_key(self, alarmkey):
        # 输入关键词，参数为list
        if isinstance(alarmkey, list) is False:
            print("alarmkey input must be list")
        self.query['__alarmKey'] = alarmkey

    def set_exact_query(self, exact_query):
        # 输入是否是精确语法查找,是为true，否为false
        self.query['exact_query'] = exact_query

    def set_extention(self, extention):
        # 输入扩展名
        self.query['extention'] = extention

# ES操作
class ESClient(object):
    conf = None

    def __init__(self, config_path, log):
        self.conf = config.Config(config_path)
        self.es = Elasticsearch(hosts=self.conf.es_hosts)
        self.log = log

    # --------------------查询行为数据----------------------------------
    def search_yth_base(self, parameter):
        L = []
        for name, value in parameter.items():
            L.append('%s=%s' % (name, value))
        self.log.debug('========>进入 search_yth_base 函数,%s' % L)

        # #####################过滤条件###############################
        filter_query = query.MatchAll()
        # 日期
        if 'begin_time' in parameter and 'end_time' in parameter:
            date_query = query.Range(_expand__to_dot=False, __connectTime={
                'gte': parameter['begin_time'],
                'lte': parameter['end_time'], 'format': parameter['time_format']})
            filter_query = filter_query & date_query

        # 行为类型
        if '__actionType' in parameter:
            filter_query = filter_query & query.Term(_expand__to_dot=False,
                                                     __actionType=parameter['__actionType'])

        # 平台
        # if '__platform' in parameter:
        #     filter_query = filter_query & query.Term(_expand__to_dot=False,
        #                                              __actionType=parameter['__platform'])

        # #####################查询条件###############################
        match_query = query.MatchAll()
        if 'match_str' in parameter:
            qs = parameter['match_str']
            if parameter['exact_query']:
                qs = '\"' + qs + '\"'
            highlight_query = match_query & query.QueryString(
                default_field="__full_query",
                query=qs
            )
            match_query = match_query & (
                    query.QueryString(
                        default_field="__full_query",
                        query=qs
                    ) | query.QueryString(
                default_field="__summary",
                query=qs
            )
            )

        # #####################高亮内容###############################
        highlight = {
            "pre_tags": [
                "<font color=\\\"red\\\">"
            ],
            "post_tags": [
                "</font>"
            ],
            "fields": {
                "__summary": {
                    "highlight_query": highlight_query.to_dict()
                }
            }
        }

        # #####################聚合内容###############################
        actionType_agg = aggs.Filter(query.Bool(must_not=query.Match(_expand__to_dot=False, __actionType='')))
        actionType_agg.bucket('__actionType', 'terms', field='__actionType', size=30)

        platform_agg = aggs.Filter(query.Bool(must_not=query.Match(_expand__to_dot=False, __actionType='')))
        platform_agg.bucket('__platform', 'terms', field='__platform', size=10)

        # 查询语句
        all_query = {
            "bool": {
                "must": match_query.to_dict(),
                "filter": filter_query.to_dict()
            }
        }

        # 排序  按接入时间或采集时间排序
        sort = []
        if 'order' in parameter:
            if parameter['order'] == '__connectTime':
                self.log.debug('按接入时间排序')
                sort = [
                    {
                        "__connectTime": {
                            "order": parameter['orderType']
                        }
                    }]
            elif parameter['order'] == '__bornTime':
                self.log.debug('按采集时间排序')
                sort = [
                    {
                        "__bornTime": {
                            "order": parameter['orderType']
                        }
                    }]

        # 查询、聚合,总体组合
        body = {
            "aggs": {
                "actionType_agg": actionType_agg.to_dict()
            },
            "query": all_query,
            'sort': sort,
            "highlight": highlight
        }
        self.log.debug('使用查询语句:{0}，从es中搜索数据'.format(body))
        return self.es.search('yth_base', 'mytype', body,
                              size=parameter['size'],
                              from_=parameter['from']
                              )


    # --------------------查询文档数据-----------------------------------
    def search_yth_fileana(self,parameter):
        """

        :param parameter:
        :return:
        """

        # #####################过滤条件###############################
        filter_query = query.MatchAll()
        # 日期
        if 'begin_time' in parameter and 'end_time' in parameter:
            date_query = query.Range(_expand__to_dot=False, __connectTime={
                'gte': parameter['begin_time'],
                'lte': parameter['end_time'], 'format': parameter['format']})
            filter_query = filter_query & date_query

        # 文档md5（这在行为中，快速预览的时候查单条会用到）
        md5 = None
        if '__md5' in parameter:
            md5 = parameter['__md5']
            filter_query = filter_query & query.Term(_expand__to_dot=False, __md5=md5)


        # 密级分类
        if '__security' in parameter:
            filter_query = filter_query & query.Term(_expand__to_dot=False, __security=parameter['__security'])

        # 公文版式
        if '__document' in parameter:
            filter_query = filter_query & query.Term(_expand__to_dot=False, __document=parameter['__document'])


        # 行业分类
        if '__industry' in parameter:
            for v in parameter['__industry']:
                filter_query = filter_query & query.Match(_expand__to_dot=False, __industry=v)


        # #####################查询条件###############################
        match_query = query.MatchAll()
        if 'match_str' in parameter:
            qs = parameter['match_str']
            if parameter['exact_query']:
                qs = '\"' + qs + '\"'
            match_query = match_query & query.QueryString(
                default_field="__Content-text",
                query=qs
            )
        # 高亮内容
        highlight = {
            "pre_tags": [
                "<font color=\\\"red\\\">"
            ],
            "post_tags": [
                "</font>"
            ],
            "fields": {
                "__Content-text": {
                    "highlight_query": match_query.to_dict()
                }
            }
        }

        #平台
        if '_platform' in parameter:
            match_query = match_query & query.QueryString(
                default_field="_platforms",
                query=parameter['_platform']
            )

        # 关键词(嵌套文档查询)
        __alarmKey_list = []
        if '__alarmKey' in parameter:
            for keyword in parameter['__alarmKey']:
                __alarmKey_list.append({"term": {"__alarmKey.__keyword": keyword}})


        # 查询语句
        all_query = {
            "bool": {
                "must": [match_query.to_dict(),
                         #关键词
                         {"nested": {
                             "path": "__alarmKey",
                             "query": {
                                 "bool": {
                                     "should": __alarmKey_list
                                 }
                             }
                         }}
                         ],
                "filter": filter_query.to_dict()
            }
        }

        # 聚合内容
        alarm_agg = aggs.Filter(query.Bool(must_not=query.Match(_expand__to_dot=False, __alarmKey='')))
        alarm_agg.bucket('alarm', 'terms', field='__alarmKey', size=50)


        document_agg = aggs.Filter(query.Bool(must_not=query.Match(_expand__to_dot=False, __document='')))
        document_agg.bucket('document', 'terms', field='__document', size=20)


        industry_agg = aggs.Filter(query.Bool(must_not=query.Match(_expand__to_dot=False, __industry='')))
        industry_agg.bucket('industry', 'terms', field='__industry', size=50)

        security_agg = aggs.Filter(query.Bool(must_not=query.Match(_expand__to_dot=False, __security='')))
        security_agg.bucket('security', 'terms', field='__security', size=50)


        Extention_agg = aggs.Filter(query.Bool(must_not=query.Match(_expand__to_dot=False, __tikaExtention='')))
        Extention_agg.bucket('extention', 'terms', field='__tikaExtention', size=50)




        # 排序  按接入时间或涉密风险值排序
        sort = []
        if 'order' in parameter:
            if parameter['order'] == '__connectTime':
                self.log.debug('按接入时间排序')
                sort = [
                    {
                        "__connectTime": {
                            "order": parameter['orderType']
                        }
                    }]
            elif parameter['order'] == '__alarmLevel':
                self.log.debug('按涉密风险值排序')
                sort = [
                    {
                        "__alarmLevel": {
                            "order": parameter['orderType']
                        }
                    },
                    {
                        "__connectTime": {
                            "order": parameter['orderType']
                        }
                    }
                ]

        body = {
            "aggs": {
                "alarmKey": alarm_agg.to_dict(),
                "document": document_agg.to_dict(),
                "industry": industry_agg.to_dict(),
                "security": security_agg.to_dict(),
                "group_by_platform": { #平台数组聚合
                    "terms": {
                        "field": "_platforms",
                        "size": 10
                    }
                },
                "__alarmKey": {#关键字聚合
                    "nested": {
                        "path": "__alarmKey"
                    },
                    "aggs": {
                        "group_by_keyword": {
                            "terms": {
                                "field": "__alarmKey.__keyword",
                                "size": 10
                            }
                        }
                    }
                }
            },
            "query": all_query,
            'sort': sort,
            "highlight": highlight
        }

        self.log.debug('使用查询语句:{0}，从es中搜索数据'.format(body))
        return self.es.search('yth_fileana', 'mytype', body,
                              size= parameter['size'] if md5 is None else 1,
                              from_=parameter['from'],
                              _source_exclude=['__Content-text'],  # 返回内容不包含全文
                              )


    # -------------------------关注或者取消关注------------------------
    def update_interested(self, index_name, index_id, interested_or_cancel):
        self.log.debug('进入 update_interested 函数, 对一条数据进行关注或者取消关注')

        """
        关注或取消关注指定的文档，需要界面提供文档的索引名、索引id、关注或取消关注
        :param index_name: 索引名
        :param index_id:   索引id
        :param interested_or_cancel: 关注或取消，TRUE 为关注，FALSE为取消
        :return:  无
        """
        timestr =time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        body = {
            'doc':{
                'interested': interested_or_cancel,
                'interested_time': timestr
            }
        }

        self.log.debug('更新关注数据，语句为{0}'.format(body))
        try:
            self.es.update(index_name,'mytype',index_id,body)
            return True
        except :
            self.log.error('更新关注数据,some error')
            return False

    # ----------------快速预览中，若遇到rar或者嵌套文件，则查询其子文件（传入md5查询子记录)-------------
    def query_yth_rarchildren(self,rootmd5):
        """

        :param rootmd5:根文件的md5
        :return:
        """
        self.log.debug('进入 query_yth_rarchildren 函数，查询根文件下面的子文件')

        filter_query = query.Term(_expand__to_dot=False, __rootmd5=rootmd5)
        body = {
            "query":{
                "bool": {
                    "filter": filter_query.to_dict()
                }
            }
        }

        self.log.debug('使用查询语句:{0}，从es中搜索数据'.format(body))
        return self.es.search('yth_rarchildren', 'mytype', body,size=10)

    #


@yth_base.route('/yth_base')
@api.resource('/v1.0/action/')
class SearchYthBase(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('begin_time', type=str)
    parser.add_argument('end_time', type=str)
    parser.add_argument('time_format', type=str)
    parser.add_argument('match_str', type=str)
    parser.add_argument('exact_query', type=int)
    parser.add_argument('order', type=str)
    parser.add_argument('orderType', type=str)
    parser.add_argument('size', type=int, required=True)
    parser.add_argument('from', type=int, required=True)
    parser.add_argument('__actionType',type=str)

    def post(self):
        es_client = ESClient(config_path, logger)
        parameter = self.parser.parse_args(strict=True)
        return es_client.search_yth_base(parameter)


@yth_base.route('/yth_base')
@api.resource('/v1.0/fileana/')
class SearchYthFileana(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('begin_time', type=str)
    parser.add_argument('end_time', type=str)
    parser.add_argument('time_format', type=str)
    parser.add_argument('__md5', type=str)
    parser.add_argument('__security',type=str)
    parser.add_argument('__document', type=str) #公文
    parser.add_argument('__industry', type=str) #行业(list)
    parser.add_argument('match_str', type=str)
    parser.add_argument('exact_query', type=int)
    parser.add_argument('_platform', type=int)
    parser.add_argument('__alarmKey', type=str)#关键字list
    parser.add_argument('order', type=str)
    parser.add_argument('orderType', type=str)
    parser.add_argument('size', type=int, required=True)
    parser.add_argument('from', type=int, required=True)
    parser.add_argument('__actionType', type=str)


    def post(self):
        es_client = ESClient(config_path, logger)
        parameter = self.parser.parse_args(strict=True)
        return es_client.search_yth_fileana(parameter)


@api.resource('/v1.0/interested/')
class Interested(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('index_name', type=str)
    parser.add_argument('index_id', type=str)
    parser.add_argument('interested_or_cancel', type=str)

    def post(self):
        es_client = ESClient(config_path, logger)
        parameter = self.parser.parse_args(strict=True)

        if es_client.update_interested(parameter['index_name'], parameter['index_id'], parameter['interested_or_cancel']):
            return Success()
        else:
            raise NotFound(description="更新异常")


@api.resource('/v1.0/rarchildren/')
class RarChildren(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('rootmd5', type=str)

    def post(self):
        es_client = ESClient(config_path, logger)
        parameter = self.parser.parse_args(strict=True)

        return es_client.query_yth_rarchildren(parameter['rootmd5'])










if __name__ == '__main__':
    # log_file = "./es_logger.log"
    # logging.basicConfig(filename=log_file, level=logging.DEBUG)
    # es_client = ESClient('192.168.10.136:9200', logging)
    # parameter = Parameter()
    # parameter.set_match_str('国家保密局')
    # parameter.set_time('2019-05-16', '2019-05-21')
    # parameter.set_from_size(0, 10)
    # print(es_client.search_yth_fileana(parameter))
    app.run(host="0.0.0.0", port=10001)


    # print(es_client.search_yth_base(parameter))
    # print(es_client.query_yth_rarchildren('dfdf'))