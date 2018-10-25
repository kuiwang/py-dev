# -*- coding:utf-8 -*-
import os, sys, datetime, time
FILE_NAME = 'file_src.dat'
'''
文件属性信息
Created on 2018年10月25日

@author: user
'''

# 显示文件属性：路径、大小、创建日期、最后修改日期、最后访问时间
def show_file_properties(file_path):
    for root, dirs, files in os.walk(file_path, True):
        print '位置:', root
        print 'dirs:',dirs
        print 'files:',files
        for file_name in files:
            stat = os.stat(os.path.join(root, file_name))
            print 'type',type(stat),'stat:',stat
            info = '文件名:' + file_name + '\t'
            info = info + "大小:" + ("%d" % stat[-4]) + " "
            t = time.strftime('%Y-%m-%d %X', time.localtime(stat[-1]))
            info = info + "创建时间:" + t + " "
            t = time.strftime('%Y-%m-%d %X', time.localtime(stat[-2]))
            info = info + "最后修改时间:" + t + " "
            t = time.strftime("%Y-%m-%d %X", time.localtime(stat[-3]))
            info = info + "最后访问时间:" + t + " "
            print info


if __name__ == '__main__':
    show_file_properties(os.getcwd())
