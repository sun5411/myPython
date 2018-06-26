#!/usr/bin/env  python

#coding:utf-8

import os
def list_files(path):
	for child in os.listdir(path):
		childPath = os.path.join(path,child)
		if os.path.isdir(childPath):
			list_files(childPath)
		else:
			print childPath

list_files('./')
