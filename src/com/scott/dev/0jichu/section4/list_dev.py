
'''
Created on 2018年10月19日

@author: user
'''

# list(列表)是Python内置的数据结构，通常作为函数的返回类型，可以实现添加删除和查找操作，元素值可以被修改
# 所有元素包含在一对方括号[]之中
# 列表创建格式如下：list=[ele1,ele2,ele3]
# 列表添加：append(obj),obj可以是元组、列表、字典或任何对象
# 列表删除：remove(),ex:remove(obj),删除元素obj，若obj不在列表中，跑出ValueError异常
from importlib import reload
import sys
reload(sys)
# sys.setdefaultencoding('utf8')


def list_access():
    print ("list_access函数开始")
    lst = ["apple", "banana", "grape", "orange"]
    print (lst)
    print (lst[2])
    lst.append("watermelon")  # 列表末尾添加元素
    print (lst)
    lst.insert(1, "fruit")  # 列表中添加元素
    print (lst)
    lst.remove("grape")
    print (lst)
    print("use foreach in below:")
    for a in lst:
        print(a)
    # lst.remove("a") #会报错
    # print lst.pop()  # 输出从列表中弹出的元素，即最后一个元素
    # print lst

'''
def list_use():
    print "list_use函数开始"
    lst = ["apple", "banana", "grape", "orange"]
    print lst[-2]
    print lst[1:3]
    print lst[-3:-1]
    lst2 = [["apple", "banana"], ["grape"], ["orange"], ["water", "fruit"]]
    for i in range(len(lst2)):
        for j in range(len(lst2[i])):
            print "lst[%s][%s] = %s" % (i, j, lst2[i][j])


def list_concat_operation():
    print "list连接操作"
    lst1 = ["apple", "banana"]
    lst2 = ["grape"]
    lst1.extend(lst2)  # lst1连接lst2
    print lst1
    lst3 = ["water"]
    lst1 = lst1 + lst3  # lst1和lst3连接后赋值给lst1
    print lst1
    lst1 += ["fruit"]  # 使用+=给lst1连接上fruit
    print lst1
    lst1 = ["app", "bpp"] * 2
    print lst1


def list_search():
    print "list_search,list查询操作"
    lst = ["apple", "banana", "grape", "orange"]
    print lst.index("grape")
    print lst.index("banana")
    print "orange" in lst
    print "app" in lst


def list_sort_reverse():
    print "list_sort_reverse,list排序反转操作"
    lst = ["apple", "grape", "banana", "orange"]
    lst.sort()  # 排序
    print "sorted list:" , lst
    lst.reverse()  # 反转操作
    print "reversed list:", lst


def list_stack():
    print "list_stack,list栈操作"
    lst = ["apple", "grape", "banana"]
    print lst
    lst.append("orange")
    print lst
    print "弹出元素：", lst.pop()
    print lst


def list_queue():
    print "list_queue,list队列操作"
    lst = ["apple", "grape", "banana"]
    print lst
    lst.append("orange")
    print lst
    print "弹出元素：", lst.pop(0)
    print lst
'''

if __name__ == '__main__':
    list_access()
#     list_use()
#     list_concat_operation()
#     list_search()
#     list_sort_reverse()
#     list_stack()
#     list_queue()
