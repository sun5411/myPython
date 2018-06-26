#!/usr/bin/env python
#coding:utf-8

import requests

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
r = requests.get("http://127.0.0.1:5000/index",headers=headers)
print r.text
