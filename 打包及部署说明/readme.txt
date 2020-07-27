安装目录为：/opt/wangan/yth_data_api/
1.安装前，若有必要（比如es端口变了等情况），先修改es.sh开头的：
host=127.0.0.1
port=9200


2.修改install.sh中的mysql_host和mysql_pwd,然后 执行install.sh

注意：此安装包只能把大屏和一体化的数据库安装在同一服务器上，后期会改


3. 需要修改的配置：
/opt/wangan/yth_data_api/目录下，config.json文件里有 es，mysql，hbase 的连接信息

4. 重启api服务：service yth_data_api restart
