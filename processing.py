#!/usr/bin/env python
#coding:utf-8

from multiprocessing import Pool
import time


def job(num):
    print num
    time.sleep(1)

p = Pool(processes=3)
for i in range(6):
    p.apply_async(job,args=(i,))

p.close()
p.join()
