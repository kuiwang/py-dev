# -*- coding:utf-8 -*-
'''
Created on 2018年10月14日

@author: root
'''

# 模块是累或函数的集合，用于处理一类问题
# 使用import或from..import导入三方模块

import sys


def sys_module_info():
    print "sys.path = ", sys.path
    print "sys.api_version=", sys.api_version
    print "sys.argv = ", sys.argv
    print "sys.builtin_module_names = ", sys.builtin_module_names
    print "sys.byteorder = ", sys.byteorder
    # print sys.copyright
    print sys.callstats()


def var_info():
    x = 1
    print "id(x)=", id(x)
    x = 2
    print "id(x)=", id(x)


if __name__ == '__main__':
    # sys_module_info()
    var_info()
