#!/usr/bin/env python
#coding:utf-8
#Author: Sun Ning

import socket
phone=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
phone.connect(('127.0.0.1',8000))
phone.send("sun ning")
data = phone.recv(1024)
print u"收到服务端端发来消息：",data 
phone.close()
