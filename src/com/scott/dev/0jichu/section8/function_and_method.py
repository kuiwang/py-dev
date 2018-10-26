# -*- coding:utf-8 -*-
'''
方法和函数的区别
Created on 2018年10月26日

@author: user
'''

'''
Python: 函数与方法的区别 以及 Bound Method 和 Unbound Method:
https://segmentfault.com/a/1190000009157792
'''


def fun():
    print '这是一个函数'
    pass


class MyClass(object):

    def fun1(self):
        return 'normal'

    @staticmethod
    def fun2():
        return 'static method'
    
    @staticmethod
    def fun4(self):
        self.color = 'red'
        return 'fun4 static method'

    @classmethod
    def fun3(cls):
        return 'class method'


if __name__ == '__main__':
    print fun, ',', type(fun)
    print '-' * 80
    print MyClass.fun1, ',', type(MyClass.fun1)
    print MyClass.fun2, ',', type(MyClass.fun2)
    print MyClass.fun3, ',', type(MyClass.fun3)
    print MyClass.fun4, ',', type(MyClass.fun4)
    
    print '-' * 80
    app = MyClass()
    print app.fun1, ',', type(app.fun1)
    print app.fun2, ',', type(app.fun2)
    print app.fun3, ',', type(app.fun3)
    print app.fun4, ',', type(app.fun4)
