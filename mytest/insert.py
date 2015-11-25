#!/usr/bin/python

L=range(9)

def insertSort(L):
    size = len(L)
    for i in range(1,size):
        fv = L[i]
        j = i
        while(j >= 1):
            if fv > L[j-1]:
                L[j] = L[j-1]
            else:
                break
            j = j-1
        L[j] = fv
        print L

insertSort(L)
