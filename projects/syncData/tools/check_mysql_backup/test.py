#!/usr/bin/env python
#conding:utf-8
import re

patt = re.compile(r':(\d+.\d+)')

f = open('/data0/binlog/11010661-2016-01-20.txt','r')
content=f.read()
print patt.findall(content)

#print patt.findall(content)
