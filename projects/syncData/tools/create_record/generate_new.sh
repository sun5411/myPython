#!/bin/bash
sample="./sample_record"
string=`cat $sample |awk -F'-' '{print $1}'`
while read line;do
	\cp $sample "record_"${line}
	sed  -i "s/${string}/${line}/g" "record_"${line}
done < cids
