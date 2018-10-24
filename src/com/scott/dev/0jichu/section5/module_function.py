# -*- coding:utf-8 -*-

'''
module_function Created on 2018年10月20日

@author: root
'''
#python程序由包(package),模块(module)和函数组成，
#模块是处理某一类问题的集合，模块由函数和类组成
from compiler.syntax import check

#包：是由一系列模块组成的集合，自带工具包位于和模块位于python安装目录的Lib子目录中
#ex:Lib目录下有xml文件夹，xml文件夹就是一个包，完成xml应用开发
#xml包下有几个子包,文件__init__.py是xml包的注册文件，如果没有该文件，python将不能识别xml包
#包至少包含一个__init__.py文件，文件可以为空，用于标识文件夹是一个包

#模块：把一组相关函数和代码组织到一个文件中，一个文件即一个模块，
#创建一个module.py文件，就定义了一个名为module的模块
#python导入一个模块时，python首先查找当前路径，然后查找lib目录、site-packages目录和环境变量
#PYTHONPATH设置的目录，可以通过sys.path搜索模块的查找路径

#模块属性:
#模块有一些内置属性，用于完成特定任务，如：__name__、__doc__
#__name__:用于判断当前模块是否为程序的入口，如当前程序正在被使用,__name__的值为__main__
#通常为每一个模块加一个条件语句，用于单独测试该模块的功能
#ex：创建一个模块myModule:
# if __name__ == '__main__':
#    print 'myModule作为主程序运行'
# else:
#    print 'myModule被另一个模块调用'

def check_count():
    print 'check count function'
    import my_module
    print __doc__
    print 'count = ',my_module.func()
    my_module.count = 10
    print 'now count = ',my_module.count
    import my_module
    print 'my count = ',my_module.func()

if __name__ == '__main__':
    check_count()