#!/usr/bin/env python
#coding:utf-8

import urllib

def callback(a,b,c):
    """
    @a : 目前为止传递的数据块数量
    @b : 每个数据块的大小，单位是byte
    @c : 远程文件大小
    """
    down_program = 100.0 * a * b / c
    if down_program > 100:
        down_program = 100
    print "%.2f%%"%down_program

url="http://www.iplaypython.com/"
url2="http://www.python.org"
local="./urlretrieve.html"
#urllib.urlretrieve(url,local,callback)
urllib.urlretrieve(url2,local,callback)
