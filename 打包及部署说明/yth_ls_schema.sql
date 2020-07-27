/*
MySQL Backup
Source Server Version: 5.7.25
Source Database: yth_ls
Date: 2019/8/15 13:58:34
*/

SET FOREIGN_KEY_CHECKS=0;
CREATE DATABASE IF NOT EXISTS yth_ls  DEFAULT CHARSET utf8mb4 COLLATE utf8mb4_general_ci;
use yth_ls;
SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
--  Table structure for `ls_alarm`
-- ----------------------------
DROP TABLE IF EXISTS `ls_alarm`;
CREATE TABLE `ls_alarm` (
  `day_` int(11) NOT NULL,
  `province` char(6) NOT NULL,
  `city` char(6) NOT NULL,
  `district` char(6) NOT NULL,
  `unit` int(11) NOT NULL,
  `__alarmType` varchar(100) NOT NULL,
  `__alarmLevel` int(11) NOT NULL,
  `cz_status` char(10) NOT NULL,
  `count_` bigint(20) DEFAULT NULL,
  `last_auid` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`day_`,`province`,`city`,`district`,`unit`,`__alarmType`,`__alarmLevel`,`cz_status`),
  KEY `ix_geo` (`province`,`city`,`district`,`unit`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
--  Procedure definition for `fun_geo_where`
-- ----------------------------
DROP FUNCTION IF EXISTS `fun_geo_where`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` FUNCTION `fun_geo_where`(
	i_province		char(6),
	i_city				char(6),
	i_district		char(6)
) RETURNS text CHARSET utf8mb4
    READS SQL DATA
BEGIN

	DECLARE o_where  text;

	set o_where = '';

	if i_province<>'' then 
		set o_where = concat(' and province = ''', i_province, '''');
	end if;

	if i_city<>'' then 
		set o_where = concat(o_where,' and city = ''', i_city, '''');
	end if;

	if i_district<>'' then 
		set o_where = concat(o_where,' and district = ''', i_district, '''');
	end if;


	return o_where;
END
;;
DELIMITER ;

-- ----------------------------
--  Procedure definition for `job_import_ls_alarm`
-- ----------------------------
DROP PROCEDURE IF EXISTS `job_import_ls_alarm`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `job_import_ls_alarm`(
)
pl:
BEGIN

	declare i json;

	SET @last_auid :=0;
	select ifnull(max(last_auid),0) into @last_auid from ls_alarm;

	insert into ls_alarm(
	day_ ,
	`province`,
  `city`,
  `district`,
  `unit`,
	__alarmType,
  `__alarmLevel`,
  `cz_status`,
	count_,
	last_auid )
	select * from (
	select DATE_FORMAT(__alarmTime,'%y%m%d'),ifnull(province,''),ifnull(city,''),
				ifnull(district,''),ifnull(unit,0),__alarmType,__alarmLevel,cz_status,count(*)count__,
				max(auid)
  from yth_alarm.alarm_list 
	WHERE auid > 761
	group by DATE_FORMAT(__alarmTime,'%y%m%d'),province,city,district,unit, __alarmLevel,__alarmType,cz_status)a
	on DUPLICATE key update  count_ = count_+a.count__

;

END
;;
DELIMITER ;

-- ----------------------------
--  Procedure definition for `pro_alarm_alarmtype`
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_alarm_alarmtype`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_alarm_alarmtype`(
#告警类型分布
	i_begin_day   int,  #190812
	i_end_day     int, #190812
	
	i_province		char(6),
	i_city				char(6),
	i_district		char(6)

)
pl:
BEGIN
	set @where_geo = `fun_geo_where`(i_province,i_city,i_district);

	set @sql_ = CONCAT('
		select __alarmtype,sum(count_)count_ from ls_alarm 
		where day_ BETWEEN ',i_begin_day, ' and ',i_end_day ,
		@where_geo,'			
		group by __alarmtype;	');

	PREPARE S1 from @sql_;		
	EXECUTE S1 ;
	DEALLOCATE PREPARE S1;

END
;;
DELIMITER ;

-- ----------------------------
--  Procedure definition for `pro_alarm_alarmtype_alarmlevel`
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_alarm_alarmtype_alarmlevel`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_alarm_alarmtype_alarmlevel`(
#告警级别分布
	i_begin_day   int,  #190812
	i_end_day     int,  #190812
	
	i_province		char(6),
	i_city				char(6),
	i_district		char(6)
)
pl:
BEGIN
/*
select __alarmtype,__alarmlevel,sum(count_)count_ , 
	sum(case when cz_status <>'NO' then count_ else 0 end )count_yes,
	sum(case when cz_status ='PASS' then count_ else 0 end )count_pass,
	SUM(CASE when cz_status not in ('NO','PASS') then count_ else 0 end )count_bad
from ls_alarm 
group by __alarmtype,__alarmlevel



*/

	set @where_geo = `fun_geo_where`(i_province,i_city,i_district);

	set @sql_ = CONCAT('
	select __alarmtype,__alarmlevel,sum(count_)count_ , 
	sum(case when cz_status <>''NO'' then count_ else 0 end )count_yes,
	sum(case when cz_status =''PASS'' then count_ else 0 end )count_pass,
	SUM(CASE when cz_status not in (''NO'',''PASS'') then count_ else 0 end )count_bad
	from ls_alarm 
	where day_ BETWEEN ',i_begin_day, ' and ',i_end_day ,
		@where_geo,'			
	group by __alarmtype,__alarmlevel	');

	PREPARE S1 from @sql_;		
	EXECUTE S1 ;
	DEALLOCATE PREPARE S1;
END
;;
DELIMITER ;

-- ----------------------------
--  Procedure definition for `pro_alarm_cz_status`
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_alarm_cz_status`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_alarm_cz_status`(
#处置结果分布
	i_begin_day   int,  #190812
	i_end_day     int, #190812

	
	i_province		char(6),
	i_city				char(6),
	i_district		char(6)
)
pl:
BEGIN

	/*
	select __alarmtype,
		sum(case when cz_status='JIMI' then count_ else 0 end)as count_jimi, 
		sum(case when cz_status='MIMI' then count_ else 0 end)as count_mimi, 
		sum(case when cz_status='JUEMI' then count_ else 0 end)as count_juemi 
	from ls_alarm 	
	group by __alarmtype
	*/

	set @where_geo = `fun_geo_where`(i_province,i_city,i_district);

	set @sql_ = CONCAT('
	select __alarmtype,
		sum(case when cz_status=''JIMI'' then count_ else 0 end)as count_jimi, 
		sum(case when cz_status=''MIMI'' then count_ else 0 end)as count_mimi, 
		sum(case when cz_status=''JUEMI'' then count_ else 0 end)as count_juemi 
	from ls_alarm
	where day_ BETWEEN ',i_begin_day, ' and ',i_end_day ,
	@where_geo,'
	group by __alarmtype');

	PREPARE S1 from @sql_;		
	EXECUTE S1 ;
	DEALLOCATE PREPARE S1;
	

 
END
;;
DELIMITER ;

-- ----------------------------
--  Procedure definition for `pro_alarm_cz_trend`
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_alarm_cz_trend`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_alarm_cz_trend`(
#处置趋势 ， 所谓趋势，就是按天给出数据（没有数据的天，不出现！）
	i_begin_day   int,  #190812
	i_end_day     int, #190812

	
	i_province		char(6),
	i_city				char(6),
	i_district		char(6)
)
pl:
BEGIN
/*
	
	select day_,sum(count_)count_, sum(case when cz_status <>'NO' then count_ else 0 end )count_yes
	from ls_alarm 	
	group by day_

*/


	set @where_geo = `fun_geo_where`(i_province,i_city,i_district);

	set @sql_ = CONCAT('
	select day_,sum(count_)count_ ,
	sum(case when cz_status <>''NO'' then count_ else 0 end )count_yes
	from ls_alarm 	
	where day_ BETWEEN ',i_begin_day, ' and ',i_end_day ,
		@where_geo,'			
	group by day_');

	PREPARE S1 from @sql_;		
	EXECUTE S1 ;
	DEALLOCATE PREPARE S1;
	

 
END
;;
DELIMITER ;

-- ----------------------------
--  Procedure definition for `pro_event_trend`
-- ----------------------------
DROP PROCEDURE IF EXISTS `pro_event_trend`;
DELIMITER ;;
CREATE DEFINER=`root`@`%` PROCEDURE `pro_event_trend`(
#事件趋势图，按天统计
	i_begin_day   int,  #190812
	i_end_day     int, #190812

	
	i_province		char(6), #这个参数目前不应该为空串
	i_city				char(6), #这个参数若不是空串，意味着查询某个市的下属区 ; 若这个参数是空串，则意味着查询某个省下属的市
	i_district		char(6)  #这个参数应该永远传空串
)
pl:
BEGIN

/*
	select DATE_FORMAT(add_time,'%y%m%d')day_,count(*)count_ 
	from yth_alarm.event_list 
	group by DATE_FORMAT(add_time,'%y%m%d')
*/

	set @where_geo = `fun_geo_where`(i_province,i_city,i_district);
	set @sql_ = CONCAT('
		select day_,count(*)count_ 
		from (select id,DATE_FORMAT(add_time,''%y%m%d'')day_,province,city,district from yth_alarm.event_list)a
		where day_ BETWEEN ',i_begin_day, ' and ',i_end_day ,
		@where_geo,'			
		group by day_;	');

	PREPARE S1 from @sql_;		
	EXECUTE S1 ;
	DEALLOCATE PREPARE S1;
END
;;
DELIMITER ;

-- ----------------------------
--  Records 
-- ----------------------------
INSERT INTO `ls_alarm` VALUES ('190812','','','','0','1','5','JUEMI','6','445'), ('190812','','','','0','1','5','NO','258','703'), ('190812','','','','0','2','0','NO','4','1034'), ('190812','','','','0','2','2','MIMI','1','710'), ('190812','','','','0','2','2','NO','6051','761'), ('190812','','','','0','2','3','NO','789','759'), ('190812','','','','0','2','5','NO','1','704'), ('190813','','','','0','2','2','NO','6452','4282'), ('190813','','','','0','2','3','NO','808','4283'), ('190813','','','','0','2','3','PASS','4','3744'), ('190813','','','','0','2','5','NO','32','4284'), ('190813','','','','0','2','5','PASS','8','4278');
