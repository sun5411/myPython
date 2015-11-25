#!/usr/bin/python

def f(x,*args):
    print x
    print args

def f2(x,*args,**kwargs):
    print x,args,kwargs

a=333

f(a,4,5,6)
f2(a,7,8,9,10,999,y=10,z='sun')

