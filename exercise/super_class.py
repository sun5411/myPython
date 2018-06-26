#!/usr/bin/env python
#coding:utf-8

class FooParent(object):
    def __init__(self):
        self.parent='I\'am the parent.'
        print('Parent')
    def bar(self,message):
        print (message,'from parent')


class FooChild(FooParent):
    def __init__(self):
        super(FooChild,self).__init__()
        print('child')
    def bar(self,message):
        super(FooChild,self).bar(message)
        print ('Child bar function')
        print (self.parent)

if __name__=='__main__':
	fooChild=FooChild()
	fooChild.bar('Hello World')
