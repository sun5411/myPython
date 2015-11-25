#!/usr/bin/python

def dict(name,age):
    print "Name : %s, Age : %s" %(name,age)

d={'age':30,'name':'SunNing'}

dict(**d)
