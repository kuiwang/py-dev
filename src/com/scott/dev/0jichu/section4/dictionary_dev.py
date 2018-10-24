# -*- coding:utf8 -*-
'''
Created on 2018年10月19日

@author: user
'''

# dictionary(字典)是Python内置的数据结构，字典由"键-值"对组成的集合，"键-值"对之间以逗号“，”分隔包含在
# 花括号之中，字典中的“值”可以通过“键”来引用
# 创建字典和使用：
# dict={k1:v1,k2:v2,k3:v3}


def dict_use():
    print "dict_use 开始"
    dict = {"a":"apple", "b":"banana", "g":"grape", "o":"orange"}
    print dict
    print dict["a"]

# 元素和列表访问是通过数字索引来获取对应值
# 字典则是通过key值来获取相应的value值，访问格式如下：v = dict[k]
# 字典添加删除修改非常简单，添加修改只需要一条赋值语句：dict["x"]="v"
# 如果x不在dict的key列表中，dict会添加一条新的映射(x:v),如果存在x，则修改x的value为v
# 字典没有remove操作，字典元素删除可以调用del实现
# 字典调用pop弹出列表中一个元素，D.pop(k[,d])->v:
# 如果字典中存在索引k，则v等于D[k],如果没有索引k，则返回d
# 清除字典中的所有内容，可以调用字典的clear()


def dict_access():
    print 'dictionary 访问开始'
    dict = {"a":"apple", "b":"banana", "g":"grape", "o":"orange"}
    print dict
    dict["w"] = "water"
    print dict
    del(dict["a"])
    print dict
    dict["g"] = "grp_update"
    print dict
    dict.pop("b")
    print dict
    dict.clear()
    print dict


# 字典遍历
def dict_visit():
    print 'dictionary 字典遍历开始'
    dict = {"a":"apple", "b":"banana", "g":"grape", "o":"orange"}
    for k in dict:
        print "dict[%s] = %s" % (k , dict[k])
    #字典items使用
    print dict.items()
    print "使用items()来循环遍历"
    for (k,v) in dict.items():
        print "dict[%s]=%s" %(k,v)
    #字典keys()方法
    print dict.keys()
    #字典values()方法
    print dict.values()

#将已有字典添加到现有字典
def addDictToExistDict():
    d={"k1":'v1',"k2":"v2"}
    e={"k3":"v3","k4":"v4"}
    d.update(e)
    print d
    d1={"k1":'v1',"k2":"v2"}
    e1={"k3":"v3","k4":"v4"}
    for k in e1:
        d1[k]=e1[k]
    print d1

#全局字典：sys.modules模块
#sys.modules是一个全局字典，是python启动后就夹在在内存中的，每当导入新的模块时，sys.modules都将记录这些模块，
#sys.modules对加载模块起到缓存的作用，第二次再导入时，python会直接诶从字典中查找，从而加快程序运行速度
#sys.modules拥有字典的一切方法，可以通过这些方法查看当前环境加载了那些模块
def sys_modules_use():
    print 'sys_modules_use 函数开始'
    import sys
    sys_module_dict=sys.modules
    #print sys_module_dict
    for k in sys_module_dict:
        print '%s=%s' %(k,sys_module_dict[k])
    print sys.modules.keys()
    print sys.modules.values()
    print sys.modules.items()
    print sys.modules['os']

if __name__ == '__main__':
    dict_use()
    dict_access()
    dict_visit()
    addDictToExistDict()
    sys_modules_use()
