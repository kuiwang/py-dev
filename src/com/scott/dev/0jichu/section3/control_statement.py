# -*- coding:utf-8 -*-
'''
Created on 2018年10月15日

@author: user
'''


def conditional_judgment():
    if_condition()
    if_elif_else_condition()

# if条件语句
"""
if(condition):
    statement1
else:
    statement2
"""


def if_condition():
    a = input("a:")
    a = int(a)
    b = input("b:")
    b = int(b)
    if(a > b):
        print a, ">", b
    elif(a == b):
        print a, "=", b
    else:
        print a, '<', b

# if..elif..else条件语句
"""
if(condition1):
    statement1
elif(condition2):
    statement2
else:
    statement3
"""


def if_elif_else_condition():
    score = float(input("score:"))
    if (score >= 90 and score <= 100):
        print 'A'
    elif (score >= 80 and score < 90):
        print 'B'
    elif (score >= 60 and score < 80):
        print 'C'
    else:
        print 'D'


if __name__ == '__main__':
    conditional_judgment()
