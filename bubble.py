#!/usr/bin/env python

def bubble(x,n):
    for i in range(n):
        for j in range(n-1):
            if x[j]<x[j+1]:
                t=x[j]
                x[j]=x[j+1]
                x[j+1]=t
    print x


x=[1,2,4,56,7,9,88,72]
bubble(x,len(x))
