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

    parser.add_argument('begin_time', type=str)
    parser.add_argument('end_time', type=str)
    parser.add_argument('time_format', type=str)
    parser.add_argument('match_str', type=str)
    parser.add_argument('exact_query', type=bool)
    parser.add_argument('order', type=str)
    parser.add_argument('orderType', type=str)
    parser.add_argument('size', type=int, required=True)
    parser.add_argument('from', type=int, required=True)
    parser.add_argument('__actionType', type=str)
    

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

('__rootmd5s', type=str) 

注意：__rootmd5s不止一个md5，这是多个md5构成的列表（数组），每一个root对应一棵树

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

actiontype  char(20),  -- 
'' 全部   行为类型  代替 “来源”

 /*

http	056-网页发布  

im	056-即时通讯

netdisk	056-网盘

email	056-电子邮件

filetransfer	056-文件传输

other	056-其他

csmp	三合一

docaudit	文档审计

website	门户网站
*/

__alarmSour int,  -- 告警来源 代替告警产生  0:全部 1：告警模型  2：手动加入

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



### 4.11 处置告警
url : '/v1.0/alarmlist/cz'

参数：


        parser.add_argument('cz_user', type=str, required=True) #处置用户
        parser.add_argument('cz_status', type=str,required=True) # NO: 未处置  PASS：处置为正常  JIMI: 处置为机密   MIMI: 处置为秘密    JUEMI：处置为绝密
        parser.add_argument('__md5', type=str,required=True)
        parser.add_argument('cz_summary', type=str, required=True) #涉密摘要 （处置摘要），改为正常的话要值为空
        parser.add_argument('cz_detail', type=str, required=True) #ui自行组织字段，用于在历史记录里面显示的



### 4.12 告警中心统计页面查询

url： /v1.0/alarmlist/tj

参数：

起始日期

parser.add_argument('begin_day', type=str, required=True)

结束时间 

parser.add_argument('end_day', type=str, required=True)

