#!/usr/bin/env python
#coding:utf-8
#Author: Sun Ning

from socket import *

ip_port=('127.0.0.1',8000)
back_log = 5
buffer_size = 1024

tcp_client = socket(AF_INET,SOCK_STREAM)
tcp_client.connect(ip_port)

while True:
    msg = raw_input('>>:') #发送空格到自己的发送缓存中
    tcp_client.send(msg.encode('utf-8'))
    print '客户端已经发送消息'
    data = tcp_client.recv(buffer_size) #收缓存为空则阻塞
    print '收到服务端发来消息:' + str(data.decode('utf-8'))

tcp_client.close()
