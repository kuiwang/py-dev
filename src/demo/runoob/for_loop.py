#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding: utf-8
import os
import sys


reload(os)

def forloop():
    for i in range(1,5):
        for j in range(1,6):
            for k in range(1,7):
                if ((i!=j) and (i!=k) and (j!=k)):
                    #print %i+"|"+%d+"|"+%d) % (i,j,k)
                    print '结果�?:%d,%d,%d' % (i,j,k)
    d=[]
    for a in range(1,5):
        for b in range(1,5):
            for c in range(1,5):
                if (a!=b) and (a!=c) and (c!=b):
                    d.append([a,b,c])
    print "总数量：", len(d)
    print d
    

if __name__ == '__main__':
    forloop()