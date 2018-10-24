# -*- coding:utf8 -*-
'''
Created on 2018年10月19日

@author: user
'''

# 序列
def list_sort_asc():
    lst=[2,5,3,8,10,1]
    lst.sort(cmp=None, key=None, reverse=False) 
    for i in range(len(lst)):
        print lst[i]

def string_reverse():
    s="123456"
    print s[-1:0]

if __name__ == '__main__':
    list_sort_asc()
