#!/bin/bash
libs=`cat /data0/syncdata/tools/cid_ok|awk '{print $1}'`
#mysql -uroot  -p123456 -DAutoITI -e "LOAD DATA LOCAL INFILE '$filesql' INTO TABLE '$tableName'"
dbHost="10.10.1.170"
>dataRecord
for lib in $libs;do
	info=`mysql -upyuser -pyhzdatacenter -D C$lib -h $dbHost -e "select cinema_sell_time from cinema_sell_log ORDER BY cinema_sell_id DESC LIMIT 2"`
	echo $lib $info >> dataRecord
done

