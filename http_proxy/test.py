#!/usr/bin/env python  
# -*- coding:utf8 -*-  
import urllib2  
import requests
import time  
from bs4 import BeautifulSoup  
import sys  
import pdb
reload(sys)  
sys.setdefaultencoding( "utf-8" )  
req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',  
  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  
  #'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',  
  'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',  
  'Accept-Encoding':'en-us',  
  'Connection':'keep-alive',  
  'Referer':'http://www.baidu.com/'  
   }  
req_timeout = 5  
#testUrl = "http://www.baidu.com/"  
testUrl = "http://ip.chinaz.com/getip.aspx"  
testStr = "wahaha"  
file1 = open('proxy.txt' , 'w')  
# url = ""  
# req = urllib2.Request(url,None,req_header)  
# jsondatas = urllib2.urlopen(req,None,req_timeout).read()  
cookies = urllib2.HTTPCookieProcessor()  
checked_num = 0  
grasp_num = 0  

def validIP(ip,protocol):
    url="http://ip.chinaz.com/getip.aspx"
    try:
        proxy_host = protocol + "://" + ip
        html = requests.get(url,proxies = proxy_host,timeout=3)
        if(html.status_code == 200):
            print "ok"
        else:
            print "failed"
    except:
        print "error"

#for page in range(1, 160):  
for page in range(6, 10):  
    req = urllib2.Request('http://www.xici.net.co/nn/' + str(page), None, req_header)  
    html_doc = urllib2.urlopen(req, None, req_timeout).read()  
    soup = BeautifulSoup(html_doc)  
    trs = soup.find('table', id='ip_list').find_all('tr')  
    for tr in trs[1:]:  
        tds = tr.find_all('td')  
        ip = tds[1].text.strip()  
        port = tds[2].text.strip()  
        protocol = tds[5].text.strip()  
        if protocol == 'HTTP' or protocol == 'HTTPS':  
            grasp_num +=1  
            t1 = time.time()  
            proxies = {protocol : r'%s://%s:%s' % (protocol.lower(),ip, port)}
            try:  
                response = requests.get(testUrl, proxies=proxies, timeout=2)
                if response.status_code == 200:
                    print proxies
                else:
                    print "Failed proxy : " + str(proxies)
                timeused = time.time() - t1  
            except Exception,e:  
                continue  
file1.close()  
print checked_num,grasp_num  
