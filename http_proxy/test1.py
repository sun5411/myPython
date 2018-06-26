#!/usr/bin/env python  
# -*- coding:utf8 -*-  
import urllib2  
import requests
import time  
from bs4 import BeautifulSoup  
import sys  

#reload(sys)  
#sys.setdefaultencoding( "utf-8" )  
req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',  
  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',  
  #'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',  
  'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',  
  'Accept-Encoding':'en-us',  
  'Connection':'keep-alive',  
  'Referer':'http://www.baidu.com/'  
   }  

def available_check(proxy):
    test_url ='http://www.jd.com/?cu=true&utm_source=click.linktech.cn&utm_medium=tuiguang&utm_campaign=t_4_A100220955&utm_term=7e7c13a102664ab3a6886ccefa66d930&abt=3'  
    another_url = 'https://www.taobao.com/' 
    res = urllib.urlopen(self.test_url, proxies=proxy_temp).read()
    res2 = urllib.urlopen(self.another_url, proxies=proxy_temp).read()
    soup = BeautifulSoup(res)
    soup2 = BeautifulSoup(res2)  
    ans = soup.find('link', rel='dns-prefetch')  
    ans2 = soup2.find('link', rel='dns-prefetch')
    if ans == None or ans2 == None:
        return False
    else:
        return True

def fetch_xici():
    #for page in range(1, 160):  
    req_timeout = 1  
    #testUrl = "http://ip.chinaz.com/getip.aspx"  
    proxies = []
    for page in range(16, 160):  
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
                t1 = time.time()  
                #proxies = {protocol : r'%s://%s:%s' % (protocol.lower(),ip, port)}
                #if int(port) == 80 or int(port) == 8080:
                try:  
                    #response = requests.get(testUrl, proxies=proxies, timeout=2)
                    #if response.status_code == 200:
                    #    proxies.append(r'%s://%s:%s' % (protocol.lower(),ip, port))
                    #else:
                    #    print "Failed proxy : " + str(proxies)
                    #timeused = time.time() - t1  
                    proxy = r"'%s':'%s://%s:%s'" %(protocol.lower(),protocol.lower(),ip, port)
                    if available_check(proxy):
                        print "ok ...."
                        proxies.append(r'%s://%s:%s' % (protocol.lower(),ip, port))
                    else:
                        print "Failed proxy : " + str(proxies)
                except Exception,e:  
                    continue  
    return proxies
print fetch_xici()
