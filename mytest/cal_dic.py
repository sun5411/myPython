#!/usr/bin/python

from __future__ import division

def jia(x,y):
    return x+y
def jian(x,y):
    return x-y
def chu(x,y):
    return x/y
def cheng(x,y):
    return x*y

d={'+':jia,'-':jian,'*':cheng,'/':chu}

print d["*"](5,3)
print d["+"](5,3)
print d["-"](5,3)
print d["/"](5,3)
