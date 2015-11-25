#!/usr/bin/python
x="sun"

def fun():
    global x
    x=100

print x
fun()
print "end...",x
