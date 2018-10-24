# -*- coding:utf-8 -*-
'''
Created on 2018年10月21日

@author: root
'''

def func():
    print 'pack1.myModule1.func()'

if __name__ == '__main__':
    print 'myModule1作为主程序运行'
else:
    print 'myModule1被另一个模块调用'