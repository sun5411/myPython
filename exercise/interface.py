#!/usr/bin/env python
#coding:utf-8

from abc import ABCMeta,abstractmethod

class Alert():
	__metaClass__ = ABCMeta #抽象类

	@abstractmethod #抽象方法
	def Send(self):
		pass

class Foo(Alert):
	def __init__(self):
		print '__init__'

	#@abstractmethod
	#def Send(self):
	#	print 'Foo test...'

f = Foo()
f.Send()
