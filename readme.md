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
"from":0
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
    parser.add_argument('_interested', type=bool)
    

方法：POST

### 4.3查询文档数据
Url：/v1.0/fileana/

```
('begin_time', type=str)

('end_time', type=str)

('time_format', type=str)
parser.add_argument('__connectTime', type=bool)

('__md5', type=str)

('__security',type=str)

('__document', type=str) #公文

('__industry', type=str) #行业"__industry":[ {"key":"行业"}]

('match_str', type=str)

('exact_query', type=int)

('_platform', type=int)

('__alarmKey', type=str)#关键字"__alarmKey":[ {"key":"\"地区\""}]

('order', type=str)

('orderType', type=str)

('size', type=int, required=True)

('from', type=int, required=True)



parser.add_argument('_interested', type=bool)

parser.add_argument('_alarmed', type=bool)
```

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

('__md5', type=str) 

注意：当条记录的md5

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
    
    __alarmType int , -- 0:全部 其他见字典
    
    orderby varchar(30), -- __alarmLevel/__connectTime/__alarmTime + asc /desc
    
    page_capa  int , -- 每页的容量（400）
    
    page_num  int -- 跳页数（ 首页为0 ，第二页是1 ）,
    
    
    
     '__security', type=str -- 密级
     '__alarmKey', type=str) -- 关键字
    
    }

方法 POST
/v1.0/alarmlist/


### 4.9 查询左侧统计切换区

URL: /v1.0/alarmlist/left

参数：

{


        parser.add_argument('begin_day', type=str, required=True)
        parser.add_argument('end_day', type=str, required=True)
        parser.add_argument('alarmlevel_query', type=str)
        parser.add_argument('fulltext_query', type=str)
        parser.add_argument('actiontype', type=str)
        parser.add_argument('__alarmType', type=int)
        parser.add_argument('__alarmSour', type=int)
        parser.add_argument('_interested', type=int) -- 0: 全部  1：关注  2：未关注
        '__security', type=str -- 密级
     '__alarmKey', type=str) -- 关键字
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


post


### 4.13 查询处置历史清单

url: /v1.0/czlist/


参数：__md5 


方法：post



### 4.14 添加事件（同时关联行为） 

url ： /v1.0/eventlist

方法：post

        parser = reqparse.RequestParser()
        __md5  
        parser.add_argument('event_id', type=str, required=True)#事件编号
        parser.add_argument('event_name', type=str, required=True)#事件名
        parser.add_argument('event_type', type=int, required=True)# 字典里有
        #
        # 1       违规外联
        # 2       互联网传输泄密
        # 3       网络攻击窃密
        # 4       违规存储 / 处理涉密信息
        #
        parser.add_argument('event_miji', type=str, required=True)#字典里有
        parser.add_argument('event_status', type=int, required=True) #字典里有 1.待处理 2.不移交  3移交未反馈  4移交已反馈
        parser.add_argument('content', type=str, required=True) # 内容 显示 文件名 或者 违规外联描述
        parser.add_argument('remark', type=str)# 备注
        parser.add_argument('add_user', type=str, required=True)  # 添加者
        parser.add_argument('report', type=str, required=True)  # 这是ui自行组织的json，用于打印报告


### 4.15 查询全部关注数据

```
GET /v1.0/interested/list
```
请求参数
* index_name:数据类型（索引名），取值为：`yth_fileana`或`yth_base`
* from:从第多少条记录开始返回
* size:最大返回记录条数



### 4.16 查询单个文件的内容，用以生成预览

```
GET /v1.0/fileana/view/
```
请求参数
* __md5 : 文件的md5


### 4.17 下载文件


```
GET /v1.0/filedownload/
```
请求参数
* __md5 : 文件的md5
* filename: 从行为列表返回的filename

返回：

正常情况：返回response,其中的

异常情况：返回
```json
{
   'message': 错误信息,
   'data': None
}

```



### 4.14 查询事件列表 

url ： /v1.0/eventlist/

方法：get

        
        parser.add_argument('__md5', type=str, required=True)  # 告警的md5
        parser.add_argument('begin_day', type=str, required=True)  # 事件编号
        parser.add_argument('end_day', type=str, required=True)  # 事件名
        parser.add_argument('event_type', type=int)  # 字典里有 , 默认0或不传
        #
        # 1       违规外联
        # 2       互联网传输泄密
        # 3       网络攻击窃密
        # 4       违规存储 / 处理涉密信息
        #
        parser.add_argument('event_miji', type=str)  # 字典里有 默认不传
        parser.add_argument('event_status', type=int)  #默认0，或不传 字典里有 1.待处理 2.不移交  3移交未反馈  4移交已反馈
        parser.add_argument('fulltext_query', type=str)  # 关键字查询(事件名 违规内容 备注)
        parser.add_argument('page_capa', type=int, required=True)  # 每页的容量（400）
        parser.add_argument('page_num', type=int, required=True)  # 跳页数（ 首页为0 ，第二页是1 ）
        

### 4.15 关注告警清单

url: post /alarmlist/interested/

```buildoutcfg
        parser.add_argument('__md5', type=str, required=True)
        parser.add_argument('_interested', type=bool, required=True)
```



### 4.16 添加关键字

url: post /keyword/

```buildoutcfg
        parser.add_argument('keyword', type=str, required=True)  # 关键字、正则表达式
        parser.add_argument('keylevel', type=str, required=True)  # 等级
        parser.add_argument('enabled', type=bool, required=True)  # true false
        parser.add_argument('remark', type=str, required=True)  # 备注
        parser.add_argument('add_user', type=str, required=True)  # 添加者
        parser.add_argument('keytype', type=int, required=True,choices=[1,2])  # 1:关键词  2：正则表达式

```


### 4.17 查询关键字

url: get /keyword/

```buildoutcfg
	begin_day  date,
	end_day		 date,
	keylevel     int ,  -- 0:全部  1-5：其他等级
	enabled			bool, -- true / false 
	keyword    varchar(100),-- '':空串不加入该条件   
	last_keylevel int, -- 只有在告警等级排序的时候，才传这个值，否则传0
	last_auid  int, -- 0:首次  >0：上一页最大id
	page_count  int , -- 每页数量
	order_by  varchar(10), --  asc/desc  
	keytype   int -- 0 : 无此条件  1：关键字  2正则表达式
```


### 4.18 创建event_id

url :   get /eventid/

无参数


### 4.19 更新事件


飒飒|撒|统一
---|---|---
是多少|有一条

---

url:  put /eventlist/

```buildoutcfg
        parser.add_argument('event_id', type=str, required=True)  # 事件编号
        parser.add_argument('event_name', type=str, required=True)  # 事件名
        parser.add_argument('event_type', type=int, required=True)  # 字典里有
        #
        # 1       违规外联
        # 2       互联网传输泄密
        # 3       网络攻击窃密
        # 4       违规存储 / 处理涉密信息
        #
        parser.add_argument('event_miji', type=str, required=True)  # 字典里有
        parser.add_argument('event_status', type=int, required=True)  # 字典里有 1.待处理 2.不移交  3移交未反馈  4移交已反馈
        parser.add_argument('remark', type=str)  # 备注
        parser.add_argument('add_user', type=str, required=True)  # 添加者
```


### 4.20 删除事件

url: delete /eventlist/

```buildoutcfg
    parser.add_argument('event_id', type=str, required=True)  # 事件编号

```


### 4.21 查询轨迹的详细

url : get /action/one/

```buildoutcfg

parser.add_argument('index_id', type=str)
parser.add_argument('__md5', type=str) #在告警清单，子条目点详细时，需要传这个参数，用来查询doc_summary
```


### 4.22 更新关键字

url :  put /keyword/

```
        parser = reqparse.RequestParser()
        parser.add_argument('auid', type=int, required=True)  # 关键字id
        parser.add_argument('keyword', type=str, required=True)  # 关键字、正则表达式
        parser.add_argument('keylevel', type=str, required=True)  # 等级
        parser.add_argument('enabled', type=int, required=True)  # -1 0  1
        parser.add_argument('remark', type=str, required=True)  # 备注
        parser.add_argument('add_user', type=str, required=True)  # 添加者
        parser.add_argument('keytype', type=int, required=True, choices=[1, 2])  # 1:关键词  2：正则表达式
        
        
```


### 4.23 删除关键字

url: delete /keyword/

```
   
        parser.add_argument('auid', type=int, required=True)  # 关键字id
  
        
```



### 4.24 批量添加关键字

url ： post /keyword/batch/


```buildoutcfg
 parser.add_argument('keywords', type=str, required=True)  # 若干关键字组成的json串[{},{}]
```






### 4.25 首页统计过

url ： get /tj/frontpage/


```buildoutcfg
 parser.add_argument('begin_day', type=str, required=True)  # 2019-07-01
        parser.add_argument('end_day', type=str, required=True)  # 2019-07-11
```



### 4.26 根据md5查询fileana的详细

url:  get /fileana/one/
```buildoutcfg

parser.add_argument('__md5', type=str, required=True)
```



### 4.27 根据md5查询轨迹

url:  get /action/guiji/
```buildoutcfg

parser.add_argument('__md5', type=str, required=True)
```


### 4.28 平台的修改和查询 

url : 这两个接口都是用   /platform/
只是调用方法不一样，修改是Post  查询是get

修改的参数：
```buildoutcfg
parser.add_argument('platformid',type=int, required=True)  # 平台id
        parser.add_argument('name',type=str, required=True)  # 名称
        parser.add_argument('nicname',type=str, required=True)  # 别名
        parser.add_argument('simname',type=str, required=True)  # 简称
```

查询不需要参数



### 4.29 华哥添加三合一告警


post  /alarmlist/add/ (加上前缀为：http://192.168.12.38:10086/v1.0/alarmlist/add/)


```buildoutcfg
        parser.add_argument('yth_fileana_id', type=str)
        parser.add_argument('__md5', type=str,)
        parser.add_argument('__connectTime', type=str)
        parser.add_argument('__title', type=str)
        parser.add_argument('__alarmLevel', type=int)
        parser.add_argument('summary', type=str)
        parser.add_argument('__alarmKey', type=str)
        parser.add_argument('__document', type=str)
        parser.add_argument('__industry', type=str)
        parser.add_argument('__security', type=str)
        parser.add_argument('__ips', type=str)
        parser.add_argument('__alarmType', type=int)
```


## 五、大屏接口说明

注意：大屏的URL前缀为： /ls/v1.0/

### 5.1查询告警类型分布

get  /alarmtype/ (加上前缀为：http://192.168.10.10:10086/ls/v1.0/alarmtype/)

```buildoutcfg

parser.add_argument('begin_day', type=int, required=True)  # 起始时间
parser.add_argument('end_day', type=int,required=True)      # 结束时间

parser.add_argument('province', type=str) #省编码（6位）
parser.add_argument('city', type=str)  # 市编码（6）
parser.add_argument('district',type=str)  # 区编码（6）

```

### 5.2 告警级别分布 及 处置情况 （有3个图）

get  /alarmtypelevel/ (加上前缀为：http://192.168.10.10:10086/ls/v1.0/alarmtypelevel/)

```buildoutcfg
parser.add_argument('begin_day', type=int, required=True)  # 起始时间
parser.add_argument('end_day', type=int,required=True)      # 结束时间

parser.add_argument('province', type=str) #省编码（6位）
parser.add_argument('city', type=str)  # 市编码（6）
parser.add_argument('district',type=str)  # 区编码（6）

```


### 5.3 告警处置趋势

get  /alarmcztrend/ (加上前缀为：http://192.168.10.10:10086/ls/v1.0/alarmcztrend/)

```buildoutcfg
parser.add_argument('begin_day', type=int, required=True)  # 起始时间
parser.add_argument('end_day', type=int,required=True)      # 结束时间

parser.add_argument('province', type=str) #省编码（6位）
parser.add_argument('city', type=str)  # 市编码（6）
parser.add_argument('district',type=str)  # 区编码（6）
```

### 5.4 异常数据密级分布

get  /alarmczstatus/ (加上前缀为：http://192.168.10.10:10086/ls/v1.0/alarmczstatus/)

```buildoutcfg
parser.add_argument('begin_day', type=int, required=True)  # 起始时间
parser.add_argument('end_day', type=int,required=True)      # 结束时间

parser.add_argument('province', type=str) #省编码（6位）
parser.add_argument('city', type=str)  # 市编码（6）
parser.add_argument('district',type=str)  # 区编码（6）
```


### 5.5 中央地图告警处置分布


get  /alarmmap/ (加上前缀为：http://192.168.10.10:10086/ls/v1.0/alarmmap/)

```buildoutcfg

parser.add_argument('begin_day', type=int, required=True)  # 起始时间
parser.add_argument('end_day', type=int,required=True)      # 结束时间

parser.add_argument('province', type=str) # 这个参数目前不应该为空串
parser.add_argument('city', type=str)  # 这个参数若不是空串，意味着查询某个市的下属区 ; 若这个参数是空串，则意味着查询某个省下属的市
parser.add_argument('district',type=str)  # 这个参数应该永远传空串


```


### 5.6 事件趋势

get /eventtrend/

```buildoutcfg
parser.add_argument('begin_day', type=int, required=True)  # 起始时间
parser.add_argument('end_day', type=int,required=True)      # 结束时间

parser.add_argument('province', type=str) #省编码（6位）
parser.add_argument('city', type=str)  # 市编码（6）
parser.add_argument('district',type=str)  # 区编码（6）
```



### 5.7 事件类型-密级分布图


get /eventmijitype/

```buildoutcfg
parser.add_argument('begin_day', type=int, required=True)  # 起始时间
parser.add_argument('end_day', type=int,required=True)      # 结束时间

parser.add_argument('province', type=str) #省编码（6位）
parser.add_argument('city', type=str)  # 市编码（6）
parser.add_argument('district',type=str)  # 区编码（6）
```




