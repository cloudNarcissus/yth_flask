from elasticsearch import Elasticsearch
from elasticsearch_dsl import query, aggs, function
import time




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

    def tj_yth_base_ruku(self,params):
        '''
        统计首页的 入库量，告警量违规量处置率（这三个数据来自于mysql）
        :params: 起止日期，格式为yyyy-mm-dd
        :return: 
        '''
        begin_time = params['begin_time']
        end_time = params['end_time']

        body={
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
        return self.es.search('yth_base', 'mytype', body=body,size=0)

if __name__ == '__main__':

    es_client = ESClient('192.168.10.136:9200')
    re = es_client.tj_yth_base_ruku({"begin_time":"2019-07-08","end_time":"2019-07-08"})

    print(re)
