# -*- coding:utf-8 -*-
'''
Created on 2018年10月13日

@author: root
'''
#python文件编译后生成.pyc后缀的文件,pyc文件是编译过的文件,无法使用文本编辑工具打开,pyc文件是平台无关的
#py文件直接运行后即可得到pyc文件，或者使用脚本生成该类型的文件
#以下将hello.py编译为hello.pyc
import py_compile as pycmpl
import py_compile
pycmpl.compile('hello.py')
py_compile.compile('hello.py')