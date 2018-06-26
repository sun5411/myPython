#!/usr/bin/env python
#coding:utf-8

import urllib

url="http://www.iplaypython.com/"
#url="http://www.163.com/"
urllib.urlretrieve(url,"./urlretrieve.html")
html = urllib.urlopen(url)
#print html.read()
#print html.info()
#print html.headers
#print html.getcode()

html.close()
