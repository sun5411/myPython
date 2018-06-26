#!/usr/bin/env python
#coding:utf-8
#Author: Sun Ning

from socket import *

ip_port=('127.0.0.1',8000)
back_log = 5
buffer_size = 1024

tcp_server = socket(AF_INET,SOCK_STREAM)
tcp_server.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
tcp_server.bind(ip_port)
tcp_server.listen(back_log)

print '服务端开始运行...'
conn,addr = tcp_server.accept() #服务器阻塞
print '双向链接是' + str(conn)
print '客户端地址' + str(addr)

while True:
    data = conn.recv(buffer_size) #收缓存为空，则阻塞
    print '接收到客户端发来消息：' + str(data.decode('utf-8'))
    conn.send(data.upper())

conn.close()
tcp_server.close()
