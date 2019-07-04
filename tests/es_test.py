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
                "excludes": ["__Content-text", "summary", "file_summary"]
            }

        }
        return self.es.search('yth_fileana', 'mytype', body, size=10)



if __name__ == '__main__':

    es_client = ESClient('192.168.10.136:9200')
    print(type(es_client.search()['hits']['hits'][0]['_source']['__rootmd5s']))
