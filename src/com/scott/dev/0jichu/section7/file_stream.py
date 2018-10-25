# -*- coding:utf-8 -*-
import os, sys, datetime, time
FILE_NAME = 'file_src.dat'
'''
文件和流对象
Created on 2018年10月25日

@author: user
'''
# 读写数据方式有多种:文件读写、数据库读写、为了有效表示数据读写,把文件、外设、网络连接等数据传输抽象的标识为流
# 数据传输像流水一样,从一个容器流入另一个容器中

# python把文件处理和流关联起来，流对象实现了File类的所有方法
# sys模块提供了三种基本流对象：stdin、stdout、stderr
# stdin：


def test_stdin():
    print 'test_stdin function'
    sys.stdin = open(FILE_NAME, 'r')
    for line in sys.stdin.readlines():
        print line
    sys.stdin.close()


def test_stdout():
    print 'test_stdout function'
    sys.stdout = open(FILE_NAME, 'a')
    print 'the end'
    # sys.stdout.close()


def test_stderr():
    print 'test_stderr function'
    sys.stderr = open('error.log', 'a')
    f = open(FILE_NAME, 'r')
    t = time.strftime('%Y-%m-%d %X', time.localtime())
    context = f.read()
    if context:
        sys.stderr.write(t + ' \t' + context)
    else:
        raise Exception , t + "异常信息"


if __name__ == '__main__':
    test_stdin()
    test_stdout()
    test_stderr()
