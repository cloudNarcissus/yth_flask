# yth_alarm数据库存储过程文档【mysql】

PS：没有明确标明含义的输入输出参数，有两种可能性：一是该字段是自解释的，比如mac、sip等；二是该字段在model设计文档中有明确的定义，不再赘述。因此需要结合mode设计文档来查阅此文档。

## pro_action_list_add

### 用途

添加轨迹追踪

### 输入

```sql
create PROCEDURE pro_action_list_add(
i_yth_base_id varchar(25), #es 中 yth_base的doc_id，可以此关联到es表
i___md5   varchar(50), 
i_platform int, 
i_actiontype char(20),
i_redPoint int, #是否有红点(0,1)
i_unit  varchar(50),
i___connectTime datetime,
i_website_name varchar(100), #网站名称
i_account varchar(50), #账号名称
i_url varchar(100),
i_ip  varchar(200),
i_smac varchar(50),
i_sport varchar(50),
i_unitaddr varchar(100),
i_contact  varchar(100),
i___bornTime datetime #原始数据时间
)
```

### 输出

NULL



## pro_action_list_query

### 用途

查询轨迹追踪

### 输入

```sql
CREATE DEFINER=`root`@`%` PROCEDURE `pro_action_list_query`(
# 查询轨迹追踪（子条目action）
i___md5  varchar(50)  #alarm_list的md5
)
```

### 输出

结果集：action_list 全字段




## pro_alarm_list_add

### 用途

添加告警清单主条目

### 输入

```sql
CREATE DEFINER=`root`@`%` PROCEDURE `pro_alarm_list_add`(
# 加入告警
i_yth_fileana_id varchar(25), #es 中 yth_fileana的doc_id，可以此关联到es表
i___md5   varchar(50),  # 文件md5  用于检测唯一性的

i___connectTime datetime, #接入时间
i___title   varchar(100),#标题
i___alarmLevel int ,#告警等级 1-5, 手动加入默认为5
i___alarmSour int, #告警来源 1：告警模型  2：手动加入
i_summary text, #显示的摘要

i___alarmKey text,  #关键字 JSON格式 同es
i___document text,  #公文 JSON格式 同es
i___industry text,  #行业 JSON格式 同es
i___security text,  #密级 JSON格式 同es


i___ips  varchar(100),
i___alarmType int # 1:违规外联

)
```

### 输出

NULL


## pro_alarm_list_cz

### 用途

处置告警

### 输入

```sql
CREATE DEFINER=`root`@`%` PROCEDURE `pro_alarm_list_cz`(
# 处置告警
i_cz_user varchar(50),
i___md5   varchar(50),
i_cz_status  char(10), -- NO:未处置  PASS：处置为正常  JIMI:处置为机密 MIMI:处置为秘密  JUEMI：处置为绝密
i_cz_summary  text, -- 涉密摘要 （处置摘要）
i_cz_detail  text -- ui自行组织字段，用于在历史记录里面显示的
)
```

### 输出
NULL



## pro_alarm_list_interested

### 用途

关注告警

### 输入

```sql
CREATE DEFINER=`root`@`%` PROCEDURE `pro_alarm_list_interested`(
# 关注告警
i___md5   varchar(50),
i__interested  bool  # true  flase 
)
```

### 输出
NULL




## pro_alarm_list_left

### 用途

统计切换区的查询

### 输入

```sql
CREATE DEFINER=`root`@`%` PROCEDURE `pro_alarm_list_left`(
# 统计切换区
i_begin_day  date, -- 2019-06-04
i_end_day  date,
i_alarmlevel_query  varchar(10), -- 等于5：=5  大于3：>=3  等于全部：'' 没有大于全部小于全部
i_fulltext_query text, -- 关键字查询
i_actiontype  char(20),  -- '':全部  行为类型
i___alarmType int,-- 1,2,3,4 0:全部

i___alarmSour int,  -- 告警来源0:全部 1：告警模型  2：手动加入
i__interested int,
i___security  varchar(50),  #密级
i___alarmKey  varchar(50)   #关键字
)
```

### 输出
```buildoutcfg
select @NO_count as NO_count , #待处置
@YES_count as YES_count,#已处置
@DANGER_count as DANGER_count,#违规
@INTRESTED_count as NTRESTED_count;#关注
```


## pro_alarm_list_query

### 用途

告警清单列表查询

### 输入

```sql
CREATE DEFINER=`root`@`%` PROCEDURE `pro_alarm_list_query`(

i_begin_day  date, -- 2019-06-04
i_end_day  date,
i_alarmlevel_query  varchar(10), -- 等于5：=5  大于3：>=3  等于全部：'' 没有大于全部小于全部
i_fulltext_query text, -- 关键字查询
i_actiontype  char(20),  -- '':全部  行为类型
/*
056:查平台1
http	网页发布
im	即时通讯
netdisk	网盘
email	电子邮件
filetransfer	文件传输
other	其他
csmp	接入互联网
docaudit	文档操作
website	门户网站
*/
i___alarmSour int,  -- 告警来源0:全部 1：告警模型  2：手动加入
i_cz_status  int , -- 1:待处置 2：已处置  3：违规  0:无此查询
i__interested int, -- 0: 全部  1：关注  2：未关注
i___alarmType int,-- 1,2,3,4 0:全部

i_orderby varchar(30), -- __alarmLevel/__connectTime/__alarmTime + asc /desc
i_page_capa  int , -- 每页的容量（400） 
i_page_num  int ,-- 跳页数（ 首页为0 ，第二页是1 ）

i___security  varchar(50),-- 密级
i___alarmKey  varchar(50) -- 关键字

)
```

### 输出
```buildoutcfg
结果集1：
alarm_list全字段+ total_rows（总数）
```

```buildoutcfg
结果集2：
__security（密级）
count_（分类统计数）
```

```buildoutcfg
结果集3：
__alarmKey（关键字）
count_（分类统计数）
```




## pro_cfg_keyword_add

### 用途

添加关键字

### 输入

```sql
CREATE DEFINER=`root`@`%` PROCEDURE `pro_cfg_keyword_add`(
# 添加关键字
	i_keyword		varchar(200),
	i_keylevel	int,
	i_enabled		int, #启用0 禁用1
	i_remark		varchar(200),
	i_add_user	varchar(100),
	i_keytype int  # 1:关键词  2：正则表达式
)
```

### 输出
```buildoutcfg
select True as err , #成功
'添加成功' as msg ; #成功信息
```




## pro_cfg_keyword_delete

### 用途

删除关键字

### 输入

```sql
CREATE DEFINER=`root`@`%` PROCEDURE `pro_cfg_keyword_delete`(
# 添加关键字
	i_auid      int
)
```

### 输出
```buildoutcfg
select True as err , '删除成功' as msg ;
```



## pro_cfg_keyword_edit

### 用途

编辑关键字

### 输入

```sql
CREATE DEFINER=`root`@`%` PROCEDURE `pro_cfg_keyword_edit`(
# 编辑关键字
	i_auid      int,
	i_keyword		varchar(200),
	i_keylevel	int,
	i_enabled		int,
	i_remark		varchar(200),
	i_add_user	varchar(100),
	i_keytype int   # 1:关键词  2：正则表达式
)
```

### 输出
```buildoutcfg
select True as err , '更新成功' as msg ;
```






## pro_cfg_keyword_edit_valid

### 用途

更新关键字的有效性（后台调用）

### 输入

```sql
CREATE DEFINER=`root`@`%` PROCEDURE `pro_cfg_keyword_edit_valid`(
# 更新关键字的有效性
	i_auid		int, #关键字的auid
	i_valid	int  # 0.无效  1有效
)
```

### 输出
```buildoutcfg
select True as err , '更新成功' as msg ;
```


## pro_cfg_keyword_query

### 用途

查询关键字列表

### 输入

```sql
CREATE  PROCEDURE `pro_cfg_keyword_query`(
# 查询关键字
	i_begin_day  date,
	i_end_day		 date,
	i_keylevel     int ,  -- 0:全部  1-5：其他等级
	i_enabled			int, -- -1 0 1
	i_keyword    varchar(100),-- '':空串不加入该条件   
	i_last_keylevel int, -- 只有在告警等级排序的时候，才传这个值，否则传0
	i_last_auid  int, -- 0:首次  >0：上一页最大id
	i_page_count  int , -- 每页数量  0:不分页 全部导出
	i_order_by  varchar(10), --  asc/desc  
	i_keytype   int -- 0 : 无此条件  1：关键字  2正则表达式
)
```

### 输出
```buildoutcfg
cfg_keyword的全字段+total（总数）
```






## pro_cfg_keyword_query_all

### 用途

查询关键字列表(后台使用，全查)

### 输入

NULL

### 输出
```buildoutcfg
select auid, 
keyword, #
keylevel,#
keytype #
```




## pro_cz_list_query

### 用途

查询处置记录

### 输入

CREATE DEFINER=`root`@`%` PROCEDURE `pro_cz_list_query`(
i___md5   varchar(50)  # 告警文档的md5
)

### 输出
```buildoutcfg
cz_list 表的所有字段
```


## pro_dict_query

### 用途

查询字典元数据

### 输入

NULL

### 输出
```buildoutcfg
`type`, #项组
`key`,#key
`value`,#value
remark #备注或中文
```

## pro_event_list_add

### 用途

添加事件列表

### 输入
```
CREATE DEFINER=`root`@`%` PROCEDURE `pro_event_list_add`(
i___md5  varchar(50), -- 告警的md5，这个字段是用来关联行为的
i_event_id  varchar(20), #事件编号
i_event_name varchar(200), #事件名称
i_event_type int , # 
/*
1	违规外联
2	互联网传输泄密
3	网络攻击窃密
4	违规存储/处理涉密信息
*/
i_event_miji char(10), #JIMI:机密 MIMI:秘密  JUEMI：绝密  NEIBU:内部
i_event_status int, # 1.待处理 2.不移交  3移交未反馈  4移交已反馈 
i_content  text, #内容 显示 文件名 或者 违规外联描述
i_remark   text, #备注
i_add_user varchar(50),
i_report  text  #这是ui自行组织的json，用于打印报告
)
```
### 输出
```buildoutcfg
	select true as err , '添加事件成功' as msg ;
```


## pro_event_list_create_event_id

### 用途

创建事件ID

### 输入
null
### 输出
```buildoutcfg
event_id #根据时间创建的串
```



## pro_event_list_drop

### 用途

删除事件

### 输入
```buildoutcfg
CREATE DEFINER=`root`@`%` PROCEDURE `pro_event_list_drop`(
i_event_id  varchar(20) #事件编号
)
```
### 输出
```buildoutcfg
select True as err,'删除成功' as msg;
```


## pro_event_list_edit

### 用途

编辑事件

### 输入
```buildoutcfg
CREATE DEFINER=`root`@`%` PROCEDURE `pro_event_list_edit`(
i_event_id  varchar(20), #事件编号
i_event_name varchar(200), #事件名称
i_event_type int , # 
/*
1	违规外联
2	互联网传输泄密
3	网络攻击窃密
4	违规存储/处理涉密信息
*/
i_event_miji char(10), #JIMI:机密 MIMI:秘密  JUEMI：绝密  NEIBU:内部
i_event_status int, # 1.待处理 2.不移交  3移交未反馈  4移交已反馈 
i_remark   text, #备注
i_add_user varchar(50)
)
```
### 输出
```buildoutcfg
select True as err,'更新成功' as msg;
```




## pro_event_list_query

### 用途

查询事件列表

### 输入
```buildoutcfg
i_begin_day  date, -- 2019-06-04
i_end_day  date,
i_event_status  int, #0全查 1.待处理 2.不移交  3移交未反馈  4移交已反馈
i_event_miji  varchar(20),
i_event_type  int,
i_fulltext_query text, -- 关键字查询(事件名 违规内容 备注)
i_page_capa  int , -- 每页的容量（400） 
i_page_num  int -- 跳页数（ 首页为0 ，第二页是1 ）
```
### 输出
```buildoutcfg
event_list 全字段 + total_rows（总行数）
```





## pro_tj_action_list_actiontype

### 用途

统计待处置告警数的行为类型分布

### 输入
```buildoutcfg
i_begin_day  date, -- 开始日期（针对告警时间__alarmTime）
i_end_day  date  -- 结束日期
```
### 输出
```buildoutcfg
actiontype, #见dict
__count #每个actiontype对应的数量
```



## pro_tj_action_list_alarmtype

### 用途

统计待处置告警数的告警类型分布

### 输入
```buildoutcfg
i_begin_day  date, -- 开始日期（针对告警时间__alarmTime）
i_end_day  date  -- 结束日期
```
### 输出
```buildoutcfg
alarm_type, #见dict
__count #每个alarm_type对应的数量
```

## pro_tj_alarm_list_cz

### 用途

统计处置告警的状态分布

### 输入
```buildoutcfg
i_begin_day  date, -- 开始日期（针对告警时间__alarmTime）
i_end_day  date  -- 结束日期
```
### 输出
```buildoutcfg
cz_status, #见dict
__count #每个cz_status对应的数量
```


## pro_tj_alarm_list_level

### 用途

统计未处置告警的告警等级分布

### 输入
```buildoutcfg
i_begin_day  date, -- 开始日期（针对告警时间__alarmTime）
i_end_day  date  -- 结束日期
```
### 输出
```buildoutcfg
alarm_level, #见dict
__count #每个alarm_level对应的数量
```


## pro_tj_alarm_list_weigui

### 用途

 统计违规告警数 以及 是否有红点

### 输入
```buildoutcfg
i_begin_day  date, -- 开始日期（针对告警时间__alarmTime）
i_end_day  date  -- 结束日期
```
### 输出
```buildoutcfg
__count #违规告警数
redPoint：0:无红点  1：有红点

```


## tj_frontpage_alarm_list

### 用途

首页统计————告警 违规 处置

### 输入
```buildoutcfg
i_begin_day  date,
i_end_day date,
cz_or_wg  varchar(10)  # cz: 查询处置量   wg:查询违规量
```
### 输出
```buildoutcfg
__count # 数量
```

## tj_frontpage_alarm_list_day

### 用途

首页统计————告警 违规 处置 的 日峰值

### 输入
```buildoutcfg
cz_or_wg  varchar(10)  # cz: 查询处置量   wg:查询违规量  '' 所有
```
### 输出
```buildoutcfg
__count # 数量
```



## tj_frontpage_alarm_platform

### 用途

首页统计————告警 违规 处置 (按平台)

### 输入
```buildoutcfg
	i_begin_day  date,
	i_end_day date
```
### 输出
```buildoutcfg
@count_p1_all count_p1_all, #平台1总量，平台234以此推
@count_p1_cz count_p1_cz, #平台1处置量，平台234以此推
@count_p1_wg count_p1_wg,#平台1违规量，平台234以此推
@count_p2_all count_p2_all,@count_p2_cz count_p2_cz,@count_p2_wg count_p2_wg,
@count_p3_all count_p3_all,@count_p3_cz count_p3_cz,@count_p3_wg count_p3_wg,
@count_p4_all count_p4_all,@count_p4_cz count_p4_cz,@count_p4_wg count_p4_wg;
```



## fun_action_list_getLastTime

### 用途

函数：查询上次connectionTime时间，用于查红点数据时，起始时间限制


### 输入
```buildoutcfg
i___md5   varchar(50)
```
### 输出
```buildoutcfg
datetime：上次最大时间
```


## fun_alarm_list_exists

### 用途

函数：查询某md5在alarm_list中是否存在


### 输入
```buildoutcfg
i___md5   varchar(50)
```
### 输出
```buildoutcfg
tinyint：0:不存在 1：存在 2：存在且被判定为违规
```



## fun_translate_code

### 用途

函数：将特殊符号转译为其他字符存储在mysql中
具体映射关系见dict的translate_code

### 输入
```buildoutcfg
i_keyword   varchar(200)  # 将keyword中的特殊字符串转译
```
### 输出
```buildoutcfg
varchar(200)：经过转译以后的串
```


## tj_frontpage_alarm_sour

### 用途

统计首页右下角，人工加入的告警和自动加入的告警数据量

### 输入
```buildoutcfg
i_begin_day  date,
i_end_day date
```
### 输出
```buildoutcfg
row_name：__security、__alarmKey、__document、__industry
__alarmSour：见model
count_：统计量
```


## pro_platform_edit

### 用途

编辑平台的简称、别名

### 输入
```buildoutcfg
	i_platformid   int, #平台id，见dict
	i_name  varchar(45), #名称
	i_nicname  varchar(45), #别名
	i_simname  varchar(45) #简称

```
### 输出
```buildoutcfg
select 0 as err, concat('修改平台',i_platformid,'成功')as msg;
```


## pro_platform_query

### 用途

查询平台的简称、别名

### 输入
null
### 输出
```buildoutcfg
platformid   int, #平台id，见dict
name  varchar(45), #名称
nicname  varchar(45), #别名
simname  varchar(45) #简称
```