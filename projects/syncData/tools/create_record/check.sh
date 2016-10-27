#!/bin/bash
while read line;do
	cat "record_"$line|grep $line > /dev/null
	[[ $? -eq 0 ]] || echo "###please check file record_$line"
	filename=`cat "record_"$line|awk '{print $1}'`
	ls /data0/binlog/|grep $filename > /dev/null
	[[ $? -eq 0 ]] || echo "###Haven't file $filename"
done < cids
