# -*- coding:utf-8 -*-
'''
类的方法
Created on 2018年10月26日

@author: user
'''

# 类的方法：
# 类的方法也分为公有方法和私有方法,
# 私有方法不能被模块外的类或方法调用，私有方法也不能被外部的类或函数调用。
# 其他语言使用static声明静态方法
# Python使用函数staticmethod()或@staticmethod修饰器把普通的函数转换为静态方法。
# Python的静态方法并没有和类的示例进行静态绑定,要调用只需使用类名作为它的前缀即可


class Fruit(object):
    price = 0  # 类变量
    
    def __init__(self):
        self.__color = 'red'  # 定义私有变量
    
    def getColor(self):
        print self.__color  # 返回私有变量
    
    # 使用@staticmethod修饰器定义静态方法
    @staticmethod
    def getPrice():
        print Fruit.price
    
    # 定义私有函数
    
    def __getPrice():
        Fruit.price = Fruit.price + 10
        print Fruit.price
    
    count = staticmethod(__getPrice)

    
if __name__ == '__main__':
    apple = Fruit()  # 实例化apple
    apple.getColor()  # 使用实例调用静态方法
    Fruit.count()
    banana = Fruit()
    Fruit.count()
    Fruit.getPrice()
