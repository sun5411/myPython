#!/usr/bin/env python
#coding:utf-8

class IorderRepository:  ##接口
    def fetch_one_by(self,nid):
        '''
        获取单条数据的方法，所有的继承呢当前类的类必须继承
        :param nid:
        :return:
        '''
        # raise Exception('子类中必须包含该方法')
 
class OrderReposititory(IorderRepository): #类
    def fetch_one_by(self,nid):
        print(nid)
obj = OrderReposititory()
obj.fetch_one_by(1)
