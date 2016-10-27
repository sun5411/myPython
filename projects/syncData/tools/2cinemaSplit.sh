#!/bin/bash
clists=`cat newCidList|awk '{print $1}'`
>existed_lists
>nofile_lists
for cid in $clists;do
	ls /data0/binlog/ -lt|grep $cid|grep sql.gz >/dev/null
	if [[ $? -eq 0 ]];then
		echo $cid >> existed_lists 
	else
		echo "The CIDs without sql files: "
		echo $cid
		echo $cid >> nofile_lists 
	fi
done
