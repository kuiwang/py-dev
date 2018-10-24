# -*- coding:utf-8 -*-
'''
Created on 2018年10月20日

@author: root
'''

#apply():
#python3移除了apply()函数调用可变参数列表的函数的功能只能使用在列表前加*来实现

#filter():
#可以对某个序列做过滤处理，判断自定义函数的参数返回的结果是否为真来过滤，并一次性返回处理结果,声明如下：
#class filter(object)
#    filter(function or None,iterable ) --> filter object

def func(x):
    if x>0:
        return x
    else:
        return 0

def test_filter():
    print range(-9,10)
    #使用range生成待处理的列表，然后把该列表的值一次传给func，func返回结果给filter
    #最后将结果yield成一个iterable对象返回，可以进行遍历
    print (filter(func, range(-9,10)))
    print 'use list'
    print list(filter(func,range(-9,10)))

#reduce():
#对序列中元素的连续操作可以通过循环来处理,reduce()也可实现连续处理的功能
#reduce()声明如下:
#reduce(func,sequence[,initial]) -> value
#func:自定义函数，在func中实现对参数sequence的连续操作
#sequence:待处理的序列
#initial:若initial不为空，则initial的值将首次传入func进行计算，如sequence为空，则对inital进行处理
#reduce()的返回值是func计算后的结果

def sum1(x,y):
    return x+y

def test_reduce():
    print 'test reduce()函数'
    print reduce(sum1, range(0,10))
    print reduce(sum1, range(0,10),10)
    print reduce(sum1,range(0,0),100)

#map():
#map()对tuple元组进行解包操作，调用时设置map()的第一个参数为None
#map()可以对多个序列的每个元素都执行相同的操作，并返回一个map对象，声明如下：
#class map(object):
#    map(func,*iterable) --> map object
#func:自定义函数，实现对序列的每个元素的操作
#iterables:待处理的序列，参数iterables的个数可以是多个
#map()的返回值是对序列元素处理后的列表

def power_2(x):
    return x**x
def power_xy(x,y):
    return x**y

def test_map():
    print 'test map() 函数开始 '
    print map(power_2,range(1,5))
    print list(map(power_2,range(1,5)))
    print map(power_xy,range(1,5),range(5,1,-1))
    print list(map(power_xy,range(1,5),range(5,1,-1)))

#内置函数
#abs(x):返回x的绝对值
#bool([x]):把一个值或表达式转换为bool类型
#delattr(obj,name):等价于del obj.name
#eval(s[,globals[,locals]]):计算表达式的值
#float(x):把整数或字符串转换为float类型
#hash(object):返回一个对象的hash值
#id(x):返回一个对象的标识
#input([prompt]):接受控制台的输入，并把输入的值转换为数字
#int(x):把整数或字符串转换为int类型
#len(obj):对象包含的元素个数
#range([start,],end[,step]):生成一个列表并返回
#reduce(func,sequence[,initial]):对序列的值进行累计计算
#round(x,n=0):四舍五入函数
#set([iterable]):返回一个set集合
#sorted(iterable[,cmp[,key[,reverse]]]):返回一个排序后的列表
#sum(iterable[,start=0]):返回一个序列的和
#type(obj):返回一个对象的类型
#zip(iter1[,iter2[...]]):把n个序列作为列表的元素返回
if __name__ =='__main__':
    test_filter()
    test_reduce()
    test_map()