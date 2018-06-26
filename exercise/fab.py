#!/usr/bin/env python

#coding:utf-8
def feb(max):
	n,a,b = 0,0,1
	while n < max:
		print b
		a,b = b,a+b
		n=n+1	

feb(10)
