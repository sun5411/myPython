#!/usr/bin/env python
#coding:utf-8
#Author: Sun Ning

import socket

phone=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
phone.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
phone.bind(('127.0.0.1',8000))
phone.listen(5)
print('---------------->')
conn,addr=phone.accept()

msg=conn.recv(1024)
print "客户端发来消息：",msg
conn.send(msg.upper())

conn.close()
phone.close()
