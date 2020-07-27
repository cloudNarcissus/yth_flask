
host=127.0.0.1
port=9200
echo 'delete table yth_base'
curl -XDELETE "http://${host}:${port}/yth_base"
echo 'create table yth_base'
curl -XPUT "http://${host}:${port}/yth_base" -H 'Content-Type: application/json' -d'
{
	"settings": {
		"index": {
			"number_of_shards": 3,
			"similarity": {
				"my_bm25": {
					"type": "BM25",
					"b": "0.75",
					"k1": "1.2"
				}
			}
		},
		"analysis": {
			"normalizer": {
					"my_lowercase": {
					"type": "custom",
					"filter": ["lowercase", "asciifolding"]
				}
			}
		}

	},
	"mappings": {
		"mytype": {
			"properties": {
				"__connectTime": {
					"type": "date",
					"format": "yyyy-MM-dd HH:mm:ss.SSS||yyyy-MM-dd HH:mm:ss.SS||yyyy-MM-dd HH:mm:ss.S||yyyy-MM-dd HH:mm:ss"
					
				},
				"__bornTime": {
					"type": "date",
					"format": "yyyy-MM-dd HH:mm:ss.SSS||yyyy-MM-dd HH:mm:ss.SS||yyyy-MM-dd HH:mm:ss.S||yyyy-MM-dd HH:mm:ss"
					
				},
				"__platform": {
					"type": "integer"
					
				},
				"__actionType": {
					"type": "keyword",
					"normalizer": "my_lowercase"
				},
				"__md5": {
					"type": "keyword"
					
				},
				"sip": {
					"type": "ip",
					"copy_to": "__full_query"
				},
				"dip": {
					"type": "ip",
					"copy_to": "__full_query"
				},
				"ip": {
					"type": "ip",
					"copy_to": "__full_query"
				},
				"smac": {
					"type": "keyword"
				},
				"dmac": {
					"type": "keyword"
				},
				"mac": {
					"type": "keyword"
				},
				"hostname": {
					"type": "keyword"
					
				},
				"__summary": {
					"type": "text",				
					"similarity": "my_bm25",
					"analyzer": "ik_max_word"
				},
				"_interested": {
					"type": "boolean"
					
				},
				"_interested_time": {
					"type": "date",
					
					"format": "yyyy-MM-dd HH:mm:ss.SSS||yyyy-MM-dd HH:mm:ss.SS||yyyy-MM-dd HH:mm:ss.S||yyyy-MM-dd HH:mm:ss"
				},
				"_existsfile": {
					"type": "boolean"
					
				},
				"_alarmed": {
					"type": "boolean"
					
				},
				"__full_query": {
					"type": "text",
					"analyzer": "ik_max_word"
				},
				"app_opt": {
					"properties": {
						"account": {
							"type": "keyword",
							"copy_to": "__full_query"
						},
						"domain": {
							"type": "keyword",
							"copy_to": "__full_query"
						},
						"receiver": {
							"type": "keyword",
							"copy_to": "__full_query"
						},
						"sender": {
							"type": "keyword",
							"copy_to": "__full_query"
						},
						"subject": {
							"type": "keyword",
							"copy_to": "__full_query"
						},
						"url": {
							"type": "keyword"
						}
					}
				},
				"mainlicense": {
					"type": "keyword"
					
				},
				"FileName": {
					"type": "keyword",
					"copy_to": "__full_query"
				},
				"__unit": {
					"type": "keyword"
					
				},
				"__unitaddr": {
					"type": "keyword"
					
				},
				"__contact": {
					"type": "keyword"
					
				}
			}
		}
	}
}'

echo 'delete table yth_fileana'
curl -XDELETE "http://${host}:${port}/yth_fileana"
echo 'delete table yth_fileana'
curl -XPUT "http://${host}:${port}/yth_fileana" -H 'Content-Type: application/json' -d'
{
	"settings": {
		"index": {
			"number_of_shards": 3,
			"similarity": {
				"my_bm25": {
					"type": "BM25",
					"b": "0.75",
					"k1": "1.2"
				}
			}
		}
	},
	"mappings": {
		"mytype": {
			"properties": {
				"FileExt": {
					"type": "text",
					"fields": {
						"keyword": {
							"type": "keyword",
							"ignore_above": 256
						}
					}
				},
				"FileName": {
					"type": "text"	,				
					"similarity": "my_bm25",
					"analyzer": "ik_max_word"
					
				},
				"Filelength": {
					"type": "long"
					
				},
				"__Content-text": {
					"type": "text"	,				
					"similarity": "my_bm25",
					"analyzer": "ik_max_word"
				},
				"__md5": {
					"type": "keyword"
					
				},
				"__rootmd5s": {
					"type": "keyword"
				},				
				"__alarmKey": {
					"type":"nested",
					   "properties": {
						 "__keyword":{ "type" :"keyword"},
						 "__frequency":{ "type" :"integer"},
						 "__position":{"type": "text"}
					   }
				},
				"__connectTime": {
					"type": "date",					
					"format": "yyyy-MM-dd HH:mm:ss.SSS||yyyy-MM-dd HH:mm:ss.SS||yyyy-MM-dd HH:mm:ss.S||yyyy-MM-dd HH:mm:ss"
				},		
				
				"__document": {
					"type": "keyword"
					
				},				
				
				"__industry": {
					"type": "text",
					
					"term_vector": "with_positions_offsets",
					"fields": {
						"raw": {
							"type": "keyword"
							
						}
					},
					"analyzer": "whitespace",
					"fielddata": true
				},
				"__security": {
					"type": "keyword"
					
				},
				"__tikaExtention": {
					"type": "keyword"
					
				},								
				"_interested": {
					"type": "boolean"
					
				},
				"_interested_time": {
					"type": "date",
					
					"format": "yyyy-MM-dd HH:mm:ss.SSS||yyyy-MM-dd HH:mm:ss.SS||yyyy-MM-dd HH:mm:ss.S||yyyy-MM-dd HH:mm:ss"
				},				
				"summary": {
					"type": "keyword",
					"index": false					
				},
				"_alarmed": {
					"type": "boolean"					
				},
				"__alarmLevel": {
					"type": "integer"
					
				},
				"_platforms": {
					"type": "integer"
					
				},
				"__alarmType": {
					"type": "integer"
					
				}
			}
		}
	}
}'

echo 'delete table yth_raroot'
curl -XDELETE "http://${host}:${port}/yth_raroot"
echo 'delete table yth_raroot'
curl -XPUT "http://${host}:${port}/yth_raroot" -H 'Content-Type: application/json' -d'
{	
	"mappings": {
		"mytype": {
			"properties": {
				"__rootmd5": {
					"type": "keyword"
				},
				"FileName": {
					"type": "keyword"
				},
				"FilePaths": {
					"type":"nested",
					   "properties": {
						 "__md5":{ "type" :"keyword"},
						 "path":{ "type" :"keyword"},
						 "__alarmLevel":{"type": "integer"}
					   }
				}
			}
		}
	}
}'
