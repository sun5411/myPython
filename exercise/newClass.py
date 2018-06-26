#!/usr/bin/env python
#coding:utf-8

#class A: #经典类
class A(object): #新式类
	def __init__(self):
		print 'This is A'
	def save(self):
		print 'save method from A'

class B(A):
	def __init__(self):
		print 'This is B'

class C(A):
	def __init__(self):
		print 'This is C'
	def save(self):
		print 'save method from C'

 
# 继承从左到右，经典类深度优先，新式类广度优先
class D(B,C):
	def __init__(self):
		print 'This is D'

c = D()
c.save()
