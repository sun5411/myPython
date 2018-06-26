#coding:utf-8
import urllib2
url="http://blog.csdn.net/happydeer"
my_headers={
          "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
          "GET":url,
          "Host": "blog.csdn.net",
          "Referer":"http://blog.csdn.net/"
        }
req = urllib2.Request(url,headers=my_headers)

#req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36")
#req.add_header("GET",url)
#req.add_header("Host", "blog.csdn.net")
#req.add_header("Referer","http://blog.csdn.net/")

html = urllib2.urlopen(req)
print html.read()
