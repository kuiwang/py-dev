# -*- coding:utf8 -*-
'''
Created on 2018年10月19日

@author: user
'''


# tuple(元组)是Python内置的数据结构，由一系列元素组成,
# 所有元素包含在圆括号()内部，创建时可以不指定元素个数，相当于不定长的数组
# 一旦创建成功就不能修改元组的长度
# 创建格式:tuple =(ele1,ele2,ele3)
# 空元祖：tuple = ()
# 单元素元组：tuple=(1,)
def tuple_dev():
    print 'tuple_dev 函数开始...'
    tup1 = ("apple")  # 非元组
    print tup1[0]
    print len(tup1)
    print type(tup1)
    tup2 = ("apple",)
    print tup2[0]
    print type(tup2)


# 元组元素的值通过索引访问，索引是一对方括号[]中的数字,
# tuple[n]:标识访问元组中的第n个元素，n可以为正整数、0或负整数
# 负数索引或分片：最后一个元素索引为-1，倒数第二个为-2
# 分片(slice):是元组的一个子集，分片是从第一个索引到第二个索引（不包含第二个索引所指的元素）所指定
# 的所有元素，分片索引可以为正数或负数，索引间用冒号分隔，格式如下：tuple[m:n]
def tuple_access():
    print 'tuple_access 函数开始...'
    tuple = ("a", "s", "d", "f", "p", "t", "k")
    print tuple[1:4]  # 从第二个元素到第4个元素（下标为3），不包含第二个索引4指定的元素
    print tuple[1:-2]  # 从第二个元素到倒数第3个元素
    print tuple[3:]  # 从第4个元素到结尾
    print tuple[5:-2]
    tuple2 = ("a", "b", "c", "d")
    print tuple2[2:-2]
    f1 = ("app", "ban")
    f2 = ("grp", "peach")
    f3 = (f1, f2)
    print f3
    print ("f3[0][1]="), f3[0][1]
    print ("f3[1][1]="), f3[1][1]


def tuple_pack():
    print 'tuple_pack 函数开始...'
    # 打包
    tup = ("app", "ban", "grap", "peach")
    # 解包
    a, b, c, d = tup
    print a, b, c, d


# 遍历需要用到两个函数range()和len()
# len():计算元组内的元素个数
# range():返回一个由数字组成的列表
# range([start,],stop[,step]):
# start:列表开始的值，默认为0；
# stop:列表结束的值，不可缺少
# step:表示步长,每次递增或递减的值，默认为1
def tuple_visit():
    print 'tuple_visit 函数开始...'
    tup = (("apple", "banana"), ("grape", "orange"), ("watermelon",), ("fruit",))
    tup_len = len(tup)
    print "tuple length:", tup_len
    for i in range(tup_len):
        #print "outer i:", i
        for j in range(len(tup[i])):
            #print "innter j:", j
            print  "tup[%s][%s]=%s" %(i,j,tup[i][j])


if __name__ == '__main__':
    tuple_dev()
    tuple_access()
    tuple_pack()
    tuple_visit()
