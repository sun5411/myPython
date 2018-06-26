#!/usr/bin/env python
#coding:utf-8

t1 = (123,456,67)
l1 = [111,'aaa',22.22]

t = iter(t1)
l = iter(l1)

for a in t:
	print a
for b in l:
	print b
