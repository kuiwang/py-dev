# -*- coding:utf-8 -*-
'''
Created on 2018年10月15日

@author: user
'''


def section2():
    operator_dev()
    relation_dev()
    logical_dev()


def operator_dev():
    print "1+1=", 1 + 1
    print "2-1=", 2 - 1
    print "2X3=", 2 * 3
    print "4/2=", 4 / 2
    print "1/2=", 1 / 2
    print "1/2=", 1.0 / 2.0
    print "3%2=", 3 % 2
    print "2**4=", 2 ** 4
    print "2**38=", 2 ** 38


def relation_dev():
    print "2>1:" , 2 > 1
    print "1<=2:" , 1 <= 2
    print "1==2:", 1 == 2
    print "1!=2:", 1 != 2


def logical_dev():
    print not True
    print  False and True
    print True and False
    print True or False


def get_sum(n):
    print '求和函数,参数n为下限'
    i = 0
    sum_res = 0
    while (i <= n):
        sum_res = sum_res + i
        i = i + 1
    return sum_res
    

if __name__ == '__main__':
    section2()
    print get_sum(100)
