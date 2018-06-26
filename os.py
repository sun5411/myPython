#!/usr/bin/env python
#coding:utf-8

import os

def print_dir_contents(path):
    for child in os.listdir(path):
        nChild = os.path.join(path,child)
        if os.path.isdir(nChild):
            print_dir_contents(nChild)
        else:
            print nChild


print_dir_contents("./")
