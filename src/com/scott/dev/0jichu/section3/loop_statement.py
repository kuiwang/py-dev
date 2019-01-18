# -*- coding:utf-8 -*-
'''
Created on 2018年10月15日

@author: user
'''


def loop_statement():
    while_statment_loop()
    for_statement_loop()


# while循环
# while(condition):
#    ..
# else:
#    ...
def while_statment_loop():
    # number = input('输入几个数字,以逗号分隔:\n').split(",")
    # print number
    number = [1, 2, 3, 4, 5]
    x = 0
    while x < len(number):
        print number[x]
        x = x + 1


# for循环
# 集合可以是元组、列表、字典等数据结构
# for 变量 in 集合:
#    ...
# else:
#    ...
def for_statement_loop():
    for x in range(-3, 5):
        if(x > 0):
            print '正数:', x
        elif x == 0:
            print '零:', x
        else:
            print '负数:', x
    else:
        print 'loop循环结束'


if __name__ == "__main__":
    loop_statement()
