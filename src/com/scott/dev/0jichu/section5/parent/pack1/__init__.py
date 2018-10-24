# -*- coding:utf-8 -*-

#自定义包:
#包就是一个至少包含__init__.py文件的文件夹
#以下代码初始化pack包，当pack包被其他模块调用时，将输出"pack初始化"

#__init__.py也可用于提供当前包的模块列表，例如添加如下代码：
#__all__=["myModule1"]
#__all__:记录了当前pack包所包含的模块，【】内的内容是模块名的列表，用逗号分隔
if __name__ =='__main__':
    print '作为主程序运行'
else:
    print 'pack1初始化'