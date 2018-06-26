#!/usr/bin/env python
#coding:utf-8

import urllib
import chardet

def getCoding(url):
    content = urllib.urlopen(url).read()
    result = chardet.detect(content)
    return result['encoding']

urls=["http://www.iplaypython.com/",
      "http://www.baidu.com",
      "http://www.163.com",
      "http://www.jd.com",
      "http://www.dangdang.com"
      ]
for url in urls:
    print url,getCoding(url)
#url="http://www.iplaypython.com/"
#url2="http://www.python.org"
#url1="http://www.tudou.com"
#urllib.urlretrieve(url,local,callback)
#content=urllib.urlopen(url).read()
#coding=chardet.detect(content)
#print coding['encoding']
#print info.getparam('charset')

#print getCoding(url)
#print getCoding(url2)
