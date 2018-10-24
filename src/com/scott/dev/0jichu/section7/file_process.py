# -*- coding:utf-8 -*-
'''
Created on 2018年10月13日

@author: root
'''
# 文件处理一般包含如下3步骤:
# 1、创建并打开文件,使用file函数返回一个file对象
# 2、调用file对象的read、write等方法处理文件
# 3、调用close关闭文件，释放file对象占用的资源
from __builtin__ import file

# 文件模式:
# r: 以只读方式打开文件
# r+: 以为读写方式打开文件
# w: 以写入方式打开文件，先删除文件原有内容，再重新写入新内容，如果文件不存在则创建一个新文件
# w: 以读写方式打开文件，先删除文件原有内容，再重新写入新内容，如果文件不存在则创建一个新文件
# a: 以写入方式打开文件，在文件末尾追加新内容，如果文件不存在，则创建一个新文件
# a: 以读写方式打开文件，在文件末尾追加新内容，如果文件不存在，则创建一个新文件
# b: 以二进制模式打开文件，可与r、w、a、+结合使用，图片和视频文件必须使用'b'模式读写
# U: 支持所有的换行符号。'\r','\n','\r\n'都表示换行

# file类常用属性和方法:
# closed: 判断文件是否关闭，如果被关闭返回True
# encoding: 显示文件的编码类型
# mode: 显示文件的打开模式
# name: 显示文件的名称
# newlines: 文件使用的换行模式
# file(name[,mode[,buffering]]): 以mode指定的方式打开文件，如果文件不存在则先创建文件再打开文件
# buffering:表示缓存模式,0:不缓存;1:表示行缓存;如果大院1则表示缓冲区的大小
# flush(): 把缓存区的内容写入磁盘
# close(): 关闭文件
# read([size]): 从文件中读取size个字节的内容作为字符串返回
# readline([size]):从文件中读取一行作为字符串返回，如指定size标识每行每次读取的字节数，依然要读完整行的内容
# readlines([size]): 把文件的每行存储在列表中返回，如果指定size，标识每次读取的字节数
# seek(offset[,whence]): 把文件指针移动到一个新位置,offset表示相对于whence的位置;如无whence，则offset表示相对文件开头的位置
# whence用于设置相对位置的起点. #whence=0:表示从文件开头开始计算，1表示从当前位置开始计算，2:表示从文件末尾开始计算，
# tell(): 返回文件指针当前的位置
# next(): 返回下一行的内容，并将文件指针移到下一行
# truncate([size]): 删除size个字节的内容
# write(str): 把字符串str的内容写入文件
# writelines(seq_of_strings): 把字符串序列写入文件

# 文件删除:需要使用os和os.path模块，os模块提供了对系统环境、文件和目录等OS级的接口函数

# os模块常用文件处理函数: 
# access(path,mode): 按照mode指定的权限访问文件
# chmod(path,mode): 改变文件的访问权限
# open(filename,flag[,mode=0777]): 按照mode指定权限打开文件，默认时给所有用户读写执行的权限，os模块的open()函数和内建的open()函数用法不同
# remove(path): 删除path指定的文件
# rename(old,new): 重命名文件或目录
# stat(path): 返回path指定文件的所有属性
# fstat(path): 返回打开的文件的所有属性
# lseek(fd,pos,how): 设置文件的当前位置，返回当前位置的字节数
# startfile(filepath[,operation]): 启动关联程序打开文件，如：打开html文件，则启动浏览器
# tmpfile(): 创建一个临时文件，文件创建时在OS的临时目录中

# os.path模块常用函数:
# abspath(path): 返回path所在的绝对路径
# isabs(s): 测试路径是否是绝对路径
# dirname(p): 返回目录的路径
# isdir(path): 判断path指定的是否是目录
# exists(path): 判断文件是否存在
# isfile(path): 判断path指定的是否是文件
# getatime(filename): 返回文件的最后访问时间
# getctime(filename): 返回文件的创建时间
# getmtime(filename): 返回文件最后修改时间
# getsize(filename): 返回文件的大小
# split(p): 对路径进行分割，并以列表形式返回
# splitext(p): 从路径中分割文件的扩展名
# splitdrive(p): 从路径中分割驱动器的名称
# walk(top,func,arg): 遍历目录树，于os.walk()的功能相同

FILE_NAME = 'hello.dat'


def test_create_file():
    print '\ntest_create_file 开始'
    # 创建文件
    content = '''hello,this is a long content ,这是一段长内容\n'''
    # 打开一个文件
    f = open(FILE_NAME, 'w+') 
    # 将字符串写入文件
    f.write(content) 
    f.write('hello python world')
    # 关闭文件
    f.close() 


# 按行读取
def test_readline():
    print '\ntest_readline 开始'
    f = open(FILE_NAME)
    while True:
        # 读取文件的每一行
        line = f.readline()
        if line:
            print line
        else:
            break;
    f.close()


# 一次性读取多行:readlines()
def test_readlines():
    print '\ntest_readlines 开始'
    f = open(FILE_NAME)
    # 把文件所有内容存储在列表lines中
    lines = f.readlines()
    
    # 循环读取列表lines中每个元素的内容
    for line in lines:
        print line
    f.close()


# 一次性读取方式read()
def test_read():
    print '\ntest_read 开始'
    f = open(FILE_NAME)
    # 把文件所有内容存储在变量context中
    context = f.read()
    print context
    f.close()


# 控制read()的参数,返回指定字节的内容
def test_read_param():
    print '\ntest_read_param 开始'
    f = open(FILE_NAME)
    cont = f.read(5)
    print 'first 5 bytes:', cont
    print 'current file pointer:', f.tell()
    cont = f.read(3)  # 继续读取3字节内容
    print 'next 3 bytes:', cont
    print 'current file pointer:', f.tell()
    f.close()


# 文件写入:
# writelines()写文件
def test_file_write():
    f = open(FILE_NAME, 'w+')
    li = ['corporations', 'facebook', 'linkedin', 'amazon', 'google', 'apple']
    f.writelines(li)
    f.close()


# 文件删除
def test_remove():
    print 'test_remove 开始'
    import os
    open(FILE_NAME, 'w+')
    current_path = os.path.abspath(__file__)
    print 'type of __file__ :',__file__
    parent_path = os.path.abspath(os.path.dirname(current_path))
    print '当前文件路径:',current_path
    print '当前目录路径:',parent_path
    remove_file_abs_path = parent_path + os.path.sep + FILE_NAME
    print '要删除的文件路径:', remove_file_abs_path
    if os.path.exists(remove_file_abs_path):
        print '文件: %s 存在' % remove_file_abs_path
        os.remove(remove_file_abs_path)
        print '删除%s 成功' % remove_file_abs_path
    else:
        print '文件 %s 不存在' % remove_file_abs_path


if __name__ == '__main__':
    test_create_file()
    test_readline()
    test_readlines()
    test_read()
    test_read_param()
    test_file_write()
    test_remove()
