#!/usr/bin/env python
#coding:utf-8

def feb(n):
	a,b,i = 0,1,0
	while i < n:
		yield b
		a,b = b,a+b
		i = i + 1



ss = feb(5)
for num in ss:
	print num

for num in ss:
	print num
