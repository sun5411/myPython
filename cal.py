#!/usr/bin/python

from __future__ import division

#def jia(x,y):
#    return x+y
#def jian(x,y):
#    return x-y
#def cheng(x,y):
#    return x*y
#def chu(x,y):
#    return x/y
#
#
#opers={"+":jia,"-":jian,"*":cheng,"/":chu}
#
#def f(x,o,y):
#    print opers.get(o)(x,y)
#f(4,"+",2)
#f(4,"-",2)
#f(4,"*",2)
#f(3,"/",2)
x=int(raw_input("Please input x: "))
y=int(raw_input("Please input y: "))

results={
        "+":x+y,
        "-":x-y,
        "*":x*y,
        "/":x/y
        }

print results.get("+")
print results.get("-")
print results.get("*")
print results.get("/")
