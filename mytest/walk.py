#!/usr/bin/python

import os

for path,d,filelist in os.walk('/home/sun/python/mytest'):
    for filename in filelist:
        print os.path.join(path,filename)
