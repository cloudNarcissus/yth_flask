from elasticsearch import Elasticsearch
from elasticsearch_dsl import query, aggs, function
import time

from app.config import Config

class ESClient(object):
    def __init__(self, hosts):
        self.es = Elasticsearch(hosts=hosts)


    def search(self):
        body ={
            "query": {
                "query_string": {
                    "default_field": "_platforms",
                    "query": 1
                }},
            "_source": {
                "includes": ["__alarmKey"]
            }

        }
        return self.es.search('yth_fileana', 'mytype', body, size=10)

    def tj_yth_base_ruku(self,begin_time,end_time):
        '''
        统计首页的 入库量，告警量违规量处置率（这三个数据来自于mysql）
        :params: 起止日期，格式为yyyy-mm-dd
        :return: 
        '''
        body = {
            "query": {
                "range": {
                    "__connectTime": {
                        "gte": begin_time,
                        "lte": end_time,
                        "format": "yyyy-MM-dd"
                    }
                }
            }
        }
        result = self.es.search('yth_base', 'mytype', body=body,size=0)
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
        result= self.es.search('yth_base', 'mytype', body=body, size=0)
        if isinstance(result, dict):
            return result.get('aggregations', {}).get('max_day',{}).get('value',0)
        else:
            return 0

    def tj_frontpage(self):
        '''
        首页统计
        :param params:起止时间（仅针对下半部分） 
        :return: 
        '''

        from app.utils.common import today
        from app.utils.common import yesterday
        from app.utils.common import monday
        from app.utils.common import firstdayofmonth


        # 今天
        today = today()
        begin_time = today
        end_time = today
        ruku_today =self.tj_yth_base_ruku(begin_time, end_time)

        # 昨天
        begin_time = yesterday()
        end_time = yesterday()
        ruku_yesterday = self.tj_yth_base_ruku(begin_time, end_time)

        # 本周
        begin_time = monday()
        end_time = today
        ruku_week = self.tj_yth_base_ruku(begin_time, end_time)

        # 本月
        begin_time = firstdayofmonth()
        end_time = today
        ruku_month = self.tj_yth_base_ruku(begin_time, end_time)

        # 每日平均,先从配置文件获取起始日期begin_day
        from app.utils.common import diffday
        begin_day = Config.begin_day
        diff_day = diffday(begin_day, today)
        ruku_avg_day = self.tj_yth_base_ruku(begin_day, today) / (diff_day+1)

        # 历史峰值
        ruku_max_history =self.tj_yth_base_ruku_history_max()


        print(ruku_max_history)

if __name__ == '__main__':

    es_client = ESClient('192.168.10.136:9200')
    es_client.tj_frontpage()
