#!/usr/bin/python
def f(x,*args,**kargs):
    print "x:",x
    print "args:",args
    print "Kargs:",kargs

f(1,2,3,4,5)

f(1,2,3,45,y=6,z=99)
