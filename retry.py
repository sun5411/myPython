#!/usr/bin/env python
#coding:utf-8
import time
import os

def retry(attempt):
    def decorator(func):
        def wrapper(*args, **kw):
            att = 0
            while att < attempt:
                try:
                    print "The %s times try ..."%(att)
                    return func(*args, **kw)
                except Exception as e:
                    time.sleep(1)
                    att += 1
        return wrapper
    return decorator

@retry(attempt=5)
def test(cmd):
    status = None
    try:
        ret = os.system(cmd)
        if ret != 0:
            status = False
            print "Error : upload sourceFile into hdfs dir failed! ret: %s,  command : %s"%(ret,cmd)
            raise("err....")
        else:
            status = True
    except Exception, e:
        print traceback.format_exc()
        print e
    return status


aaa = test('ls fajdifjaosdf')
print "**" * 30
if aaa:
	print "ok"
else :
	print "failed"
