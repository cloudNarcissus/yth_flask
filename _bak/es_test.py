from elasticsearch import Elasticsearch
from elasticsearch_dsl import query, aggs, function
import logging
import time


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
        self.query['industry'] = industry

    def set_document(self, document):
        # 输入版式名称
        self.query['document'] = document

    def set_security(self, security):
        # 输入密级
        self.query['security'] = security

    def set_alarm_key(self, alarmkey):
        # 输入关键词，参数为list
        if isinstance(alarmkey, list) is False:
            print("alarmkey input must be list")
        self.query['alarmKey'] = alarmkey

    def set_exact_query(self, exact_query):
        # 输入是否是精确语法查找,是为true，否为false
        self.query['exact_query'] = exact_query

    def set_extention(self, extention):
        # 输入扩展名
        self.query['extention'] = extention

class ESClient(object):
    def __init__(self, hosts, log):
        self.es = Elasticsearch(hosts=hosts)

        self.log = log

    def search_yth_base(self, params):
        self.log.debug('进入 search_yth_base 函数,%s'%params.return_all_members())

        # #####################过滤条件###############################
        filter_query = query.MatchAll()
        # 日期
        date_query = query.Range(_expand__to_dot=False, __connectTime={
            'gte': params.query['begin_time'],
            'lte': params.query['end_time'], 'format': params.query['format']})
        filter_query = filter_query & date_query

        # 行为分类
        if '__actionType' in params.query:
            filter_query = filter_query & query.Term(_expand__to_dot=False,
                                                     __actionType=params.query['__actionType'])



        # #####################查询条件###############################
        match_query = query.MatchAll()
        if 'match_str' in params.query:
            qs = params.query['match_str']
            if params.query['exact_query']:
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
        actionType_agg.bucket('actionType', 'terms', field='__actionType', size=30)


        # 查询语句
        all_query = {
            "bool": {
                "must": match_query.to_dict(),
                "filter": filter_query.to_dict()
            }
        }

        # 排序  按接入时间或采集时间排序
        sort = []
        if 'sort' in parameter.query:
            if parameter.query['order'] == '__connectTime':
                self.log.debug('按接入时间排序')
                sort = [
                    {
                    "__connectTime": {
                        "order": parameter.query['orderType']
                    }
                }]
            elif parameter.query['order'] == '__bornTime':
                self.log.debug('按采集时间排序')
                sort = [
                    {
                        "__bornTime": {
                            "order": parameter.query['orderType']
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
                              size=parameter.query['size'],
                              from_=parameter.query['from']
                              )



if __name__ == '__main__':
    log_file = "./es_logger.log"
    logging.basicConfig(filename=log_file, level=logging.DEBUG)
    es_client = ESClient('192.168.10.136:9200', logging)
    parameter = Parameter()
    parameter.set_match_str('国家保密局')
    parameter.set_time('2019-05-16', '2019-05-21')
    parameter.set_from_size(0, 10)
    print(parameter.return_all_members())
    print(es_client.search_yth_base(parameter))
