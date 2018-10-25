# -*- coding:utf-8 -*-
import os

'''
目录操作
Created on 2018年10月25日

@author: user
'''
#os模块提供了针对目录进行操作的函数
#mkdir(path[,mode=0777]): 创建path指定的一个目录
#makedirs(name,mode=5111): 创建多级目录,name标识path1/path2/...
#rmdir(path): 删除path指定的目录
#removedirs(path): 删除path指定的多级目录
#listdir(path): 返回path指定目录下所有的文件名
#getcwd(): 返回当前的工作目录
#chdir(path): 改变当前目录为path指定的目录
#walk(top,topdown=True;onerror=None): 遍历目录树

def test_rmdir_mkdir():
    import os
    os.mkdir('hi')
    print '创建单级目录hi'
    os.rmdir('hi')
    print '删除hi目录'
    os.makedirs('hi/hi1')
    print '创建多级目录hi/hi1/'
    os.removedirs('hi/hi1')
    print '删除多级目录hi/hi1/'

#遍历目录
#使用普通方法遍历目录
def traverse_dir_normal(dir_path):
    lst = os.listdir(dir_path)
    for p in lst:
        path_name = os.path.join(dir_path,p)
        if not os.path.isfile(path_name):
            traverse_dir_normal(path_name)
        else:
            print 'path:',path_name

#使用walk()方法遍历目录
def travese_dir_walk(dir_path):
    print 'travese_dir_walk function'
    walk_res = os.walk(dir_path)
    print 'walk res:',walk_res
    print 'type of walk_res:',type(walk_res)
    for root,dirs,files in os.walk(dir_path):
        for file_path in files:
            print 'join_path:',os.path.join(root,file_path)

if __name__ == '__main__':
    my_dir_path ='D:\programs\pyclipse\mypy\src\com\scott\dev'
    test_rmdir_mkdir()
    #traverse_dir_normal(my_dir_path.replace('\\', os.path.sep))
    travese_dir_walk(my_dir_path.replace('\\',os.path.sep))