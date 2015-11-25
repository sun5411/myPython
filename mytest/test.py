#!/usr/bin/python

import os

for path,d,filelist in os.walk('/home/sun/python/mytest'):
    for f in filelist:
        print os.path.join(path,f)
