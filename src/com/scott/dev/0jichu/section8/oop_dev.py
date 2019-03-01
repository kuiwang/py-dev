# -*- coding:utf-8 -*-

'''
类和对象
Created on 2018年10月25日

@author: user
'''

# 类:是对客观世界中事物的抽象；对象:是类实例化后的实体
# python使用class关键字定义一个类,类名的首字符一般大写。
# 当创建的类型不能用简单类型来表示时，则需要定义类，然后利用定义的类创建对象，
# 类把需要使用的变量和方法组合在一起，这种方式称为封装，定义类有两种方式:
# 继承自object
# class ClassName(object):...
# 不显式继承object
# class ClassName: ...

# 类创建
# 类的方法必需有一个self参数，但在调用时，可以不传递这个参数

# 对象创建
# 创建对象的过程称为实例化。当一个对象被创建后，包含3方面特性：对象的句柄、属性和方法
# 对象的句柄用于区分不同的对象，当对象被创建后，
# 该对象会获取一块存储空间，存储空间的地址即为对象的标识。
# 对象的属性和方法与类的成员变量和成员方法相对应。

# 属性和方法:
# 类由属性和方法组成。类的属性是对数据的封装，而类的方法则表示对象具有的行为。
# 类通常由函数(实例方法)和变量(类变量)组成
# python的构造函数、析构函数、私有属性或方法都通过名称约定区分的
# python还提供了一些有用的内置方法，简化了类的实现

# 类的属性：
# 类的属性一般分为私有属性和公有属性，python默认下所有属性都是公有的，
# 这样对类中属性的访问将没有任何限制，并且会被子类继承，也能从子类中进行访问
# python使用约定属性名称来达到数据封装的目的，
# 如果属性名字以两个下划线开始，就标识为私有属性，
# 反之没有双下划线开始的表示公有属性，类的方法同样使用这样的约定

# Python的属性分为实例属性和静态属性：实例属性是以self作为前缀的属性。
# __init__方法即python类的构造函数，
# 如果__init__方法中定义的遍历没有使用self作为前缀声明，则该变量只是普通的局部变量
# 静态变量可以被类直接调用，当创建新的实例化对象时，
# 静态变量并不会获得新的内存空间，而是使用类创建的内存空间
# 因此静态变量能被多个实例化对象共享,python中静态变量成为类变量，
# 类变量可以在该类的所有实例中被共享
# python类和对象都可以访问类属性，java只能类访问静态变量
# 类外部不能直接访问私有属性,如果把color属性改为私有属性__color,
# 执行print fruit.__color,python将不能识别属性__color
# 如何直接访问私有属性? 访问格式:
# instance._classname__attribute
# instance:表示实例化对象;classname表示类名;attribute:表示私有属性
'''
属性分为实例属性与类属性

方法分为普通方法，类方法，静态方法

 

一：属性：

　　尽量把需要用户传入的属性作为实例属性，而把同类都一样的属性作为类属性。实例属性在每创造一个实例时都会初始化一遍，不同的实例的实例属性可能不同，不同实例的类属性都相同。从而减少内存。

　　1：实例属性：

　　　　最好在__init__(self,...)中初始化

　　　　内部调用时都需要加上self.

　　　　外部调用时用instancename.propertyname

　　2:类属性：

　　　　在__init__()外初始化

　　　　在内部用classname.类属性名调用

　　　　外部既可以用classname.类属性名又可以用instancename.类属性名来调用

　　3：私有属性：

　　　　1）：单下划线_开头：只是告诉别人这是私有属性，外部依然可以访问更改

　　　　2）：双下划线__开头：外部不可通过instancename.propertyname来访问或者更改

　　　　　　实际将其转化为了_classname__propertyname

二：方法

　　1：普通类方法：

　　　　def fun_name(self,...):

　　　　　　pass

　　　　外部用实例调用

　　2：静态方法：@staticmethod            

　　　　　　不能访问实例属性！！！   参数不能传入self！！！

　　　　　　与类相关但是不依赖类与实例的方法！！

　　3:类方法：@classmethod

　　　　　　不能访问实例属性！！！   参数必须传入cls！！！

　　　　　　必须传入cls参数（即代表了此类对象-----区别------self代表实例对象），并且用此来调用类属性：cls.类属性名

　　*静态方法与类方法都可以通过类或者实例来调用。其两个的特点都是不能够调用实例属性
'''


class Fruit:
    # 类属性
    price = 0 

    # __init__:类的构造函数
    def __init__(self):
        # 实例属性
        self.color = 'red' 
        # 局部变量
        zone = 'China'

    def grow(self):
        print 'fruit growing now ...' 


# 访问私有属性:
class Frit1(object):

    def __init__(self):
        self.__color = 'red_color'  # 私有变量使用双下划线开始的名称


class Apple(Frit1):
    ''' this is doc '''
    pass


if __name__ == '__main__':
    print Fruit.price  # 使用类名调用类变量
    apple = Fruit()  # 实例化apple
    print apple.color  # 输出apple实例的颜色
    print apple.price 
    Fruit.price = Fruit.price + 10  # 类变量加10
    print 'apple\'s price:', str(apple.price)
    banana = Fruit()
    print 'banana\'s price:', str(banana.price)
    
    # 访问私有变量
    frit1 = Frit1()
    print frit1._Frit1__color
    app = Apple()
    # 输出基类组成的元组
    print 'Apple.__bases__:', Apple.__bases__
    
    # 输出属性组成的字典
    print 'app.__dict__:', app.__dict__
    
    # 输出类所在的模块名
    print 'app.__module__:', app.__module__
    
    # 输出doc文档
    print 'app.__doc__:', app.__doc__

