#!/usr/bin/env python
#coding:utf-8

import datetime
s='1985-05-11'
start=datetime.datetime.strptime(s,'%Y-%m-%d')
end=datetime.datetime.today()
print (end-start).days
