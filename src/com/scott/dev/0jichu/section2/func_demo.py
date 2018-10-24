# -*- coding:utf-8 -*-
'''
Created on 2018年10月14日

@author: root
'''

# 函数名通常采用小写，并用下划线或首字母大写增加名称的可读性
# 导入的函数以模块名作为前缀
# randrange:
# randrange(start,stop[,step])
# start: 生成随机数所在范围的开始数字
# stop:生成随机数所在范围的结束数字，但不包含数字stop
# step:从start开始往后的步数，生成的随机数位于[start,stop-]，取值等于start+step
# ex:randrange(1,9,2):取值在1、3、5、7之间

import random


def compareNum(m, n):
    if(m > n):
        return 1
    elif(m == n):
        return 0
    else:
        return -1


if __name__ == '__main__':
    m = random.randrange(1, 9)
    n = random.randrange(1, 9)
    print ("m=", m)
    print ('n=', n)
    print('compare %i and %i is: %i') % (m, n, compareNum(m, n))
