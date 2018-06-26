#!/usr/bin/env python
#coding:utf-8
import multiprocessing
import time
import re


#aaa="""'b\'<style type="text/css">\\r\\n</style>\\r\\n</marquee>\\r\\n<meta http-equiv="Content-Type" content="text/html; charset=GBK" />\\r\\n<title>\\xb0\\xb2\\xd0\\xa1\\xc4\\xaa\\xcc\\xe1\\xca\\xbe\\xa3\\xba\\xc4\\xe4\\xc3\\xfb\\xcc\\xe1\\xc8\\xa1\\xb3\\xc9\\xb9\\xa6</title>\\r\\n<script type="text/javascript">\\r\\nvar sogou_ad_id=768629;\\r\\nvar sogou_ad_height=90;\\r\\nvar sogou_ad_width=960;\\r\\n</script>\\r\\n<script>\\r\\nvar mediav_ad_pub = \\\'47zFt2_1221523\\\';\\r\\nvar mediav_ad_width = \\\'640\\\';\\r\\nvar mediav_ad_height = \\\'60\\\';\\r\\n</script>\\r\\n<script type="text/javascript" language="javascript" charset="utf-8"  src="//static.mediav.com/js/mvf_g2.js"></script>\\r\\n\\r\\n\\r\\n  \\t163.125.158.122:8888<br />\\r\\n\\t\\t218.255.65.22:8118<br />\\r\\n\\t\\t119.136.198.22:8118<br />\\r\\n\\t\\t114.251.228.124:3128<br />\\r\\n\\t\\t118.250.86.62:8118<br />\\r\\n\\t\\t122.13.15.10:80<br />\\r\\n\\t\\t59.110.139.20:8118<br />\\r\\n\\t\\t171.39.43.73:8123<br />\\r\\n\\t\\t113.78.65.76:9797<br />\\r\\n\\t\\t1.65.218.170:8118<br />\\r\\n\\t</div>\\r\\n<script type="text/javascript">\\r\\n$(function(){\\r\\n$(\\\'#adarea\\\').slideDown(500);\\r\\n$(\\\'#adclose\\\').click(function(){\\r\\n$(\\\'#adarea\\\').slideUp(500);\\r\\n});\\r\\n});\\r\\n</script>\\r\\n<script type="text/javascript" src="http://www.66ip.cn/ggg/jquery.min.js"></script>\\r\\n<div id="adarea"onclick=location.href=\\\'http://www.ip3366.net/fetch/\\\' style="cursor: pointer;display: none;position: fixed;right:15px;bottom:15px;width: 285px;height: 250px;background: url(http://www.66ip.cn/ggg/fkgg.png) no-repeat;">\\r\\n<div id="adclose" style="cursor: pointer; position: absolute;  top: 0px;  right: 0px;  display: block;  width: 20px;  height: 20px;font-family: cursive;background: url(http://www.66ip.cn/ggg/close.png) no-repeat;" title="\\xb5\\xe3\\xbb\\xf7\\xb9\\xd8\\xb1\\xd5"> </div>\\r\\n</div>\\r\\n<script type="text/javascript">\\r\\n$(function(){\\r\\n$(\\\'#adarea\\\').slideDown(500);\\r\\n$(\\\'#adclose\\\').click(function(){\\r\\n$(\\\'#adarea\\\').slideUp(500);\\r\\n});\\r\\n});\\r\\n</script>\'' """
#
#p = r'(?:((?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5]))\D+?(6[0-5]{2}[0-3][0-5]|[1-5]\d{4}|[1-9]\d{1,3}|[0-9]))'
#print re.findall(p,aaa)
#print re.findall(r'\d*\.\d*\.\d*\.\d*:\d*',aaa)

f=open("aaa",'r')
ret=f.readlines()
r=r" (.*).sina.com.cn"
c=re.compile(r)
for l in ret:
    t=re.findall(c,l)
    if t:
        print t[0]
