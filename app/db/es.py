import json
import time
import logging
from ast import literal_eval

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

        # 是否关注
        if params['_interested'] is True:
            filter_query = filter_query & query.Term(_expand__to_dot=False,
                                                     _interested=True)

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
                                    from_=params['from'], _source_exclude=['sm_summary']
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
            for indu_dict_str in params['__industry']:
                indu_dict = literal_eval(indu_dict_str)
                filter_query = filter_query & query.Match(_expand__to_dot=False, __industry=indu_dict.get('key'))

        # 是否关注
        if params['_interested'] is True:
            filter_query = filter_query & query.Term(_expand__to_dot=False,
                                                     _interested=True)

        # #####################查询条件###############################
        match_query = query.MatchAll()
        # highlight = {}
        if params['match_str'] is not None:
            qs = str(params['match_str']).strip()
            if qs.startswith('.'):  # 以.开头则默认为查询后缀名
                qs = qs.strip('.')  # 去掉.开始查询
                filter_query = filter_query & query.Term(_expand__to_dot=False,__tikaExtention=qs)
            else:
                if params['exact_query']:
                    qs = '\"' + qs + '\"'
                match_query = match_query & (
                    query.QueryString(
                        default_field="__Content-text",
                        query=qs
                    ) | query.QueryString(  # 搜索框内的条件还可以查询Filename，也即标题
                        default_field="FileName",
                        query=qs
                    )
                )


                # 高亮内容  暂时不要了
                # highlight = {
                #     "pre_tags": [
                #         "<font color=\\\"red\\\">"
                #     ],
                #     "post_tags": [
                #         "</font>"
                #     ],
                #     "fields": {
                #         "__Content-text": {
                #             "highlight_query": match_query.to_dict()
                #         }
                #     }
                # }

        # 平台
        if params['_platform'] is not None:
            match_query = match_query & query.QueryString(
                default_field="_platforms",
                query=params['_platform']
            )

        must = [match_query.to_dict()]

        # 关键词(嵌套文档查询)
        alarmKey_list = []
        if params['__alarmKey'] is not None:
            for keyword_dict_str in params['__alarmKey']:
                keyword_dict = literal_eval(keyword_dict_str)
                alarmKey_list.append({"term": {"__alarmKey.__keyword": keyword_dict.get('key')}})

            must.append({"nested": {
                "path": "__alarmKey",
                "query": {
                    "bool": {
                        "should": alarmKey_list
                    }
                }
            }})
        # 查询语句
        all_query = {
            "bool": {
                "must": must,
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
            'sort': sort
            # "highlight": highlight
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
        :param __md5:当前文件的md5  
        :return:
        """

        md5 = params['__md5']

        self.log.debug('进入 query_yth_rarchildren 函数，查询根文件下面的子文件')

        # 通过md5 取出 rootmd5s ， 如果没有，说明是行为那边来的数据
        body = {
            "query": {
                "bool": {
                    "must": [
                        {"term":
                            {
                                "__md5": {"value": md5}
                            }
                        }

                    ]
                }
            }
        }
        root = self.es.search('yth_fileana', 'mytype', body, size=1)
        rootmd5s = []
        if root['hits']['total'] > 0:
            rootmd5s = root['hits']['hits'][0]['_source']['__rootmd5s']
        else:
            rootmd5s.append(md5)

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
            tree = self.es.search('yth_raroot', 'mytype', body, size=10)
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
        return self.es.search('yth_base', 'mytype', body, size=20, _source_exclude=['sm_summary'])

    # -------------------------查询某个index_id的yth_base记录----------------------------------------
    @addHead()
    def query_yth_base_by_indexid(self, params):
        index_id = params['index_id']
        return True, self.es.get(index='yth_base', doc_type='mytype', id=index_id, _source_exclude=['sm_summary'])

    # -------------------------加入告警到alarm——list-------------------------------------------
    @addHead()
    def add_alarm_list(self, params):

        index_id = params['index_id']
        md5 = params.get('__md5')
        alarmSour = params['__alarmSour']

        def panduan_yth_fileana_isroot():
            """
            判断某个md5条目是否是根（压缩文件或者嵌套文件的根）
            :param md5:条目自身的md5 
            :return: (是否是根节点true/flase ,如果不是根则返回rootmd5 )
            """
            if self.es.exists(index='yth_fileana', doc_type='mytype', id=index_id):
                es_doc = self.es.get(index='yth_fileana', doc_type='mytype', id=index_id,
                                     _source_include=['__md5', '__rootmd5s']).get('_source')
                md5_ = es_doc['__md5']
                rootmd5s_ = es_doc.get('__rootmd5s', [])  # 一个文件有多个父

                if md5_ in rootmd5s_:
                    return [md5_]
                else:
                    return rootmd5s_ if isinstance(rootmd5s_, list) else [rootmd5s_]
            else:
                return []

        def query_yth_base_then_insert_action_list(md5, md5s, connectTime, redPoint):
            # 先查询 yth_base，然后入action_list
            # md5 : 插入action_list的时候，仍然用fileana的MD5，否则无法关联到alarm_list
            # md5s : 可能有多个md5（因为一个文件可能属于多个root md5）

            for md5_ in md5s:
                action_dict = self.query_yth_base_by_md5(md5_, connectTime)
                action_count = action_dict.get('hits').get('total')
                if action_count > 0:
                    action_list = action_dict.get('hits').get('hits')
                    for row in action_list:
                        params_dict = {
                            'yth_base_id': row['_id'],
                            '__md5': md5,
                            'platform': row['_source']['__platform'],
                            'actiontype': row['_source']['__actionType'],
                            'redPoint': redPoint,
                            '__unit': row['_source'].get('__unit', ''),
                            '__connectTime': row['_source']['__connectTime'],

                            'website_info_name': row['_source'].get('website_info_name', ''),
                            'account': row['_source'].get('app_opt', {}).get('account', {}),
                            'url': row['_source'].get('url', ''),
                            'ip': row['_source'].get('ip', ''),
                            'smac': row['_source'].get('smac', ''),
                            'sport': row['_source'].get('sport', ''),
                            '__unitaddr': row['_source'].get('__unitaddr', ''),
                            '__contact': row['_source'].get('__contact', '')
                        }
                        return mc.pro_action_list_add(params_dict)
            return True, ''

        def add_alarm_list(alarmSour):
            if self.es.exists(index='yth_fileana', doc_type='mytype', id=index_id):
                es_doc = self.es.get(index='yth_fileana', doc_type='mytype', id=index_id,
                                     _source_exclude=['__Content-text']).get('_source')
                alarmLevel = 5 if alarmSour == 2 else es_doc['__alarmLevel']
                params_dict = {'yth_fileana_id': index_id, '__md5': es_doc['__md5'],
                               '__connectTime': es_doc['__connectTime'], '__title': es_doc['FileName'],
                               '__alarmLevel': alarmLevel, '__alarmSour': alarmSour, 'summary': es_doc['summary'],
                               '__alarmKey': json.dumps(list(map(
                                   lambda x: {"__keyword": x["__keyword"].replace('"', '\\"'),
                                              "__frequency": x["__frequency"]}, es_doc['__alarmKey']))),
                               '__document': es_doc['__document'],
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
                    md5s = panduan_yth_fileana_isroot()
                    if not query_yth_base_then_insert_action_list(md5, md5s, None, 0)[0]:
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
                    md5s = panduan_yth_fileana_isroot()
                    if not query_yth_base_then_insert_action_list(md5, md5s, result[1], 1)[0]:
                        self.log.error('入库insert_action_list失败')
                        return False, '入库insert_action_list失败'
                else:
                    return False, '存在且被判定为违规,fun_action_list_getLastTime(%s) error' % md5
            elif exists == 1:  # 存在，但未被判定为违规
                # 获取上次时间
                result = mc.fun_action_list_getLastTime(md5)
                if result[0]:
                    # 先查询 yth_base，然后入action_list
                    md5s = panduan_yth_fileana_isroot()
                    if not query_yth_base_then_insert_action_list(md5, md5s, result[1], 0)[0]:
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

    # -------------------------首页统计---------------------------------------------------------

    def tj_yth_base_ruku(self, begin_day, end_day):
        '''
        统计首页的 入库量，告警量违规量处置率（这三个数据来自于mysql）
        :params: 起止日期，格式为yyyy-mm-dd
        :return: 
        '''
        body = {
            "query": {
                "range": {
                    "__connectTime": {
                        "gte": begin_day,
                        "lte": end_day,
                        "format": "yyyy-MM-dd"
                    }
                }
            }
        }
        result = self.es.search('yth_base', 'mytype', body=body, size=0)
        if isinstance(result, dict):
            return result.get('hits', {}).get('total', 0)
        else:
            return 0

    def tj_yth_base_ruku_history_max(self):
        """
        统计入库历史峰值和出现峰值的日期
        :return: 
        """
        body = {
            "size": 0,
            "aggs": {
                "max_day": {
                    "max_bucket": {
                        "buckets_path": "group_by_day.max_count"
                    }
                },
                "group_by_day": {
                    "date_histogram": {
                        "field": "__connectTime",
                        "interval": "1d",
                        "time_zone": "+08:00",
                        "format": "yyyy-MM-dd",
                        "min_doc_count": 0
                    },
                    "aggs": {
                        "max_count": {
                            "value_count": {
                                "field": "_id"}
                        }
                    }
                }
            }
        }
        result = self.es.search('yth_base', 'mytype', body=body, size=0)
        if isinstance(result, dict):
            return result.get('aggregations', {}).get('max_day', {}).get('value', 0)
        else:
            return 0

    def tj_yth_base_ruku_platform(self, begin_day, end_day):
        body = {
            "aggs": {
                "group_by_platform": {
                    "terms": {
                        "field": "__platform"
                    }
                }
            },
            "query": {
                "range": {
                    "__connectTime": {
                        "gte": begin_day,
                        "lte": end_day,
                        "format": "yyyy-MM-dd"
                    }
                }
            }
        }
        result = self.es.search('yth_base', 'mytype', body=body, size=0)

        ruku_platform = {
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0
        }
        buckets = result.get('aggregations', {}).get('group_by_platform', {}).get('buckets', [])
        for bucket in buckets:
            ruku_platform[bucket["key"]] = bucket["doc_count"]
        return ruku_platform

    def tj_yth_base_risk(self, begin_day, end_day):
        body = {
            "aggs": {
                "group_by_risk": {
                    "terms": {
                        "field": "risk"
                    }
                }
            },
            "query": {
                "range": {
                    "__connectTime": {
                        "gte": begin_day,
                        "lte": end_day,
                        "format": "yyyy-MM-dd"
                    }
                }
            }
        }
        result = self.es.search('yth_base', 'mytype', body=body, size=0)

        risk = {
            "0": 0,
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0
        }
        buckets = result.get('aggregations', {}).get('group_by_risk', {}).get('buckets', [])
        for bucket in buckets:
            risk[bucket["key"]] = bucket["doc_count"]
        return risk

    def tj_yth_fileana_security(self, begin_day, end_day):
        body = {
            "aggs": {
                "group_by_security": {
                    "terms": {
                        "field": "__security"
                    }
                }
            },
            "query": {

                "range": {
                    "__connectTime": {
                        "gte": begin_day,
                        "lte": end_day,
                        "format": "yyyy-MM-dd"
                    }
                }
            }

        }
        result = self.es.search('yth_fileana', 'mytype', body=body, size=0)

        risk = {}
        buckets = result.get('aggregations', {}).get('group_by_security', {}).get('buckets', [])
        for bucket in buckets:
            risk[bucket["key"]] = bucket["doc_count"]
        return risk

    def tj_frontpage_summary(self, today, yesterday, monday, firstdayofmonth, cfg_begin_day, diff_days):
        '''
        首页统计
        :param params:起止时间（仅针对下半部分） 
        :return: 
        '''

        summary = {
            "入库量": {
                "今日": 0,
                "昨日": 0,
                "本周": 0,
                "本月": 0,
                "日均": 0,
                "峰值": 0
            }
        }

        # 今天

        begin_time = today
        end_time = today
        ruku_today = self.tj_yth_base_ruku(begin_time, end_time)
        summary["入库量"]['今日'] = ruku_today

        # 昨天
        begin_time = yesterday
        end_time = yesterday
        ruku_yesterday = self.tj_yth_base_ruku(begin_time, end_time)
        summary["入库量"]['昨日'] = ruku_yesterday

        # 本周
        begin_time = monday
        end_time = today
        ruku_week = self.tj_yth_base_ruku(begin_time, end_time)
        summary["入库量"]['本周'] = ruku_week

        # 本月
        begin_time = firstdayofmonth
        end_time = today
        ruku_month = self.tj_yth_base_ruku(begin_time, end_time)
        summary["入库量"]['本月'] = ruku_month

        # 每日平均,先从配置文件获取起始日期begin_day
        ruku_day_avg = self.tj_yth_base_ruku(cfg_begin_day, today) / diff_days
        summary["入库量"]['日均'] = ruku_day_avg

        # 历史峰值
        ruku_day_max = self.tj_yth_base_ruku_history_max()
        summary["入库量"]['峰值'] = ruku_day_max

        return summary

    @addHead()
    def tj_frontpage_all(self, params):
        """
        
        :param params:包含用户自定义的起止时间 
        :return: 
        """

        from app.utils.common import today
        from app.utils.common import yesterday
        from app.utils.common import monday
        from app.utils.common import firstdayofmonth
        today = today()
        yesterday = yesterday()
        monday = monday()
        firstdayofmonth = firstdayofmonth()
        from app.utils.common import diffday
        cfg_begin_day = Config.begin_day
        diff_days = diffday(cfg_begin_day, today) + 1

        begin_day = params['begin_day']
        end_day = params['end_day']

        all = {
            "平台概况": {
                "平台数": 4,
                "告警量": {
                    "今日": 0,
                    "昨日": 0,
                    "本周": 0,
                    "本月": 0,
                    "日均": 0,
                    "峰值": 0
                },
                "入库量": {
                    "今日": 0,
                    "昨日": 0,
                    "本周": 0,
                    "本月": 0,
                    "日均": 0,
                    "峰值": 0
                },
                "处置率": {
                    "今日": 0,
                    "昨日": 0,
                    "本周": 0,
                    "本月": 0,
                    "日均": 0,
                    "峰值": 0
                },
                "违规量": {
                    "今日": 0,
                    "昨日": 0,
                    "本周": 0,
                    "本月": 0,
                    "日均": 0,
                    "峰值": 0
                }
            },
            "入库分析": {
                "入库总量": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0
                }
            },
            "告警分析": {
                "告警量": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0
                },
                "违规量": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0
                },
                "处置量": {
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0
                }
            },
            "密级vs": {
                "上报": {
                    "2": 0,
                    "3": 0,
                    "4": 0
                },
                "平台": {
                    "2": 0,
                    "3": 0,
                    "4": 0
                }
            }
        }

        # 平台概况
        err, summary_my, alarm_ana = mc.tj_frontpage_alarm_list(today, yesterday, monday, firstdayofmonth, diff_days,
                                                                begin_day, end_day)
        summary_es = self.tj_frontpage_summary(today, yesterday, monday, firstdayofmonth, cfg_begin_day, diff_days)

        if err:
            summary_my["入库量"] = summary_es.get("入库量")
            summary = summary_my
        else:
            summary = summary_es

        all["平台概况"] = summary

        # 入库总量
        ruku_platform = self.tj_yth_base_ruku_platform(begin_day, end_day)
        all["入库分析"]["入库总量"] = ruku_platform

        # 告警分析
        all["告警分析"] = alarm_ana

        # 密级
        risk = self.tj_yth_base_risk(begin_day, end_day)
        all["密级vs"]["上报"] = risk

        security = self.tj_yth_fileana_security(begin_day, end_day)
        all["密级vs"]["平台"] = security

        return err, all


ec = ESClient()
