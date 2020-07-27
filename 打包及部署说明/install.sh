#!/bin/bash

fname=$1
targetpath=/opt/wangan/yth_data_api
mysql_host=192.168.40.163
mysql_pwd=123asd!@#ASD
upgrade=0

service yth_data_api stop

echo 'Start install...'
if [ ! -n "${fname}" ] ;then
 fname=yth_data_api.zip
fi

if [ ! -d "/opt/wangan" ]; then
  mkdir /opt/wangan
fi
echo "1.uninstall old version if exist!"
rm -rf ${targetpath}

echo "2.install package to /opt/wangan"
unzip -o ${fname} -d /opt/wangan
# mv /opt/wangan/${fname%.*} ${targetpath}

echo "3.create venv"
python3 -m venv ${targetpath}/venv
source ${targetpath}/venv/bin/activate
pip install --no-index --find-links=${targetpath}/packs/ -r ${targetpath}/requirements.txt
cd ${targetpath}
#python app/config/config.py
cd -

echo '4.create service'
mv -f ${targetpath}/yth_data_api /etc/init.d/
chmod +x /etc/init.d/yth_data_api
chkconfig --add /etc/init.d/yth_data_api
service yth_data_api start

if [ ${upgrade} = 0 ] ;then
echo '5.import mysql schema'
mysql -h ${mysql_host} -u root -p${mysql_pwd}  < yth_alarm_schema.sql

echo '6.import mysql data'
mysql -h ${mysql_host} -u root -p${mysql_pwd}  < yth_alarm_data.sql
fi

#if [ ${upgrade} = 1 ] ;then
#echo '56.upgrade mysql '
#mysql -h ${mysql_host} -u root -p${mysql_pwd}  < upgrade0807.sql
#fi

if [ ${upgrade} = 0 ] ;then
echo '7.import es script'
sh es.sh
fi

if [ ${upgrade} = 0 ] ;then
echo '8.install large screen mysql '
mysql -h ${mysql_host} -u root -p${mysql_pwd}  < yth_ls_schema.sql
fi

echo 'Install finished!'
