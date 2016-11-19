#!/usr/bin/env python
#coding:utf-8
import re
#movielist = {'cid':"100",'timeStamp':"1451463515",'movies':[["1","001103112015","侏罗纪世界",180],["2","001103122015","火星救援",190],["2","001103122015","火星救援",160]]}


#for i in movielist:
#    print movielist[i]
#for k in movielist.keys():
#    print movielist[k]
###################
#s = "/*!*/;SunNing"
#
#
#s = s.strip('/*!*/;')
#print s
#
#if not s:
#    print "OK"
#else:
#    print s    
#
###############
#list = [['key1','value1'],['key2','value2'],['key1','value3']]
#d = {}
#
#for k,v in list:
#    d.setdefault(k,[]).append(v)
#
#print d.items()

sum = 5
def add(x, y):
    global sum
    print sum
    sum = x + y
    print sum

if __name__ == '__main__':
    #add(7, 8)
