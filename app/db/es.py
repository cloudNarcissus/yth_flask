import time
import logging

from elasticsearch import Elasticsearch
from elasticsearch_dsl import query, aggs

from app.config import Config
from app.utils.common import addHead
from app.db.mysql import mc

logger = logging.getLogger(__name__)


# ES操作
class ESClient(object):
    def __init__(self):
        self.es = Elasticsearch(hosts=Config.es_hosts)
        self.log = logger

    # --------------------查询行为数据----------------------------------
    @addHead()
    def search_yth_base(self, params):
        L = []
        for name, value in params.items():
            L.append('%s=%s' % (name, value))
        self.log.debug('========>进入 search_yth_base 函数,%s' % L)

        # #####################过滤条件###############################
        filter_query = query.MatchAll()
        # 日期
        if params['begin_time'] is not None and params['end_time'] is not None:
            date_query = query.Range(_expand__to_dot=False, __connectTime={
                'gte': params['begin_time'],
                'lte': params['end_time'], 'format': params['time_format']})
            filter_query = filter_query & date_query

        # 行为类型
        if params['__actionType'] is not None:
            filter_query = filter_query & query.Term(_expand__to_dot=False,
                                                     __actionType=params['__actionType'])

        # 平台
        # if params['__platform'] is not None:
        #     filter_query = filter_query & query.Term(_expand__to_dot=False,
        #                                              __actionType=params['__platform'])

        # #####################查询条件###############################
        match_query = query.MatchAll()
        highlight = {}
        if params['match_str'] is not None:
            qs = params['match_str']
            if params['exact_query']:
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
        if params['order'] is not None:
            if params['order'] == '__connectTime':
                self.log.debug('按接入时间排序')
                sort = [
                    {
                        "__connectTime": {
                            "order": params['orderType']
                        }
                    }]
            elif params['order'] == '__bornTime':
                self.log.debug('按采集时间排序')
                sort = [
                    {
                        "__bornTime": {
                            "order": params['orderType']
                        }
                    }]

        sort.append(
            {
                "_id": {
                    "order": "asc"
                }
            }
        )

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
        return True, self.es.search('yth_base', 'mytype', body,
                                    size=params['size'],
                                    from_=params['from']
                                    )

    # --------------------查询文档数据-----------------------------------
    @addHead()
    def search_yth_fileana(self, params):
        """

        :param params:
        :return:
        """

        # #####################过滤条件###############################
        filter_query = query.MatchAll()
        # 日期
        if params['begin_time'] is not None and params['end_time'] is not None:
            date_query = query.Range(_expand__to_dot=False, __connectTime={
                'gte': params['begin_time'],
                'lte': params['end_time'], 'format': params.get('time_format', 'yyyy-MM-dd')})
            filter_query = filter_query & date_query

        # 文档md5（这在行为中，快速预览的时候查单条会用到）
        md5 = None
        if params['__md5'] is not None and params['__md5'] is not None:
            md5 = params['__md5']
            filter_query = filter_query & query.Term(_expand__to_dot=False, __md5=md5)

        # 密级分类
        if params['__security'] is not None:
            filter_query = filter_query & query.Term(_expand__to_dot=False, __security=params['__security'])

        # 公文版式
        if params['__document'] is not None:
            filter_query = filter_query & query.Term(_expand__to_dot=False, __document=params['__document'])

        # 行业分类
        if params['__industry'] is not None:
            for v in params['__industry']:
                filter_query = filter_query & query.Match(_expand__to_dot=False, __industry=v)

        # #####################查询条件###############################
        match_query = query.MatchAll()
        highlight = {}
        if params['match_str'] is not None:
            qs = params['match_str']
            if params['exact_query']:
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

        # 平台
        if params['_platform'] is not None:
            match_query = match_query & query.QueryString(
                default_field="_platforms",
                query=params['_platform']
            )

        # 关键词(嵌套文档查询)
        alarmKey_list = []
        if params['__alarmKey'] is not None:
            for keyword in params['__alarmKey']:
                alarmKey_list.append({"term": {"__alarmKey.__keyword": keyword}})

        # 查询语句
        all_query = {
            "bool": {
                "must": [match_query.to_dict(),
                         # 关键词
                         {"nested": {
                             "path": "__alarmKey",
                             "query": {
                                 "bool": {
                                     "should": alarmKey_list
                                 }
                             }
                         }}
                         ],
                "filter": filter_query.to_dict()
            }
        }

        # 聚合内容

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
        if params['order'] is not None:
            if params['order'] == '__connectTime':
                self.log.debug('按接入时间排序')
                sort = [
                    {
                        "__connectTime": {
                            "order": params['orderType']
                        }
                    }]
            elif params['order'] == '__alarmLevel':
                self.log.debug('按涉密风险值排序')
                sort = [
                    {
                        "__alarmLevel": {
                            "order": params['orderType']
                        }
                    },
                    {
                        "__connectTime": {
                            "order": params['orderType']
                        }
                    }
                ]

        sort.append(
            {
                "_id": {
                    "order": "asc"
                }
            }
        )

        body = {
            "aggs": {
                "document": document_agg.to_dict(),
                "industry": industry_agg.to_dict(),
                "security": security_agg.to_dict(),
                "group_by_platform": {  # 平台数组聚合
                    "terms": {
                        "field": "_platforms",
                        "size": 10
                    }
                },
                "__alarmKey": {  # 关键字聚合
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
        return True, self.es.search('yth_fileana', 'mytype', body,
                                    size=params['size'] if md5 is None else 1,
                                    from_=params['from'],
                                    _source_exclude=['__Content-text'],  # 返回内容不包含全文
                                    )

    # --------------------查询最近5个关注-----------------------------------
    @addHead()
    def get_interested(self, params):
        """

        :param index_name: 文档：yth_fileana  行为：yth_base
        :param size:
        :param from__:
        :return:
        """
        self.log.debug('进入 get_interested 函数, 获取最近关注的5条文档')

        index_name = params.get('index_name')
        size = params.get('size', 5)
        from__ = params.get('from__', 0)

        """
        返回最近结果
        :return: 返回用户最近关注的5条数据
       """
        sort = [
            {
                "interested_time":
                    {"order": "desc",
                     'missing': '_last'}
            },
        ]

        body = {
            "query": {
                'term': {
                    'interested': {
                        'value': True
                    }
                }
            },
            'sort': sort
        }

        self.log.debug('使用查询语句:{0}，从es中搜索数据'.format(body))
        self.log.debug('排序语句：{0}'.format(sort))
        return self.es.search(index_name, 'mytype', body,
                              size=size,
                              from_=from__,
                              _source_exclude=['__Content-text'],  # 返回内容不包含全文
                              )

    # --------------------关注或者取消关注-----------------------------------
    @addHead()
    def update_interested(self, params):

        index_name = params.get('index_name')
        index_id = params.get('index_id')
        interested_or_cancel = params.get('interested_or_cancel')

        self.log.debug('进入 update_interested 函数, 对一条数据进行关注或者取消关注')

        """
        关注或取消关注指定的文档，需要界面提供文档的索引名、索引id、关注或取消关注
        :param index_name: 索引名
        :param index_id:   索引id
        :param interested_or_cancel: 关注或取消，TRUE 为关注，FALSE为取消
        :return:  无
        """
        timestr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        body = {
            'doc': {
                '_interested': interested_or_cancel,
                '_interested_time': timestr
            }
        }

        self.log.debug('更新关注数据，语句为{0}'.format(body))
        try:
            self.es.update(index_name, 'mytype', index_id, body)
            return True, '更新成功'
        except:
            self.log.error('更新关注数据,some error')
            return False, '更新关注数据,some error'

    # --------------------快速预览的文件树-----------------------------------
    @addHead()
    def query_yth_rarchildren(self, params):
        """
        若该文件有父节点，则说明该文件是rar或者嵌套文件的子文件，则查询其父的所有子文件（传入md5查询子记录)
        :param __md5:子文件的md5   __rootmd5:根节点md5列表（1个或若干个）
        :return:
        """
        self.log.debug('进入 query_yth_rarchildren 函数，查询根文件下面的子文件')

        rootmd5s = params['__rootmd5s']

        forest = []  # 森林（多棵树）

        for rootmd5 in rootmd5s:
            body = {
                "query": {
                    "bool": {
                        "must": [
                            {"term":
                                {
                                    "__rootmd5": {"value": rootmd5}
                                }
                            }

                        ]
                    }
                }
            }
            root = self.es.search('yth_raroot', 'mytype', body, size=1)
            # children = self.es.search('yth_fileana', 'mytype', body, size=10)
            tree = {
                "root": root,
                "children": "暂无"  # children
            }
            forest.append(tree)

        return True, forest

    # -------------------------查询某个MD5的yth_base记录----------------------------------------
    def query_yth_base_by_md5(self, md5, connectTime=None):
        self.log.debug('进入 query_yth_base_by_md5 函数，查询MD5：%s的行为记录' % md5)

        filter_query = query.Term(_expand__to_dot=False, __md5=md5)

        if connectTime is not None:
            date_query = query.Range(_expand__to_dot=False, __connectTime={'gt': connectTime})
            filter_query = filter_query & date_query

        body = {
            "query": {
                "bool": {
                    "filter": filter_query.to_dict()
                }
            },
            'sort': [
                {
                    "__connectTime": {
                        "order": "desc"
                    }
                }
            ]
        }
        # self.log.debug('使用查询语句:{0}，从es中搜索数据'.format(body))
        return self.es.search('yth_base', 'mytype', body, size=20)

    # -------------------------加入告警到alarm——list-------------------------------------------
    @addHead()
    def add_alarm_list(self, params):

        index_id = params['index_id']
        md5 = params.get('__md5')
        alarmSour = params['__alarmSour']

        def query_yth_base_then_insert_action_list(md5, connectTime, redPoint):
            # 先查询 yth_base，然后入action_list
            action_dict = self.query_yth_base_by_md5(md5, connectTime)
            action_count = action_dict.get('hits').get('total')
            if action_count > 0:
                action_list = action_dict.get('hits').get('hits')
                for row in action_list:
                    params_dict = {
                        'yth_base_id': row['_id'],
                        '__md5': row['__md5'],
                        'platform': row['__platform'],
                        'actiontype': row['__actionType'],
                        'redPoint': redPoint,
                        '__unit': row.get('__unit',''),
                        '__connectTime': row['__connectTime'],

                        'website_info_name': row.get('website_info_name', ''),
                        'account': row.get('app_opt', {}).get('account', {}),
                        'url': row.get('url', ''),
                        'ip': row.get('ip', ''),
                        'smac': row.get('smac', ''),
                        'sport': row.get('sport', ''),
                        '__unitaddr':row.get('__unitaddr', ''),
                        '__contact':row.get('__contact','')
                    }
                    mc.pro_action_list_add(params_dict)
            return True, ''

        def add_alarm_list(alarmSour):
            if self.es.exists(index='yth_fileana', doc_type='mytype', id=index_id):
                es_doc = self.es.get(index='yth_fileana', doc_type='mytype', id=index_id).get('_source')
                params_dict = {'yth_fileana_id': index_id, '__md5': es_doc['__md5'],
                               '__connectTime': es_doc['__connectTime'], '__title': es_doc['FileName'],
                               '__alarmLevel': 5, '__alarmSour': alarmSour, 'summary': es_doc['file_summary'],
                               '__alarmKey': es_doc['__alarmKey'], '__document': es_doc['__document'],
                               '__industry': es_doc['__industry'], '__security': es_doc['__security'],
                               '__ips': es_doc.get('__ips', None), '__alarmType': es_doc.get('__alarmType', None)}
                # 入库alarm_list
                result = mc.pro_alarm_list_add(params_dict)
            else:
                result = False, 'yth_fileana找不到该文档记录'

            return result

        def update_yth_fileana_alarmed(index_id):
            body = {
                'doc': {
                    '_alarmed': True,
                    '__alarmLevel': 5  # 手动加入的告警都是5级
                }
            }
            self.log.debug('更新告警数据，语句为{0}'.format(body))
            try:
                self.es.update('yth_fileana', 'mytype', index_id, body)
                return True, '更新成功'
            except:
                self.log.error('更新关注数据,some error')
                return False, '更新关注数据,some error'

        # 判断alarm_list中是否存在
        err, exists = mc.fun_alarm_list_exists(md5)
        if err:
            if exists == 0:  # 不存在
                self.log.debug('查询yth_fileana，并将结果导入alarm_list')
                result = add_alarm_list(alarmSour)
                if result[0]:
                    # 先查询 yth_base，然后入action_list
                    if not query_yth_base_then_insert_action_list(md5, None, False)[0]:
                        self.log.error('入库insert_action_list失败')
                        return False, '入库insert_action_list失败'
                else:
                    self.log.error('入库pro_alarm_list_add失败')
                    return False, '入库pro_alarm_list_add失败'

            elif exists == 2:  # 存在且被判定为违规
                # 获取上次时间
                result = mc.fun_action_list_getLastTime(md5)
                if result[0]:
                    # 先查询 yth_base，然后入action_list
                    if not query_yth_base_then_insert_action_list(md5, result[1], True)[0]:
                        self.log.error('入库insert_action_list失败')
                        return False, '入库insert_action_list失败'
                else:
                    return False, '存在且被判定为违规,fun_action_list_getLastTime(%s) error' % md5
            elif exists == 1:  # 存在，但未被判定为违规
                # 获取上次时间
                result = mc.fun_action_list_getLastTime(md5)
                if result[0]:
                    # 先查询 yth_base，然后入action_list
                    if not query_yth_base_then_insert_action_list(md5, result[1], False)[0]:
                        self.log.error('入库insert_action_list失败')
                        return False, '入库insert_action_list失败'
                else:
                    return False, '存在，但未被判定为违规,fun_action_list_getLastTime(%s) error' % md5

            # 手动加入告警列表以后，要把状态变为“已加入告警”; 注意自动加入告警的，是直接写的时候就把alarmed=true的
            if alarmSour == 2:
                return update_yth_fileana_alarmed(index_id)
            elif alarmSour == 1:
                return True, '成功加入告警'


        else:
            return False, 'fun_alarm_list_exists(%s) error' % md5

    # -------------------------查询相似文档-----------------------------------------------------
    @addHead()
    def search_sim_doc(self, params):
        self.log.debug('进入 search_sim_doc 函数')

        index_id = params['index_id']
        md5 = params['__md5']

        from app.utils.stopwords import stop_list
        q = query.MoreLikeThis(
            _expand__to_dot=False,
            fields=['__Content-text'],
            like=[
                {
                    "_index": "yth_fileana",
                    "_type": "mytype",
                    "_id": index_id
                }
            ],
            min_term_freq=1,
            max_query_terms=25,
            min_doc_freq=1,
            min_word_length=2,
            minimum_should_match='85%',
            stop_words=stop_list
        )

        body = {
            'query': query.Bool(must=q.to_dict(), must_not=query.Match(_expand__to_dot=False, __MD5=md5)).to_dict()
        }

        logging.debug('使用查询语句:{0}，从es中搜索文档相似数据数据'.format(body))
        return True, self.es.search('yth_fileana', 'mytype', body=body,
                                    _source_exclude=['__Content-text'])

    @addHead()
    def search_all_interested(self, params):
        '''
        查询关注列表
        :param params: index_name , 索引名
        :param params: from
        :param params: size
        :return:
        '''
        body = {
            'query': {
                'bool': {
                    'filter': {
                        'term': {
                            '_interested': True
                        }
                    }
                }
            },
            'sort': [
                {
                    '_interested_time': {
                        'order': 'desc'
                    }
                }
            ]
        }
        return True, self.es.search(params['index_name'], 'mytype', body,
                                    size=params['from'],
                                    from_=params['size'],
                                    _source_exclude=['__Content-text'])

    @addHead()
    def query_content_text(self, params):
        '''
        查询单个文件的文本内容
        :param params:__md5 
        :return: 
        '''
        md5 = params.get('__md5')
        self.log.debug('进入 query_content_text 函数 ,%s' % md5)

        body = {
            "query": {
                'term': {
                    '__md5': {
                        'value': md5
                    }
                }
            }
        }
        return True, self.es.search('yth_fileana', 'mytype', body=body,
                                    _source_include=['__Content-text'])


ec = ESClient()
