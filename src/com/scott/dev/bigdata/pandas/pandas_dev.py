# -*- coding:utf-8 -*-
'''
Created on 2018年10月19日

@author: root
'''
import pandas as pd
from pandas import Series, DataFrame


def series_dev():
    print('series_dev start')
    print('使用一维数组生成Series')
    x = Series([1, 3, 5, 7])
    print(x)
    print("x.values in below:")
    print(x.values)
    
    print('x.index in below:')
    # 默认标签为0到3的序号
    print (x.index)  # RangeIndex(start=0, stop=4, step=1) 
    
    print ('指定Series的index')  # 可将index理解为行索引
    x = Series([1, 2, 3, 4], index=['a', 'b', 'd', 'c'])
    print (x)
    
    print (x.index)  # Index([u'a', u'b', u'd', u'c'], dtype='object')
    print (x['a'])  # 通过行索引来取得元素值：1
    x['d'] = 6  # 通过行索引来赋值
    print (x[['c', 'a', 'd']])  # 类似于numpy的花式索引
    print('x in below:')
    print(x)
    print ("x[x > 1] in below:")  # 类似于numpy的布尔索引
    print (x[x > 1])  # 类似于numpy的布尔索引
    
    print ('b' in x)  # 类似于字典的使用：是否存在该索引：True
    print ('e' in x)  # False
    
    print ('使用字典来生成Series')
    data = {'a':1, 'b':2, 'd':3, 'c':4}
    x = Series(data)
    print (x)
    
    print ('使用字典生成Series,并指定额外的index，不匹配的索引部分数据为NaN。')
    exindex = ['a', 'b', 'c', 'e']
    y = Series(data, index=exindex)  # 类似替换索引
    print(y)
    
    print ('Series相加，相同行索引相加，不同行索引则数值为NaN')
    print (x + y)
    
    print ('指定Series/索引的名字')
    y.name = 'weight of letters'
    y.index.name = 'letter'
    print (y)
    
    print ('替换index')
    y.index = ['a', 'b', 'c', 'f']
    print (y)  # 不匹配的索引部分数据为NaN

    
def dataframe_dev():
    print('dataframe_dev start')
    print ('使用字典生成DataFrame，key为列名字。')
    data = {'state':['ok', 'ok', 'good', 'bad'],
            'year':[2000, 2001, 2002, 2003],
            'pop':[3.7, 3.6, 2.4, 0.9]}
    print (DataFrame(data))  # 行索引index默认为0，1，2，3 
   
    # 指定列索引columns,不匹配的列为NaN
    print (DataFrame(data, columns=['year', 'state', 'pop', 'debt'])) 
    
    print ('指定行索引index')
    x = DataFrame(data, columns=['year', 'state', 'pop', 'debt'], index=['one', 'two', 'three', 'four'])
    print (x)
    
    print ('DataFrame元素的索引与修改')
    print (x['state'])  # 返回一个名为state的Series
    print (x.state)  # 可直接用.进行列索引
    print (x.ix['three'])  # 用.ix[]来区分[]进行行索引
    
    x['debt'] = 16.5  # 修改一整列数据
    print(x)
    
    import numpy
    x.debt = numpy.arange(4)  # 用numpy数组修改元素
    print (x)
    
    print ('用Series修改元素，没有指定的默认数据用NaN')
    val = Series([-1.2, -1.5, -1.7, 0], index=['one', 'two', 'five', 'six']) 
    x.debt = val  # DataFrame的行索引不变
    print (x)
    
    print ('给DataFrame添加新列')
    x['gain'] = (x.debt > 0)  # 如果debt大于0为True
    print (x)

    
def pandas_use():
    # series_dev()
    dataframe_dev()


if __name__ == '__main__':
    pandas_use()
