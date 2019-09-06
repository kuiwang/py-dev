# -*- coding:utf-8 -*-

'''
Created on 2019年8月26日

@author: user
'''
import os,sys,time,random,datetime
from time import strftime

def print_pkq(i):
    i_hex = hex(i)
    s = "%064x" % i
    print(s)
    i = i + 1

    
if __name__ == '__main__':
    '''
    i = 0x0000000000000000000000000000000000000000000000000000000000129f10
    j = 0x129f10
    print(i)
    print(j)
    i_hex = "%064x" % i
    j_hex = "%064x" % j
    print(i_hex)
    print(j_hex)
    '''
    '''
     Commonly used format codes:
    
    %Y  Year with century as a decimal number.
    %m  Month as a decimal number [01,12].
    %d  Day of the month as a decimal number [01,31].
    %H  Hour (24-hour clock) as a decimal number [00,23].
    %M  Minute as a decimal number [00,59].
    %S  Second as a decimal number [00,61].
    %z  Time zone offset from UTC.
    %a  Locale's abbreviated weekday name.
    %A  Locale's full weekday name.
    %b  Locale's abbreviated month name.
    %B  Locale's full month name.
    %c  Locale's appropriate date and time representation.
    %I  Hour (12-hour clock) as a decimal number [01,12].
    %p  Locale's equivalent of either AM or PM.
    
    '''
    ts =  time.strftime('%Y-%m-%d %H:%M:%S')
    print(ts)