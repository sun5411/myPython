#!/usr/bin/python

#coding:utf8

class Ren(object):
    name="ren"
    high="180cm"
    wigth="80kg"
    __money="100rmb"
    __age="30"

    def run(abc):
        print abc.name
        print "running..."

    def say(self):
        print self.__money

    def get(self,x):
        if x == "money":
            return self.__money
        else:
            return self.__age

    def set(self,x):
        self.__age=x

    @classmethod
    def moRi(self):
        print "Shi jie mo ri"

    @staticmethod
    def mr():
        print "static method"

zhang=Ren()
zhang.run()
zhang.say()
print Ren.__dict__
print zhang._Ren__money
print Ren.__module__

print zhang.get('age')
zhang.set(20)
print zhang.get('age')
print Ren.mr()
print Ren.moRi()
