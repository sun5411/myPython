#!/usr/bin/python

L=range(19)

def selectSort(L):
    size = len(L)
    for i in range(0,size):
        max = L[i]
        for j in range(i+1,size):
            if max < L[j]:
                max = L[j]
                index = j
        L[i],L[index] = max,L[i]

    print L

selectSort(L)
