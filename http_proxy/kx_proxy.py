#!/usr/bin/env python
#coding:utf-8
import requests
from lxml import etree

def get_html(url):
    ''' 
    return: lxml对象
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    html = etree.HTML(r.text)
    return html

def fetch_kxdaili():
    '''
    抓取kaixin代理
    '''
    base_url = 'http://www.kxdaili.com/dailiip/1/{}.html#ip'
    try:
        proxies = []
        for page in range(1, 9): 
            url = base_url.format(page)
            html = get_html(url)
            responses = html.xpath('//tr/td[5]/text()')
            responses = [i.split(' ')[0] for i in responses]
            tmp = [i.text for i in html.xpath('//tbody/tr/td')]
            res = [i for i in tmp if i and (i.isdigit() or ''.join(i.split('.')).isdigit())]
            ip = [i for l, i in enumerate(res) if l % 2 == 0]
            port = [i for l, i in enumerate(res) if l % 2 == 1]
            for l, r in zip(ip, port):
                index = ip.index(l)
                if float(responses[index]) < 0.5 :
                    if 8080 == int(r) or 80 == int(r):
                    	proxies.append('{}:{}'.format(l, r)) 
                    	print '{}:{}'.format(l, r) , responses[index]
    except Exception as e:
        print 'error'
        proxies = []
    if not proxies:
        print ' fail to fetch kxdaili'
    return proxies


def main():
    proxy = fetch_kxdaili()
    print proxy


if __name__ == "__main__":
    main()
