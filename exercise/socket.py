#!/usr/bin/env python
#coding:utf-8

import _socket as socket

def handle_request(client):
	buf = client.recv(1024)
	client.send("HTTP/1.1 200 0k\r\n\r\n")
	client.send("Hello , Sun Ning!!!")

def main():
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.bind(('localhost',8088))
	sock.listen(5)

	while True:
		conn,address = sock.accept()
		handle_request(conn)
		print address
		conn.close

main()
