#!/usr/bin/env python
#coding:utf-8

def gensquares(n):
	for i in range(n):
		yield i**2

for item in gensquares(5):
	print item
