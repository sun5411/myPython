#!/bin/bash

file1="bbb"
file2="aaa"

strings=`cat $file1|awk '{print $1}'`

for string in $strings;do
    lineNo=`sed -n "/${string}/=" $file2`
    echo "sed -n "/${string} -Dnimbula/=" $file2"
    if [ "$lineNo" == "" ];then
        echo "###### $string is't existed in scripts ######"
        #echo $string >> ./bbb
    else
        echo "###### lineNo : $lineNo, Cases : $string"
        sed -i -e "$lineNo s/^/###/g" $file2
    fi
done

