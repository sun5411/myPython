#!/usr/bin/python

def func(x,*args,**kwargs):
    print x
    print args
    print kwargs

func(1,2,3,4,5,6,y=30,name='Ning')
