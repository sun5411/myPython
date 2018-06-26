#!/usr/bin/python
#coding:utf8

import requests
import os
import traceback
 
def retry(attempt):
    def decorator(func):
        def wrapper(*args, **kw):
            att = 0
            while att < attempt:
                try:
                    print "The %s times try ..."%(att)
                    return func(*args, **kw)
                except Exception as e:
                    att += 1
        return wrapper
    return decorator
 
# 重试次数
@retry(attempt=3)
def get_response(url):
    r = requests.get('http://www.oschina.net')
    return r.content

@retry(attempt=3)
def add():
    print "try..."
    try:
        if not os.path.exists('logs/sunning'):
            raise Exception("error....")
    except Exception,e:
        print traceback.format_exc()
        raise Exception(e)


add()
