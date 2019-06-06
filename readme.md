# 概述
## 四、接口说明

### 4.1查询字典数据

Url:/v1.0/get_dict/

方法：GET

返回：[{\"key\": \"", \"remark\": null, \"type\": \"actiontype\", \"value\": \""},...]

### 4.2查询行为数据

Url：/v1.0/action/

Body:
```json
{
"begin_time":"2019-05-16", 
"end_time":"2019-05-27", 
"time_format":"yyyy-MM-dd",
"match_str":"国家", 
"exact_query":0,
"order":"__bornTime",
"orderType":"desc",
"size":10,
"from":0,
}
```

方法：POST

### 4.3查询文档数据
Url：/v1.0/fileana/

('begin_time', type=str)

('end_time', type=str)

('time_format', type=str)

('__md5', type=str)

('__security',type=str)

('__document', type=str) #公文

('__industry', type=str) #行业(list)

('match_str', type=str)

('exact_query', type=int)

('_platform', type=int)

('__alarmKey', type=str)#关键字list

('order', type=str)

('orderType', type=str)

('size', type=int, required=True)

('from', type=int, required=True)


方法：post

### 4.4关注某条数据

Url:/v1.0/interested/

方法：post

('index_name', type=str)

('index_id', type=str)

('interested_or_cancel', type=str)

### 4.5对rar或者嵌套文件，查询其子文件

Url:/v1.0/rarchildren/

方法：post

('__rootmd5', type=str)

### 4.6在文档页面，加入告警

Url:/v1.0/fileana/alarm

参数：

{

“index_id”:文档的_id，

“__md5”:文件md5

“__alarmSour”：后台填1  手动UI填2

}


### 4.7在文档页面，查看相似文档

URL：

/v1.0/fileana/simdoc

参数：

{

“index_id”:文档的_id，

“__md5”:文件md5

}

方法 POST


### 4.8 查询告警清单

URL：

/v1.0/alarmlist/

参数：

{


begin_day  date, -- 2019-06-04

end_day  date,

alarmlevel_query  varchar(10), -- 等于5：=5  大于3：>=3  等于全部：'' 没有大于全部小于全部

fulltext_query text, -- 关键字查询

platform  int,  -- 0全部  1234    这个字段就是页面上的告警分类

__alarmSour int,  -- 告警来源0:全部 1：告警模型  2：手动加入

cz_status  int , -- 1:待处置 2：已处置  3：违规  0:无此查询

_interested int, -- 0: 全部  1：关注  2：未关注


orderby varchar(30), -- __alarmLevel/__connectTime/__alarmTime + asc /desc

page_capa  int , -- 每页的容量（400）

page_num  int -- 跳页数（ 首页为0 ，第二页是1 ）

}

方法 POST
/v1.0/alarmlist/


### 4.9 查询左侧统计切换区

URL: /v1.0/alarmlist/left

参数：

{


begin_day  date, -- 2019-06-04

end_day  date,

alarmlevel_query  varchar(10), -- 等于5：=5  大于3：>=3  等于全部：'' 没有大于全部小于全部

fulltext_query text, -- 关键字查询

platform  int,  -- 0全部  1234    这个字段就是页面上的告警分类

__alarmSour int,  -- 告警来源0:全部 1：告警模型  2：手动加入

}


### 4.10 查询行为追踪

url：/v1.0/actionlist/

参数：

__md5 







