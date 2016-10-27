#!/bin/bash
cids=`cat cid_err|awk '{print $1}'`
#mysql -uroot  -p123456 -DAutoITI -e "LOAD DATA LOCAL INFILE '$filesql' INTO TABLE '$tableName'"
for cid in $cids;do
	echo $cid
	info=`mysql -uroot -pcine123456 -D cinema_imp_record  -h 172.16.8.1 -e "update available_CID set ciname_flag=0 where cID=$cid"`
done

