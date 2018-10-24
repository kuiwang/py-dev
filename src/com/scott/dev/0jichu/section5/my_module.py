# -*- coding:utf-8 -*-
'''
my_module Created on 2018年10月20日

@author: root
'''
count=1

def func():
    global count
    count = count + 1
    return count

if __name__ == '__main__':
    print 'my_module作为主程序在运行'
else:
    print 'my_module被另一个模块调用'
    print 'doc not in main ',__doc__