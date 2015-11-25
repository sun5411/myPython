#!/usr/bin/python

L=range(9)

def bubbleSort(L):
    size=len(L)
    for i in range(size-1,-1,-1):
        for j in range(i):
            if L[j] < L[j+1]:
                L[j],L[j+1] = L[j+1],L[j]
    print L

bubbleSort(L)
