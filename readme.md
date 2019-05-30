# 概述
四、接口说明
4.1查询字典数据
Url:/v1.0/get_dict/
方法：GET
返回：[{\"key\": \"", \"remark\": null, \"type\": \"actiontype\", \"value\": \""},...]
4.2查询行为数据
Url：/v1.0/action/
Body:
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
方法：POST

4.3查询文档数据
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
('__actionType', type=str)
方法：post
4.4关注某条数据
Url:/v1.0/interested/
方法：post
('index_name', type=str)
('index_id', type=str)
('interested_or_cancel', type=str)

4.5对rar或者嵌套文件，查询其子文件
Url:/v1.0/rarchildren/
方法：post
('rootmd5', type=str)