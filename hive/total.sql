



-- ----------------------------
--  检测器
-- ----------------------------
drop database endpoint cascade;
create database if not exists endpoint comment '检测器';

-- 传输涉密：外部分区表
drop table if exists endpoint.sensitive_raw;
create external table endpoint.sensitive_raw(json string)
partitioned by (lts_ym string,lts_d string) ;



-- 检测信息表
drop table if exists endpoint.dtr_info_raw;
CREATE external TABLE endpoint.dtr_info_raw (
	dtr_id string,
	mfr_name string ,
	organs string ,
	address string,
	address_code string,
	contact string,
	memo string ,
	device_type string ,
	soft_version string 
)
COMMENT '检测器信息表'
row format delimited
fields terminated by '|'
;



-- 规则表
drop table if exists endpoint.dtr_rules_raw;
CREATE external TABLE endpoint.dtr_rules_raw (
	rule_type string,
	min_match_count int,
	rule_content string,
	type string,
	rule_id string,
	risk int
)
COMMENT '检测器信息表'
row format delimited
fields terminated by '|';






  
 
-- ----------------------------
--  三合一告警（无文件）
-- ---------------------------- 
drop database csmp cascade;
create database if not exists csmp comment '三合一违规外联';
 
drop table csmp.logex_raw;
CREATE external TABLE csmp.logex_raw (
  lts   bigint  , -- 写在文件中，用time.time()生成，用于取数据 （load timestamp的缩写）
  lts_ym    string, -- '201901'  年月
  lts_d     string, -- '01'  日
  LOG_ID varchar(35) ,
  LOG_CLASS varchar(10) ,
  MACHINE_NAME varchar(255) ,
  LOG_TYPE varchar(10) ,
  USER_INFO varchar(255) ,
  LOG_IP varchar(20) ,
  
  -- LOG_DESC需要拆分成如下字段
  user_   string,
  zone	 string,
  unit   string,
  ncard  string,
  reserved1_ string,
  ver	string,
  date_ string,
  company string,
  mboard string,
  dept string,
  hdid  string,
  os string,
  hostname string,
  ip string,
  mac string,
  desc_ string,
  
  LOG_DATE string ,
  RECV_DATE string ,
  LOG_SIGN varchar(40) ,
  RESERVED1 varchar(255) ,
  RESERVED2 varchar(255) ,
  RESERVED3 varchar(255) 
)
comment '违规外联原始数据'
row format delimited
fields terminated by '|'
;




 
-- ----------------------------
--  文档审计（有文件）
-- ---------------------------- 
drop database docaudit cascade;
create database if not exists docaudit comment '文档审计';




DROP table if exists docaudit.netward_raw;
CREATE external TABLE docaudit.netward_raw (
	lts  bigint,
	lts_ym  string,
	lts_d string,
	id int ,
	date_ string ,
	unit_id int ,
	g_attribute varchar(40) ,
	depart varchar(40) ,
	g_unit_name varchar(45) ,
	user_ varchar(50) ,
	ip varchar(16) ,
	mac varchar(25) ,
	hostname varchar(25) ,
	keywords varchar(128) ,
	summary varchar(128) ,
	title varchar(255) ,
	filename varchar(255) ,
	filemd5  string, -- 找到的文件
	fileaction varchar(10) ,
	secretkeyid int ,
	filepath varchar(255) ,
	scan int ,
	state int  ,
	type int  ,
	reason varchar(16) ,
	auditor varchar(255) ,
	dealwith int ,
	filename_a string  -- 绝对文件名
)
row format delimited
fields terminated by '|'
;


DROP table if exists docaudit.netward_md5_raw;
CREATE external TABLE docaudit.netward_md5_raw (
	id int ,
	filemd5  string -- 找到的文件
)
row format delimited
fields terminated by '|'
;





drop table if exists docaudit.user_status_raw;
CREATE external TABLE docaudit.user_status_raw (
  id int ,
  g_attribute varchar(25) ,
  g_office varchar(25) ,
  department varchar(25) ,
  g_unit_name varchar(45) ,
  username varchar(50) ,
  ip varchar(16) ,
  mac varchar(25) ,
  reg_time string,
  opt_time string,
  opt_status varchar(10) ,
  online_flag int ,
  online_time string 
)
row format delimited
fields terminated by '|'
;





drop table if exists docaudit.useradmin_raw;
CREATE external TABLE docaudit.useradmin_raw (
  id int ,
  user_name varchar(50) ,
  host_name varchar(50) ,
  OrdinalNumber int ,
  user_ip varchar(16) ,
  GAttribute varchar(40) ,
  UnitName varchar(128) ,
  GDepartment varchar(40) ,
  diskOrdinaNumber varchar(255) 
)
row format delimited
fields terminated by '|'
;






-- ----------------------------
--  门户网站
-- ---------------------------- 
drop database menhu cascade;
create database if not exists menhu comment '门户网站';

drop table if exists menhu.website_raw;
create external table menhu.website_raw(	
	id      int comment '系统内唯一标识',
	name		varchar(200) comment '网站名称',
	url		varchar(512)  comment '入口地址',
	unittype		varchar(100) comment '网站类型',
	ip		varchar(50),
	ISP	varchar(100) comment '网络提供商',
	MAINLICENSE	varchar(100) comment '备案信息',
	company	varchar(200) comment '网站使用单位'	,
	person	varchar(200)  comment '网站负责人',
	phone	varchar(50) comment'联系电话'
)
comment '文章内容（原始）'
row format delimited
fields terminated by '|'
;

drop table if exists menhu.article_raw;
create external table menhu.article_raw(
	lts  bigint,
	lts_ymd string,
	lts_d string,
	id      int comment '系统内唯一标识',
	website_id	int comment 'menhu.website表id',
	md5hash	varchar(100) comment '文章指纹MD5',
	title	VARCHAR(100) comment '标题'	,	
	summary	VARCHAR(1000) comment '摘要',	
	url	varchar(512) comment '文章链接'	,	
	crawldate string	comment '采集时间',		
	pubdate	string  comment'发布时间'	,	
	pubuser	varchar(100) comment '发布人'	,	
	host	varchar(100) comment '网站入口地址'	,	
	wordfreqs	string comment '高频词'	,
	filename string 
)
comment '文章内容（原始）'
row format delimited
fields terminated by '|'
stored as textfile
-- tblproperties("orc.compress"="SNAPPY")
;



drop table if exists menhu.article_orc;
create  table menhu.article_orc(
	lts  bigint,
	lts_ymd string,
	lts_d string,
	id      int comment '系统内唯一标识',
	website_id	int comment 'menhu.website表id',
	md5hash	varchar(100) comment '文章指纹MD5',
	title	VARCHAR(100) comment '标题'	,	
	summary	VARCHAR(1000) comment '摘要',	
	url	varchar(512) comment '文章链接'	,	
	crawldate string	comment '采集时间',		
	pubdate	string  comment'发布时间'	,	
	pubuser	varchar(100) comment '发布人'	,	
	host	varchar(100) comment '网站入口地址'	,	
	wordfreqs	string comment '高频词'	,
	filename string 
)
comment '文章内容（orc）'
clustered by (website_id)  into 1 buckets
stored as ORC
tblproperties("orc.compress"="SNAPPY")
;




-- 门户网站告警数据佳节入库
drop table if exists menhu.alarm_raw;
create  table menhu.alarm_raw(
    id   bigint,
	lts  bigint,
	lts_ym string,
	lts_ymd	string comment '20190201',
	title string,
	summary string, 
	alarm_level int,
	file_md5 string,	
	url string comment '文章链接'	,	
	crawldate string	comment '采集时间',		
	pubdate	string  comment'发布时间'	,	
	pubuser	string comment '发布人'	,	
	host	string comment '网站入口地址'	,	
	wordfreqs	string comment '高频词'	,
	filename string,
	website_name	string comment '网站名称',
	website_url		string  comment '入口地址',
	unittype	string comment '网站类型',
	ip		string,
	ISP	 string comment '网络提供商',
	MAINLICENSE	string comment '备案信息',
	company	string comment '网站使用单位'	,
	person	string  comment '网站负责人',
	phone	string comment'联系电话'	
)
comment '门户网站告警数据佳节入库'
row format delimited
fields terminated by '|'
stored as textfile
;









-- ----------------------------
--  融合数据
-- ---------------------------- 
drop database wdp cascade;
create database if not exists wdp comment '融合数据';




drop table if exists  wdp.alarm_wgxw;
create  table wdp.alarm_wgxw(
	auid   bigint,
	lts  	bigint,
	platform string,
	sour_obj string,
	sour_obj_sub string,
	wgxw_type int comment'违规行为类型', 
	title string,
	unit  string,
	duty string,
	alarm_desc string, 
	alarm_level int,
	deepana_status int, -- 0未分析  1已分析
	tag string, -- 关键字 标签
	file_count int,
	table_name string,
	table_id string,
	file_md5 string,
	search_fields string , -- 查询大杂烩字段
	star int,
	chuzhi_status int,
	chuzhi_desc string,
	deepana_lts bigint -- 用于深度分析统计的游标
)
comment '违规行为告警数据'
partitioned by (lts_ymd string)  
clustered by(alarm_level) sorted by (lts desc,auid desc) into 5 buckets 
STORED AS ORC
tblproperties("ORC.COMPRESS"="SNAPPY");


drop table if exists wdp.deepana_wgxw;
create  table wdp.deepana_wgxw(
	file_md5 string,
	alarm_level  int,
	lts bigint,
	json string	
)
comment '违规行为告警深度分析'
partitioned by (lts_ymd string)  
clustered by (alarm_level) sorted by (lts desc) into 5 buckets
STORED AS ORC;



drop table if exists wdp.deepana_wgxw_raw;
create  table wdp.deepana_wgxw_raw(
	json string	
)
comment '违规行为告警深度分析(此表入到orc表以后会删除)'
STORED AS textfile;



