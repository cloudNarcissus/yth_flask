/*
Navicat MySQL Data Transfer

Source Server         : 192.168.10.136
Source Server Version : 50544
Source Host           : 192.168.10.136:3306
Source Database       : yth_alarm

Target Server Type    : MYSQL
Target Server Version : 50544
File Encoding         : 65001

Date: 2019-07-24 16:34:54
*/
CREATE DATABASE IF NOT EXISTS yth_alarm  DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci;
use yth_alarm;
SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for action_list
-- ----------------------------
DROP TABLE IF EXISTS `action_list`;
CREATE TABLE `action_list` (
  `yth_base_id` varchar(25) NOT NULL DEFAULT '',
  `__md5` varchar(50) NOT NULL DEFAULT '',
  `platform` int(11) DEFAULT NULL,
  `actiontype` char(20) DEFAULT NULL,
  `redPoint` int(11) DEFAULT NULL,
  `unit` varchar(50) DEFAULT NULL,
  `__connectTime` datetime DEFAULT NULL,
  `website_name` varchar(100) DEFAULT NULL,
  `account` varchar(50) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL,
  `ip` varchar(200) DEFAULT NULL,
  `smac` varchar(50) DEFAULT NULL,
  `sport` varchar(50) DEFAULT NULL,
  `unitaddr` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  __bornTime datetime  default null,
  PRIMARY KEY (`__md5`,`yth_base_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for alarm_list
-- ----------------------------
DROP TABLE IF EXISTS `alarm_list`;
CREATE TABLE `alarm_list` (
  `auid` bigint(20) NOT NULL AUTO_INCREMENT,
  `yth_fileana_id` varchar(25) DEFAULT NULL,
  `__md5` varchar(50) DEFAULT NULL,
  `__connectTime` datetime DEFAULT NULL,
  `__alarmTime` datetime DEFAULT NULL,
  `__title` varchar(100) DEFAULT NULL,
  `__alarmLevel` int(11) DEFAULT NULL,
  `__alarmSour` int(11) DEFAULT NULL,
  `platform` int(11) DEFAULT NULL,
  `summary` text,
  `__alarmKey` text,
  `__document` text,
  `__industry` text,
  `__security` text,
  `cz_status` char(10) DEFAULT NULL,
  `cz_summary` text,
  `_interested` int(11) DEFAULT NULL,
  `__ips` varchar(100) DEFAULT NULL,
  `_action_count` int(11) DEFAULT '0',
  `__alarmType` int(11) DEFAULT NULL,
  `redPoint` int(11) DEFAULT NULL,
    `province` char(6) DEFAULT NULL,
  `city` char(6) DEFAULT NULL,
  `district` char(6) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `_platforms` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`auid`),
  UNIQUE KEY `ix_md5` (`__md5`),
  KEY `ix___alarmLevel` (`__alarmLevel`),
  KEY `ix___connectTime` (`__connectTime`),
  KEY `ix___alarmTime` (`__alarmTime`),
  KEY `ix_cz_status` (`cz_status`),
  KEY `ix_platform` (`platform`)
) ENGINE=InnoDB AUTO_INCREMENT=440 DEFAULT CHARSET=utf8mb4;

ALTER TABLE alarm_list ADD FULLTEXT INDEX summary(`summary`,`__md5`,`__ips`,`__title`) WITH PARSER `ngram` ;

-- ----------------------------
-- Table structure for ana_res
-- ----------------------------
DROP TABLE IF EXISTS `ana_res`;
CREATE TABLE `ana_res` (
  `taskid` varchar(36) NOT NULL DEFAULT '',
  `md5` varchar(32) NOT NULL DEFAULT '',
  `rootmd5` text,
  `parentmd5` text,
  `fileinfo` text,
  `deepinfo` text,
  `error` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for cfg_keyword
-- ----------------------------
DROP TABLE IF EXISTS `cfg_keyword`;
CREATE TABLE `cfg_keyword` (
  `auid` int(11) NOT NULL AUTO_INCREMENT,
  `keyword` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `keylevel` int(11) DEFAULT NULL,
  `enabled` int(11) DEFAULT NULL,
  `remark` varchar(200) DEFAULT NULL,
  `add_user` varchar(100) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  `keytype` int(11) DEFAULT NULL,
  `valid` int(11) DEFAULT '1',
  PRIMARY KEY (`auid`),
  UNIQUE KEY `uq_cfg_keyword` (`keyword`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for cz_list
-- ----------------------------
DROP TABLE IF EXISTS `cz_list`;
CREATE TABLE `cz_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `__md5` varchar(50) DEFAULT NULL,
  `cz_time` datetime DEFAULT NULL,
  `cz_user` varchar(50) DEFAULT NULL,
  `op_type` varchar(50) DEFAULT NULL,
  `cz_detail` text,
  `cz_status` char(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for dict
-- ----------------------------
DROP TABLE IF EXISTS `dict`;
CREATE TABLE `dict` (
  `key` varchar(50) NOT NULL COMMENT '键',
  `value` varchar(50) NOT NULL COMMENT '值',
  `desc` varchar(50) DEFAULT NULL COMMENT '描述',
  `name` varchar(45) DEFAULT NULL COMMENT '字典名称',
  `remark` varchar(45) DEFAULT NULL COMMENT '备注',
  `group` varchar(45) DEFAULT NULL COMMENT '分组',
  `parent_key` varchar(45) DEFAULT NULL COMMENT '父类型 key',
  `optional_1` varchar(45) DEFAULT NULL COMMENT '扩展字段1',
  `optional_2` varchar(45) DEFAULT NULL COMMENT '扩展字段2',
  `optional_3` varchar(45) DEFAULT NULL,
  `optional_4` varchar(45) DEFAULT NULL,
  `optional_5` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`key`,`value`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='字典';

-- ----------------------------
-- Table structure for event_action_list
-- ----------------------------
DROP TABLE IF EXISTS `event_action_list`;
CREATE TABLE `event_action_list` (
  `event_id` varchar(20) NOT NULL DEFAULT '',
  `yth_base_id` varchar(25) NOT NULL DEFAULT '',
  PRIMARY KEY (`event_id`,`yth_base_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for event_list
-- ----------------------------
DROP TABLE IF EXISTS `event_list`;
CREATE TABLE `event_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_id` varchar(20) DEFAULT NULL,
  `event_name` varchar(200) DEFAULT NULL,
  `event_type` int(11) DEFAULT NULL,
  `event_miji` char(10) DEFAULT NULL,
  `event_status` int(11) DEFAULT NULL,
  `content` text,
  `remark` text,
  `add_user` varchar(50) DEFAULT NULL,
  `add_time` datetime DEFAULT NULL,
  `report` text,
   province char(6)DEFAULT NULL,
   city char(6) DEFAULT NULL,
   district char(6) DEFAULT NULL,
   unit int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_event_id` (`event_id`),
  KEY `ix_add_time` (`add_time`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

ALTER TABLE event_list ADD FULLTEXT INDEX summary(`event_name`,`content`,`remark`) WITH PARSER `ngram` ;

-- ----------------------------
-- Table structure for file_ana_res
-- ----------------------------
DROP TABLE IF EXISTS `file_ana_res`;
CREATE TABLE `file_ana_res` (
  `md5` varchar(32) NOT NULL,
  `deepinfo` text CHARACTER SET utf8mb4 NOT NULL,
  `fileinfo` text CHARACTER SET utf8mb4 NOT NULL,
  PRIMARY KEY (`md5`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for task_tmp
-- ----------------------------
DROP TABLE IF EXISTS `task_tmp`;
CREATE TABLE `task_tmp` (
  `uuid` char(40) NOT NULL DEFAULT '',
  `md5` char(32) NOT NULL DEFAULT '',
  `root_md5` char(32) NOT NULL,
  `parent_md5` char(32) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for wdp_file_task
-- ----------------------------
DROP TABLE IF EXISTS `wdp_file_task`;
CREATE TABLE `wdp_file_task` (
  `auid` int(11) NOT NULL AUTO_INCREMENT,
  `source_type` int(11) DEFAULT '0' COMMENT '数据来源类型，暂 1-056传输SM，2-三合一，3-文档审计，4-门户网站',
  `file_md5` varchar(255) DEFAULT NULL COMMENT '文件md5',
  `filename` varchar(512) DEFAULT NULL COMMENT '文件名',
  `deal_flag` int(11) DEFAULT '0' COMMENT '处理标记',
  `location` varchar(128) DEFAULT 'hbase' COMMENT '文件保存介质，fs,mongo,hbase',
  `put_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '任务提交时间',
  `reserve1` int(11) DEFAULT NULL COMMENT '备用字段1',
  `reserve2` varchar(255) DEFAULT NULL COMMENT '备用字段2',
  PRIMARY KEY (`auid`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='多平台文件分析任务表';



-- ----------------------------
-- Procedure structure for pro_action_list_add
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_action_list_add`;
DELIMITER ;;
create PROCEDURE pro_action_list_add(
i_yth_base_id varchar(25), #es 中 yth_base的doc_id，可以此关联到es表
i___md5   varchar(50), 
i_platform int, 
i_actiontype char(20),
i_redPoint int, #是否有红点
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
i___bornTime datetime
)
pl:
BEGIN
	insert into action_list
(	
	yth_base_id,
	__md5  ,  # 文件md5  此键用于关联主表的__md5(本表中同一md5有若干条子条目)
	platform , #平台 1234
	actiontype , #行为类型 见字典
	redPoint , #是否有红点
	unit ,
	__connectTime,  #接入时间（ES那边的时间）

website_name,
account ,
url,
ip ,
smac,
sport,
unitaddr,
contact,
__bornTime
)
 values 
(
i_yth_base_id,
i___md5  , 
i_platform , 
i_actiontype ,
i_redPoint,
i_unit  ,
i___connectTime ,

i_website_name,
i_account ,
i_url ,
i_ip  ,
i_smac ,
i_sport ,
i_unitaddr ,
i_contact,
i___bornTime  
) ON DUPLICATE KEY UPDATE account=account
;

  -- 更新主表的action_count 和 redPoint  20190813又增加_platforms字段更新
	set @action_count :=0;
	set @redPoint :=0;
	set @platforms := NULL;
	select count(*),max(redPoint),group_concat(platform SEPARATOR '|') into @action_count,@redPoint,@platforms from action_list where __md5=i___md5;
	update alarm_list set _action_count=@action_count,redPoint=@redPoint,_platforms=@platforms where __md5=i___md5;

END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_action_list_query
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_action_list_query`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_action_list_query`(
# 查询轨迹追踪（子条目action）
i___md5  varchar(50)
)
pl:
BEGIN

	select * from action_list where __md5 = i___md5
	order by __connectTime desc ;

	-- 然后更新红点

	update action_list set redPoint = 0 
	where __md5=i___md5 and redPoint = 1;

END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_alarm_list_add
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_alarm_list_add`;
DELIMITER ;;
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
pl:
BEGIN

	set @platform := NULL;
	set @platforms := NULL;
	if i___alarmType =1 then 
		set i___md5 = uuid();
		set @platform := 2;
		set @platforms := '2|';
	end if;

	insert into alarm_list(
yth_fileana_id , #es 中 yth_fileana的doc_id，可以此关联到es表
__md5,  # 文件md5  用于检测唯一性的

__connectTime , #接入时间
__alarmTime  , #告警时间
__title   ,#标题
__alarmLevel  ,#告警等级 1-5
__alarmSour , #告警来源 1：告警模型  2：手动加入
summary , #显示的摘要

__alarmKey ,  #关键字 JSON格式 同es
__document ,  #公文 JSON格式 同es
__industry ,  #行业 JSON格式 同es
__security ,  #密级 JSON格式 同es

cz_status  , #NO:未处置  PASS：处置为正常  JIMI:处置为机密 MIMI:处置为秘密  JUEMI：处置为绝密
_interested,
__ips  ,
__alarmType,
platform,
_platforms
)
values (
i_yth_fileana_id , #es 中 yth_fileana的doc_id，可以此关联到es表
i___md5  ,  # 文件md5  用于检测唯一性的

i___connectTime , #接入时间
now()  , #告警时间
i___title   ,#标题
i___alarmLevel  ,#告警等级 1-5
i___alarmSour , #告警来源 1：告警模型  2：手动加入
i_summary , #显示的摘要

i___alarmKey ,  #关键字 JSON格式 同es
i___document ,  #公文 JSON格式 同es
i___industry ,  #行业 JSON格式 同es
i___security ,  #密级 JSON格式 同es
'NO' ,
FALSE,
i___ips,
i___alarmType,
@platform,
@platforms
);

END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_alarm_list_cz
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_alarm_list_cz`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_alarm_list_cz`(
# 处置告警
i_cz_user varchar(50),
i___md5   varchar(50),
i_cz_status  char(10), -- NO:未处置  PASS：处置为正常  JIMI:处置为机密 MIMI:处置为秘密  JUEMI：处置为绝密
i_cz_summary  text, -- 涉密摘要 （处置摘要）
i_cz_detail  text -- ui自行组织字段，用于在历史记录里面显示的
)
pl:
BEGIN
	update alarm_list 
	set cz_status= i_cz_status ,
	cz_summary = i_cz_summary
	where __md5 = i___md5;

	-- 插入处置历史记录
	insert into cz_list(__md5,cz_time,cz_user,op_type,cz_detail,cz_status)
	values (i___md5,now(),i_cz_user,'违规判断',i_cz_detail,i_cz_status);


END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_alarm_list_interested
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_alarm_list_interested`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_alarm_list_interested`(
# 关注告警
i___md5   varchar(50),
i__interested  bool  # true  flase 
)
pl:
BEGIN
	update alarm_list 
	set _interested = i__interested
	where __md5 = i___md5;


END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_alarm_list_left
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_alarm_list_left`;
DELIMITER ;;
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
i___security  varchar(50),
i___alarmKey  varchar(50)
)
pl:
BEGIN
	
	declare v_sql text;

	set i_end_day = DATE_ADD(i_end_day,INTERVAL 1 day);
	set @_where := CONCAT(
		'where __alarmTime between ''',i_begin_day,''' and ''',i_end_day,''' ',
		if(ifnull(i_alarmlevel_query,'')<>'', concat(' and __alarmLevel ', i_alarmlevel_query) ,''),
		if(ifnull(i_fulltext_query,'')<>'', concat(' and match(summary,__md5,__ips,__title) against (''"',i_fulltext_query,'*"'' IN BOOLEAN MODE)'),''),
		if(ifnull(i___alarmSour,0)>0,concat(' and __alarmSour =',i___alarmSour),''),
		case ifnull(i_actiontype,'') when '' then ''
																when 'csmp' then ' and a.platform=2 '
																when '056' then ' and exists(select * from action_list b where a.__md5=b.__md5 and b.platform=1)'
																else concat(' and exists(select * from action_list b where a.__md5=b.__md5 and b.actiontype =''',i_actiontype,''')')
		end,
		case ifnull(i__interested,0) when 1 then ' and a._interested = TRUE'
																when 2 then ' and a._interested = FALSE'
		else '' END,
		if(ifnull(i___alarmType,0)>0,concat(' and a.__alarmType =',i___alarmType),''),
		if(ifnull(i___security,'')<>'',concat(' and a.__security =''',i___security,''''),''),
		if(ifnull(i___alarmKey,'')<>'',concat(' and a.__alarmKey =''',i___alarmKey,''''),'')
		
	);
	

	-- 待处置数目
	set @NO_count:=0;
	set @v_sql := CONCAT(
		'select count(*) into @NO_count from alarm_list a
		',
		@_where ,
		'
		and cz_status = ''NO''
		'
	);
	-- select @v_sql; leave pl;
	PREPARE S1 from @v_sql;		
	EXECUTE S1 ;
	DEALLOCATE PREPARE S1;

	-- 已处置数目
	set @YES_count:=0;
	set @v_sql := CONCAT(
		'select count(*) into @YES_count from alarm_list a
',
		@_where ,
		'
		and cz_status <> ''NO''
		'
	);
	PREPARE S2 from @v_sql;		
	EXECUTE S2 ;
	DEALLOCATE PREPARE S2;

	
	-- 违规数目
	set @DANGER_count:=0;
	set @v_sql := CONCAT(
		'select count(*) into @DANGER_count from alarm_list a
',
		@_where ,
		'
		and cz_status not in ( ''NO'',''PASS'')
		'
	);
	PREPARE S3 from @v_sql;		
	EXECUTE S3 ;
	DEALLOCATE PREPARE S3;

	-- 关注条目
	set @INTRESTED_count:=0;
	set @v_sql := CONCAT(
		'select count(*) into @INTRESTED_count from alarm_list a
',
		@_where ,
		'
		and _interested = TRUE
		'
	);
	PREPARE S4 from @v_sql;		
	EXECUTE S4 ;
	DEALLOCATE PREPARE S4;

	select @NO_count as NO_count ,@YES_count as YES_count,@DANGER_count as DANGER_count,@INTRESTED_count as NTRESTED_count;


END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_alarm_list_query
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_alarm_list_query`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_alarm_list_query`(

i_begin_day  date, -- 2019-06-04
i_end_day  date,
i_alarmlevel_query  varchar(10), -- 等于5：=5  大于3：>=3  等于全部：'' 没有大于全部小于全部
i_fulltext_query text, -- 关键字查询
i_actiontype  char(20),  -- '':全部  行为类型
/*A
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
pl:
BEGIN
	
	declare v_sql text;
	declare v_where text;

	set @select_str :=(select GROUP_CONCAT(s.column_name) from information_schema.`COLUMNS` s where s.table_name='alarm_list' /*and s.column_name not in ('__ips')*/);

	drop TEMPORARY table if exists query_result;
	CREATE TEMPORARY TABLE `query_result` (
  `auid` bigint(20),
  `yth_fileana_id` varchar(25) DEFAULT NULL,
  `__md5` varchar(50) DEFAULT NULL,
  `__connectTime` datetime DEFAULT NULL,
  `__alarmTime` datetime DEFAULT NULL,
  `__title` varchar(100) DEFAULT NULL,
  `__alarmLevel` int(11) DEFAULT NULL,
  `__alarmSour` int(11) DEFAULT NULL,
  `platform` int(11) DEFAULT NULL,
  `summary` varchar(2000),
  `__alarmKey` varchar(200),
  `__document` varchar(2000),
  `__industry` varchar(2000),
  `__security` varchar(200),
  `cz_status` char(10) DEFAULT NULL,
  `cz_summary` varchar(2000),
  `_interested` int(11) DEFAULT NULL,
  `__ips` varchar(100) DEFAULT NULL,
  `_action_count` int(11) DEFAULT '0',
  `__alarmType` int(11) DEFAULT NULL,
  `redPoint` int(11) DEFAULT NULL,
    `province` char(6) DEFAULT NULL,
  `city` char(6) DEFAULT NULL,
  `district` char(6) DEFAULT NULL,
  `unit` int(11) DEFAULT NULL,
  `_platforms` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`auid`),
  KEY `ix___security` (`__security`),
  KEY `ix___alarmKey` (`__alarmKey`)
	)ENGINE=Memory;


		set v_where = concat(
		if(ifnull(i_alarmlevel_query,'')<>'', concat(' and a.__alarmLevel ', i_alarmlevel_query) ,''),
		if(ifnull(i_fulltext_query,'')<>'', concat(' and match(summary,__md5,__ips,__title) against (''"',i_fulltext_query,'*"'' IN BOOLEAN MODE)'),''),
		case ifnull(i_actiontype,'') when '' then ''
																when 'csmp' then ' and a.platform=2 '
																when '056' then ' and exists(select * from action_list b where a.__md5=b.__md5 and b.platform=1)'
																else concat(' and exists(select * from action_list b where a.__md5=b.__md5 and b.actiontype =''',i_actiontype,''')')
		end,
		if(ifnull(i___alarmSour,0)>0,concat(' and a.__alarmSour =',i___alarmSour),''),
		case i_cz_status when 1 then ' and a.cz_status =''NO'' '
										 WHEN 2 THEN ' and a.cz_status <> ''NO'' '
										 WHEN 3 THEN ' and a.cz_status not in (''NO'',''PASS'') '
		else '' end ,
		case ifnull(i__interested,0) when 1 then ' and a._interested = TRUE'
																when 2 then ' and a._interested = FALSE'
		else '' END,
		if(ifnull(i___alarmType,0)>0,concat(' and a.__alarmType =',i___alarmType),''),

		if(ifnull(i___security,'')<>'',concat(' and a.__security =''',i___security,''''),''),
		if(ifnull(i___alarmKey,'')<>'',concat(' and a.__alarmKey =''',i___alarmKey,''''),'')

		);	
	
		SET v_sql = concat(
		'select count(*) into @total_rows from alarm_list a where a.__alarmTime between ? and ? ',
		v_where
		);
		set @v_sql := v_sql;
		set @i_begin_day := i_begin_day;
		set @i_end_day := DATE_ADD(i_end_day,INTERVAL 1 day);
		
		PREPARE S1 from @v_sql;		
		EXECUTE S1 USING @i_begin_day,@i_end_day;
		DEALLOCATE PREPARE S1;

	
	SET v_sql = concat(
	'
	insert into query_result
	select ',@select_str,' from alarm_list a where a.__alarmTime between ? and ? ',
	v_where,
  ' order by ',i_orderby, ' limit ', i_page_num*i_page_capa,',',i_page_capa
	);
	
	set @v_sql := v_sql;
	
	PREPARE S1 from @v_sql;		
	EXECUTE S1 USING @i_begin_day,@i_end_day;
	DEALLOCATE PREPARE S1;


	select *,@total_rows as total_rows  from query_result ;

	select __security,count(*)as count_ from query_result where __security<>''  group by __security;-- 
	select __alarmKey,count(*)as count_ from query_result where __alarmKey<>'' group by __alarmKey;


END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_cfg_keyword_add
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_cfg_keyword_add`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_cfg_keyword_add`(
# 添加关键字
	i_keyword		varchar(200),
	i_keylevel	int,
	i_enabled		int,
	i_remark		varchar(200),
	i_add_user	varchar(100),
	i_keytype int  # 1:关键词  2：正则表达式
)
pl:
BEGIN
	
	set i_keyword = fun_translate_code(i_keyword);

	if exists(select * from cfg_keyword where keyword=i_keyword)
	then 
		select false as err , '重复添加' as msg ;
		leave pl;
	end if;

	insert into cfg_keyword(
	keyword,
	keylevel,
	enabled,
	remark,
	add_user,
	add_time,
	keytype
	)
	values(
	i_keyword,
	i_keylevel,
	i_enabled,
	i_remark,
	i_add_user,
	now(),
	i_keytype);

	select True as err , '添加成功' as msg ;

END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_cfg_keyword_delete
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_cfg_keyword_delete`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_cfg_keyword_delete`(
# 添加关键字
	i_auid      int
)
pl:
BEGIN

	delete from cfg_keyword where auid = i_auid;

	select True as err , '删除成功' as msg ;

end
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_cfg_keyword_edit
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_cfg_keyword_edit`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_cfg_keyword_edit`(
# 添加关键字
	i_auid      int,
	i_keyword		varchar(200),
	i_keylevel	int,
	i_enabled		int,
	i_remark		varchar(200),
	i_add_user	varchar(100),
	i_keytype int   # 1:关键词  2：正则表达式
)
pl:
BEGIN

	set i_keyword = fun_translate_code(i_keyword);

	if exists(select * from cfg_keyword where keyword=i_keyword and auid<>i_auid)
	then 
		select false as err , '该key已存在' as msg ;
		leave pl;
	end if;
 

	update cfg_keyword set 
		keyword = i_keyword,
		keylevel = i_keylevel,
		enabled =i_enabled,
		remark=i_remark,
		add_user=i_add_user,
		add_time = now(),
		keytype = i_keytype
	where auid= i_auid;

	select True as err , '更新成功' as msg ;
end
;;
DELIMITER ;



-- ----------------------------
-- Procedure structure for pro_cfg_keyword_edit_valid
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_cfg_keyword_edit_valid`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_cfg_keyword_edit_valid`(
# 更新关键字的有效性
	i_auid		int, #关键字的auid
	i_valid	int
)
pl:
BEGIN

	update cfg_keyword set 
		valid = i_valid
	where auid= i_auid;

	select True as err , '更新成功' as msg ;
end
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_cfg_keyword_query
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_cfg_keyword_query`;
DELIMITER ;;
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
pl:
BEGIN

	set @i_order_fuhao = '<';
	set @i_order_fuhao = if (i_order_by='asc','>=','<='); 
	
	set @where_ =CONCAT( '
	from cfg_keyword a
	where add_time between ? and ?
	',
	if(i_last_auid>0,concat(' and a.auid',@i_order_fuhao,i_last_auid),''),
	if(i_last_keylevel>0,concat(' and a.keylevel',@i_order_fuhao,i_last_keylevel),''),
	if(i_keylevel>0,concat(' and a.keylevel=',i_keylevel),''),
	case ifnull(i_enabled,-1) when 1 then  ' and a.enabled=1 '
														when 0 then  ' and a.enabled=0 '
	else '' end ,
	if(i_keyword<>'',concat(' and a.keyword like ''%',i_keyword,'%'''),''),
	if(i_keytype>0,concat(' and a.keytype =',i_keytype),'')
	);
	
	-- 先查总数
	set @total := 0;
	set @sql_ = concat('select count(*) into @total',@where_);
	set @i_begin_day = i_begin_day;
	set @i_end_day = DATE_ADD(i_end_day,INTERVAL 1 day);

		
	PREPARE stmt FROM @sql_;  
	EXECUTE stmt using @i_begin_day,@i_end_day;
	DEALLOCATE PREPARE stmt;
	
	-- 再查分页

	set @sql_ = concat('select a.*, @total as total',@where_,
	'
	 order by ',if(i_last_keylevel>0,concat(' a.keylevel ',i_order_by,','),''),' a.auid ',i_order_by);

	if i_page_count > 0 then 
		SET @sql_ = concat(@sql_,'
		limit ',i_page_count+1);
	END IF;
	-- select @sql_;
	-- leave pl;

	PREPARE stmt FROM @sql_;  


	EXECUTE stmt using @i_begin_day,@i_end_day;
	DEALLOCATE PREPARE stmt;


end
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_cfg_keyword_query_all
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_cfg_keyword_query_all`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_cfg_keyword_query_all`(

)
pl:
BEGIN

	set names utf8;

	select auid, keyword, keylevel,keytype from cfg_keyword where enabled =1 ;

end
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_cz_list_query
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_cz_list_query`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_cz_list_query`(
# 统计待处置告警数的行为类型分组
i___md5   varchar(50)  # 告警文档的md5
)
pl:
BEGIN

	select * from cz_list where __md5 = i___md5 order by id desc;
	


END
;;
DELIMITER ;
-- ----------------------------
-- Procedure structure for pro_dict_query
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_dict_query`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_dict_query`(
# 查询字典表
)
pl:
BEGIN


	select *,'' as addition_col from (
	select *  from (

	-- 告警级别
	select 'alarm_level' as `type`,`value` as `key`,`desc` as `value`,remark   from dict where `key`='alarm_level'
	union ALL
	-- 深度分析状态
	select 'deepana_status' as `type`,`value` as `key`,`desc` as `value`,remark  from dict where `key`='deepana_status'
	union ALL
	-- 违规行为类型
	select 'wgxw_type' as `type`,`value` as `key`,`desc` as `value`,remark  from dict where `key`='wgxw_type'
	union ALL
	-- sour_obj
	select 'sour_obj' as `type`,`name` as `key`,`desc` as `value`,remark  from dict where `key`='sour_obj'
	
	-- 三合一日志类型
	union ALL
	select 'logex_log_type'as `type`,`value` as `key`,`desc` as `value`,remark from dict where `KEY`='logex_log_type'
	-- 行为类型 actiontype
	union ALL
	select 'actiontype'as `type`,`desc` as `key`,`name` as `value`,`name` as remark from dict where `KEY`='actiontype'
	-- 事件类型 eventtype
	union ALL
	select 'event_type' as `type`,`value` as `key`,`desc` as `value`,remark from dict where `key`='event_type'
	-- 处置状态
	union all 
	select 'cz_status' as `type`,`desc` as `key`,`name` as `value`,remark from dict where `key`='cz_status'
	-- 事件密级
	union all 
	select 'event_miji' as `type`,`desc` as `key`,`name` as `value`,remark from dict where `key`='event_miji'
	-- 事件状态
	union all 
	select 'event_status' as  `type`,`value` as `key`,`name` as `value`,remark from dict where `key`='event_status'
	-- 告警类型
	union all 
	select 'alarm_type' as  `type`,`value` as `key`,`desc` as `value`,remark from dict where `key`='alarm_type'
	-- 告警类型
	union all 
	select 'alarm_type' as  `type`,`value` as `key`,`desc` as `value`,remark from dict where `key`='alarm_type'
	-- 文档审计操作类型
	union all 
	select 'operation_type' as `type`,`value` as `key`,`desc` as `value`,remark from dict where `key`='operation_type'
	-- 转译字符
	union all 
	select 'translate_code' as `type`,`value` as `key`,`name` as `value`,remark from dict where `key`='translate_code'
	-- 客户端在线状态
	union all 
	select 'client_status' as `type`,`value` as `key`,`desc` as `value`,remark from dict where `key`='client_status'

	) a order by a.type,a.`key`
	)a
	union all 
	-- 平台
	select 'platform' as `type`,`value` as `key`,`desc` as `value`,`name` as remark,remark as addition_col  from dict where `key`='platform'


	;


END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_event_list_add
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_event_list_add`;
DELIMITER ;;
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
pl:
BEGIN

	if exists(select * from event_list where event_id = i_event_id )then 
		select false as err , '事件编号已存在' as msg ;
		leave pl;
	end if;

	insert into event_list(
	event_id  ,
	event_name ,
	event_type ,
	event_miji ,
	event_status ,
	content ,
	remark   ,
	add_user ,
	add_time ,
	report )
	values(
	i_event_id  ,
	i_event_name ,
	i_event_type ,
	i_event_miji ,
	i_event_status ,
	i_content ,
	i_remark   ,
	i_add_user ,
	now() ,
	i_report);

	-- 插入关联行为
	insert into event_action_list(event_id,yth_base_id)
	select i_event_id,yth_base_id from action_list where __md5 = i___md5;

	select true as err , '添加事件成功' as msg ;
END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_event_list_create_event_id
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_event_list_create_event_id`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_event_list_create_event_id`(

)
pl:
BEGIN

	select concat('BMJ', DATE_FORMAT(now(),'%Y%m%d%H%i%s'))  as event_id; 


END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_event_list_drop
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_event_list_drop`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_event_list_drop`(
i_event_id  varchar(20) #事件编号
)
pl:
BEGIN

	delete from event_list where event_id = i_event_id;

	select True as err,'删除成功' as msg;
END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_event_list_edit
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_event_list_edit`;
DELIMITER ;;
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
pl:
BEGIN

	UPDATE event_list 
	SET 
  
  `event_name` = i_event_name,
  `event_type` = i_event_type,
  `event_miji` = i_event_miji,
  `event_status` = i_event_status,
  `remark` = i_remark,
  `add_user` = i_add_user,
  `add_time` = NOW()
  WHERE event_id = i_event_id;

	select True as err,'更新成功' as msg;


END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_event_list_query
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_event_list_query`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_event_list_query`(
# 查询事件列表
i_begin_day  date, -- 2019-06-04
i_end_day  date,
i_event_status  int, #0全查 1.待处理 2.不移交  3移交未反馈  4移交已反馈
i_event_miji  varchar(20),
i_event_type  int,
i_fulltext_query text, -- 关键字查询(事件名 违规内容 备注)
i_page_capa  int , -- 每页的容量（400） 
i_page_num  int -- 跳页数（ 首页为0 ，第二页是1 ）
)
pl:
BEGIN
	
	declare v_sql text;	

	declare v_where text;
	
	set v_where = CONCAT(
		case when i_event_miji = 'JUEMI' then ' and a.event_miji =''JUEMI'' and a.event_type<>1   '
			when ifnull(i_event_miji,'')<>'' then concat(' and a.event_miji =''', i_event_miji,'''')
			else ''
		end ,
		if(ifnull(i_fulltext_query,'')<>'', concat(' and match(event_name,content,remark) against (''"',i_fulltext_query,'*"'' IN BOOLEAN MODE)'),''),    
		if(ifnull(i_event_type,0)>0,concat(' and a.event_type =',i_event_type),''),
		if(ifnull(i_event_status,0)>0,concat(' and a.event_status =',i_event_status),'')
	);


	#IF i_page_num=0 then 
		SET v_sql = concat(
		'select count(*) into @total_rows from event_list a where a.add_time between ? and ? ',
		v_where
		);
		
		set @v_sql := v_sql;
		set @i_begin_day := i_begin_day;
		set @i_end_day := DATE_ADD(i_end_day,INTERVAL 1 day);
		-- select @v_sql;
		PREPARE S1 from @v_sql;		
		EXECUTE S1 USING @i_begin_day,@i_end_day;
		DEALLOCATE PREPARE S1;

	#end if;


	SET v_sql = concat(
	'select *,@total_rows as total_rows from event_list a where a.add_time between ? and ? ',
	v_where,
  ' order by a.add_time desc limit ', i_page_num*i_page_capa,',',i_page_capa
	);
	
	set @v_sql := v_sql;
	set @i_begin_day := i_begin_day;
	set @i_end_day := DATE_ADD(i_end_day,INTERVAL 1 day);
	-- select @v_sql;
	PREPARE S1 from @v_sql;		
	EXECUTE S1 USING @i_begin_day,@i_end_day;
	DEALLOCATE PREPARE S1;

END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_tj_action_list_actiontype
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_tj_action_list_actiontype`;
DELIMITER ;;
CREATE  PROCEDURE `pro_tj_action_list_actiontype`(
# 统计待处置告警数的行为类型分组
i_begin_day  date, -- 开始日期（针对告警时间__alarmTime）
i_end_day  date  -- 结束日期
)
pl:
BEGIN

	set i_end_day =DATE_ADD(i_end_day,INTERVAL 1 day);

	select a.actiontype,b.__count from (
	select `desc` as actiontype from dict a where `key`= 'actiontype')a
	left join (

	select q.actiontype,count(DISTINCT q.__md5) as __count
	from
	(
	select b.__md5,b.actiontype from alarm_list a, action_list b
	where  a.cz_status = 'NO' and a.__md5=b.__md5
	and ifnull(a.platform,0) <>2  
	and a.__alarmTime between i_begin_day and i_end_day
	UNION ALL 
	select a.__md5,'csmp' as actiontype from alarm_list a
	where a.cz_status = 'NO' and a.platform =2
	and a.__alarmTime between i_begin_day and i_end_day

	) q
	
	group by q.actiontype)b
	on a.actiontype = b.actiontype;

END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_tj_action_list_alarmtype
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_tj_action_list_alarmtype`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_tj_action_list_alarmtype`(
# 统计待处置告警数的行为类型分组
i_begin_day  date, -- 开始日期（针对告警时间__alarmTime）
i_end_day  date  -- 结束日期
)
pl:
begin

	set i_end_day =DATE_ADD(i_end_day,INTERVAL 1 day);

	select a.alarm_type,b.__count
	from (
	select `value` as alarm_type from dict a where `key`= 'alarm_type')a
	left join
	(
		select __alarmType,count(*) as __count
		from alarm_list
		where cz_status = 'NO' and __alarmTime between i_begin_day and i_end_day 
		group by __alarmType
	)b on a.alarm_type=b.__alarmType;


END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_tj_alarm_list_cz
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_tj_alarm_list_cz`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_tj_alarm_list_cz`(
# 统计处置告警数
i_begin_day  date, -- 开始日期（针对告警时间__alarmTime）
i_end_day  date  -- 结束日期
)
pl:
BEGIN

	select a.cz_status,b.__count from (
	select `desc` as cz_status from dict a where `key`= 'cz_status')a
	left join (
	select cz_status,count(*) as __count
	from alarm_list
	where __alarmTime between i_begin_day and DATE_ADD(i_end_day,INTERVAL 1 day)
	group by cz_status) b on a.cz_status=b.cz_status;

END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_tj_alarm_list_level
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_tj_alarm_list_level`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_tj_alarm_list_level`(
# 统计待处置告警数的等级分组
i_begin_day  date, -- 开始日期（针对告警时间__alarmTime）
i_end_day  date  -- 结束日期
)
pl:
BEGIN
	set i_end_day =DATE_ADD(i_end_day,INTERVAL 1 day);


	select a.alarm_level,b.__count from (
	select `value` as alarm_level from dict a where `key`= 'alarm_level')a
	left join (

		select __alarmLevel,count(*) as __count
		from alarm_list
		where __alarmTime between i_begin_day and i_end_day 
		and cz_status = 'NO'
		group by __alarmLevel) b 
	on a.alarm_level = b.__alarmLevel;

END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for pro_tj_alarm_list_weigui
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_tj_alarm_list_weigui`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_tj_alarm_list_weigui`(
# 统计违规告警数 以及 是否有红点
i_begin_day  date, -- 开始日期（针对告警时间__alarmTime）
i_end_day  date  -- 结束日期
)
pl:
BEGIN

	set @count :=0;
	set @redPoint := FALSE;

	set i_end_day =DATE_ADD(i_end_day,INTERVAL 1 day);

	select count(*) into @count
	from alarm_list
	where __alarmTime between i_begin_day and i_end_day 
	and cz_status not in ('NO','PASS');

	if exists(
		select * from  action_list a,
    alarm_list b
		where b.__alarmTime between i_begin_day and i_end_day 
			and a.__md5 = b.__md5
      and a.redPoint = true 
	) then 

		set @redPoint = true;
	END if 
	;

	select @count as __count,@redPoint as redPoint;

END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for tj_frontpage_alarm_list
-- ----------------------------
DROP PROCEDURE IF EXISTS `tj_frontpage_alarm_list`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `tj_frontpage_alarm_list`(
# 首页统计 告警 违规 处置
	i_begin_day  date,
	i_end_day date,
	cz_or_wg  varchar(10)  # cz: 查询处置量   wg:查询违规量
)
pl:
BEGIN

	declare v_sql text;

	set i_end_day = DATE_ADD(i_end_day,INTERVAL 1 day);

	set v_sql = CONCAT(' select count(*) as count_ from alarm_list where 1=1 ',
		if(ifnull(i_begin_day,'1970-01-01')>'1970-01-01', concat(' and __alarmTime BETWEEN ''',i_begin_day,''' and ''',i_end_day,'''') ,''),
		case ifnull(cz_or_wg,'')
			when 'cz' then ' and cz_status <> ''NO'' '
			WHEN 'wg' then ' and cz_status not in (''NO'',''PASS'') '
			WHEN '' THEN ''
		END 
	);

		set @v_sql := v_sql;
		-- SELECT @v_sql;
		PREPARE S1 from @v_sql;		
		EXECUTE S1 ;
		DEALLOCATE PREPARE S1;
END
;
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for tj_frontpage_alarm_list_day
-- ----------------------------
DROP PROCEDURE IF EXISTS `tj_frontpage_alarm_list_day`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `tj_frontpage_alarm_list_day`(
	cz_or_wg  varchar(10)  # cz: 查询处置量   wg:查询违规量  '' 所有
)
BEGIN

	if cz_or_wg = '' then 
		select ifnull(max(count_),0)count_ from (
			select DATE_FORMAT(__alarmTime,'%Y-%m-%d')day_,count(*)count_ from alarm_list GROUP BY DATE_FORMAT(__alarmTime,'%Y-%m-%d')
		)a;
	elseif cz_or_wg = 'cz' then 
		select ifnull(max(count_),0)count_ from (
			select DATE_FORMAT(__alarmTime,'%Y-%m-%d')day_,count(*)count_ from alarm_list 
			where  cz_status <> 'NO'
			GROUP BY DATE_FORMAT(__alarmTime,'%Y-%m-%d')
		)a;
	elseif cz_or_wg = 'wg' then 
		select ifnull(max(count_),0)count_ from (
			select DATE_FORMAT(__alarmTime,'%Y-%m-%d')day_,count(*)count_ from alarm_list 
			where cz_status not in ('NO','PASS') 
			GROUP BY DATE_FORMAT(__alarmTime,'%Y-%m-%d')
		)a;
	end if;
END
;;
DELIMITER ;

-- ----------------------------
-- Procedure structure for tj_frontpage_alarm_platform
-- ----------------------------
DROP PROCEDURE IF EXISTS `tj_frontpage_alarm_platform`;
DELIMITER ;;
CREATE  PROCEDURE `tj_frontpage_alarm_platform`(
# 首页统计 告警 违规 处置 (按平台)
	i_begin_day  date,
	i_end_day date
)
pl:
BEGIN


	set i_end_day = DATE_ADD(i_end_day,INTERVAL 1 day);

	-- 平台1总量 
	select count(*) into @count_p1_all
	from alarm_list a
	where exists(select * from action_list b  where a.__md5 = b.__md5 and b.platform = 1)	
	and a.__alarmTime BETWEEN i_begin_day and i_end_day;

	-- 平台1处置量
	select count(*) into @count_p1_cz
	from alarm_list a
	where exists(select * from action_list b  where a.__md5 = b.__md5 and b.platform = 1)	
	and a.cz_status NOT IN ('NO')
	and a.__alarmTime BETWEEN i_begin_day and i_end_day;

		-- 平台1违规量
	select count(*) into @count_p1_wg
	from alarm_list a
	where exists(select * from action_list b  where a.__md5 = b.__md5 and b.platform = 1)	
	and a.cz_status not in ('NO','PASS')
	and a.__alarmTime BETWEEN i_begin_day and i_end_day;


	-- 平台2总量
	select count(*) into @count_p2_all
	from alarm_list a
	where a.platform = 2
	and a.__alarmTime BETWEEN i_begin_day and i_end_day;

	-- 平台2处置量
	select count(*) into @count_p2_cz
	from alarm_list a
	where a.platform = 2
	and a.cz_status NOT IN ('NO')
	and a.__alarmTime BETWEEN i_begin_day and i_end_day;

	-- 平台2违规量
	select count(*) into @count_p2_wg
	from alarm_list a
	where a.platform = 2
	and a.cz_status not in ('NO','PASS')
	and a.__alarmTime BETWEEN i_begin_day and i_end_day;

	
	-- 平台3总量
	select count(*) into @count_p3_all
	from alarm_list a
	where exists(select * from action_list b  where a.__md5 = b.__md5 and b.platform = 3)	
	and a.__alarmTime BETWEEN i_begin_day and i_end_day;

	-- 平台3处置量
	select count(*) into @count_p3_cz
	from alarm_list a
	where exists(select * from action_list b  where a.__md5 = b.__md5 and b.platform = 3)	
	and a.cz_status not in ('NO')
	and a.__alarmTime BETWEEN i_begin_day and i_end_day;

	-- 平台3违规量
	select count(*) into @count_p3_wg
	from alarm_list a
	where exists(select * from action_list b  where a.__md5 = b.__md5 and b.platform = 3)	
	and a.cz_status not in ('NO','PASS')
	and a.__alarmTime BETWEEN i_begin_day and i_end_day;


	-- 平台4总量
	select count(*) into @count_p4_all
	from alarm_list a
	where exists(select * from action_list b  where a.__md5 = b.__md5 and b.platform = 4)	
	and a.__alarmTime BETWEEN i_begin_day and i_end_day;


	-- 平台4处置量
	select count(*) into @count_p4_cz
	from alarm_list a
	where exists(select * from action_list b  where a.__md5 = b.__md5 and b.platform = 4)	
	and a.cz_status not in ('NO')
	and a.__alarmTime BETWEEN i_begin_day and i_end_day;

	-- 平台4违规量
	select count(*) into @count_p4_wg
	from alarm_list a
	where exists(select * from action_list b  where a.__md5 = b.__md5 and b.platform = 4)	
	and a.cz_status not in ('NO','PASS')
	and a.__alarmTime BETWEEN i_begin_day and i_end_day;

	

	select  @count_p1_all count_p1_all,@count_p1_cz count_p1_cz,@count_p1_wg count_p1_wg,
					@count_p2_all count_p2_all,@count_p2_cz count_p2_cz,@count_p2_wg count_p2_wg,
					@count_p3_all count_p3_all,@count_p3_cz count_p3_cz,@count_p3_wg count_p3_wg,
					@count_p4_all count_p4_all,@count_p4_cz count_p4_cz,@count_p4_wg count_p4_wg;


END
;;
DELIMITER ;

-- ----------------------------
-- Function structure for fun_action_list_getLastTime
-- ----------------------------
DROP FUNCTION IF EXISTS `fun_action_list_getLastTime`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` FUNCTION `fun_action_list_getLastTime`(
# 查询上次connectionTime时间
	i___md5   varchar(50)
) RETURNS varchar(50) CHARSET utf8mb4
    READS SQL DATA
BEGIN
	declare i_time datetime;
	select max(__connectTime) into i_time from action_list where __md5=i___md5;
	if i_time is not NULL then
		return DATE_FORMAT(i_time,'%Y-%m-%d %H:%i:%s');
	else
		return NULL;
	end if;
END
;;
DELIMITER ;

-- ----------------------------
-- Function structure for fun_alarm_list_exists
-- ----------------------------
DROP FUNCTION IF EXISTS `fun_alarm_list_exists`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` FUNCTION `fun_alarm_list_exists`(
# 查询是否存在
	i___md5   varchar(50)
) RETURNS tinyint(4)
    READS SQL DATA
BEGIN

	set @exist :=0;
	if exists (select __md5 from alarm_list where __md5=i___md5 and cz_status not in ('NO','PASS')) then 
		set @exist := 2;  # 存在且被判定为违规
	elseif exists (select __md5 from alarm_list where __md5=i___md5)THEN
		set @exist := 1;  # 仅存在
	else 
		set @exist := 0;
	end if;

	return @exist;
END
;;
DELIMITER ;

-- ----------------------------
-- Function structure for fun_translate_code
-- ----------------------------
DROP FUNCTION IF EXISTS `fun_translate_code`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` FUNCTION `fun_translate_code`(
# 转义字符
	i_keyword   varchar(200)  # 将keyword中的特殊字符串转译
) RETURNS varchar(200) CHARSET utf8mb4
    READS SQL DATA
BEGIN

	drop TEMPORARY table if exists translate_code;
	create TEMPORARY table translate_code(id int auto_increment PRIMARY key ,from_ varchar(10),to_ varchar(10));
	insert into translate_code(from_,to_)
	select `name`,`value` from  dict where `key` = 'translate_code';
	
	while exists(select * from translate_code)
	do 
		select id,from_,to_ into @id,@from_,@to_ from translate_code limit 1;

		set i_keyword = replace(i_keyword,@from_,@to_);
		delete from translate_code where id = @id;
	end while ;


	return i_keyword;
END
;;
DELIMITER ;


drop procedure if exists  tj_frontpage_alarm_sour;
DELIMITER ;;
CREATE PROCEDURE `tj_frontpage_alarm_sour`(
#统计首页右下角，人工加入的告警和自动加入的告警数据量
	i_begin_day  date,
	i_end_day date
)
pl:
BEGIN

	declare v_sql text;

	set i_end_day = DATE_ADD(i_end_day,INTERVAL 1 day);

	#security
	select '__security' as row_name, __alarmSour,count(*) as count_
	from alarm_list 
	where ifnull(__security,'') <>'' and __alarmTime BETWEEN i_begin_day and i_end_day
	group by __alarmSour

	union all 

	#关键字
	select '__alarmKey' , __alarmSour,count(*) 
	from alarm_list 
	where ifnull(__alarmKey,'[]') not in ('[]','') and __alarmTime BETWEEN i_begin_day and i_end_day
	group by __alarmSour

	union all 

	#__document
	select '__document' ,__alarmSour,count(*) 
	from alarm_list 
	where ifnull(__document,'') <>'' and __alarmTime BETWEEN i_begin_day and i_end_day
	group by __alarmSour

	union all 

	#__industry
	select '__industry', __alarmSour,count(*) 
	from alarm_list 
	where ifnull(__industry,'')not in ('' ,'其它类')  and __alarmTime BETWEEN i_begin_day and i_end_day
	group by __alarmSour;

END
;;
DELIMITER ;



drop procedure if exists pro_platform_edit;
DELIMITER ;;
CREATE PROCEDURE `pro_platform_edit`(
#编辑平台的简称、别名

	i_platformid   int,
	i_name  varchar(45), #名称
	i_nicname  varchar(45), #别名
	i_simname  varchar(45) #简称

)
pl:
BEGIN
	
	update dict set `name` = i_name,
							`desc` = i_nicname,
							remark = i_simname
	where `key` = 'platform' and `value` = i_platformid;

	select 0 as err, concat('修改平台',i_platformid,'成功')as msg;

END
;;
DELIMITER ;



drop procedure if exists pro_platform_query;
DELIMITER ;;
CREATE PROCEDURE `pro_platform_query`(
#查询平台的简称、别名
)
pl:
BEGIN
	
	select `value` as platformid,  
	`name` as i_name,
	`desc` as i_nicname,
	remark as i_simname
	from dict 
	where `key` = 'platform'  ;

END
;;
DELIMITER ;



