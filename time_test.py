#!/usr/bin/env python
import datetime
import time

def Caltime(start,end):
    start=time.strptime(start,"%Y-%m-%d_%H:%M:%S")
    end=time.strptime(end,"%Y-%m-%d_%H:%M:%S")
    start=datetime.datetime(start[0],start[1],start[2],start[3],start[4],start[5])
    end=datetime.datetime(end[0],end[1],end[2],end[3],end[4],end[5])
    return end-start

print Caltime("2015-12-24_10:06:07","2015-12-24_10:26:04")


