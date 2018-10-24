# -*- coding:utf-8 -*-

# 函数定义：使用def定义，使用前必须定义，函数的类型即返回值的类型，定义格式如下：
# def 函数名(参数1,参数2...):
#    return 表达式
# 参数可以有1个或多个，参数之间用逗号分隔，这种参数成为形式参数

# 函数调用格式如下：
# 函数名(实参1,实参2...)

# 函数的参数：
# python中任何东西都是对象，因此只有引用传参的方式，
# python通过名称绑定的机制，把实际参数的值和形式参数的名称绑定在一起，即：
# 把形式参数传递到函数所在的局部命名空间内，形式参数和实际参数指向内存中同一个存储空间

# 函数参数支持默认值，当某个参数没有传递实际值时，函数将使用默认参数计算，
# 例如可以给arichmetic()参数提供默认值


def arichmetic(x=1, y=1, opt='+'):
    result = {
        "+":x + y,
        "-":x - y,
        "*":x * y,
        "/":x / y
    }
    return result.get(opt)


def test_arichmetic():
    print arichmetic(1, 2)
    print arichmetic(1, 2, '-')
    print arichmetic(y=3, opt="-")
    print arichmetic(x=4, opt='-')
    print arichmetic(y=3, x=4, opt='-')


#变长参数：
#开发中常需要传递可变长度的参数，在函数的参数前使用标识符"*"可以实现这个功能
#"*"可以引用元组，把多个参数和到一个元组中
#ex:
# def func(*args):
#    print args
# func(1,2,3)

#还提供了一个标识符"**",在形参前加一个"**"，可以引用一个字典，根据实际参数的赋值表达式生成字典
#ex：
#下面实现一个在一个字典中匹配元组的元素，设计两个参宿，一个待匹配的元组，标识为*t,另一个是字典，标识为**d
#函数调用时，实际参数分成两部分，一部分参数是若干个数字或字符串，另一部分参数是赋值表达式

def search(*t,**d):
    keys = d.keys()
    values=d.values()
    print keys
    print values
    for arg in t:
        for k in keys:
            if arg == k:
                print 'find:',d[k]
def test_search_in_dictionary():
    search("one","three",one="1",two="2",three="3")

def func(*args):
    print args

def test_change_params():
    #由于参数使用了*args格式，因此传入的实际参数被打包到一个元组中，输出结果为(1,2,3)
    func(1,2,3)


if __name__ == '__main__':
    test_arichmetic()
    test_change_params()
    test_search_in_dictionary()
