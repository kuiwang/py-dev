# -*- coding:utf-8 -*-

#类名首字母采用大写
#对象名采用小写
#类的属性和方法名以对象作为前缀
#类的私有变量和私有方法以两个下划线作为前缀

class Student(object):
    __name=''
    def __init__(self ,n):
        self.__name = n
    def getName(self):
        return self.__name

if __name__ == "__main__":
    s = Student("paul")
    n = s.getName()
    print ("student name is:%s") % n