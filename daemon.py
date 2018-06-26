#!/usr/bin/env python

import time
import os
time.sleep(1)
f=open("log",'a')
t=time.time()
f.write(str(t))
f.write("\n")
f.close()
