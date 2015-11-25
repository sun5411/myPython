#!/usr/bin/python
import pdb

def is_sushu(num):
    res = True
    for x in range(2,num/2+1):
        if num%x == 0:
            res = False
            return res
    return res

print ([x for x in range(100) if is_sushu(x)])
