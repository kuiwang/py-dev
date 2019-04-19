# -*- coding:utf-8 -*-
'''
Created on 2019年2月13日

@author: user
'''
import os, sys
# pandas 数据分析
import pandas as pd
# numpy 科学计算
import numpy as np
from pandas import Series, DataFrame

pwd = os.getcwd()
train_file = 'train.csv'
test_file = 'test.csv'
cur_dir = os.path.join(pwd)
train_path = os.path.join(cur_dir, train_file)
test_path = os.path.join(cur_dir, test_file)


def train_info():
    dt=pd.read_csv(train_path)
    return dt
    '''
    print data_train
    print data_train.info()
    print data_train.describe()
    '''
def all_view(data_train):
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    fig = plt.figure()
    fig.set(alpha=0.2)  # 设定图表颜色alpha参数
    
    plt.subplot2grid((2,3),(0,0))             # 在一张大图里分列几个小图
    data_train.Survived.value_counts().plot(kind='bar')# 柱状图
    plt.title(u"获救情况 (1为获救)") # 标题
    plt.ylabel(u"人数")
    
    plt.subplot2grid((2,3),(0,1))
    data_train.Pclass.value_counts().plot(kind="bar")
    plt.ylabel(u"人数")
    plt.title(u"乘客等级分布")
    
    plt.subplot2grid((2,3),(0,2))
    #plt.scatter(data_train.Survived, data_train.Age)
    plt.scatter(data_train.Age, data_train.Survived)
    plt.ylabel(u"年龄")                         # 设定纵坐标名称
    plt.grid(b=True, which='major', axis='y')
    plt.title(u"按年龄看获救分布 (1为获救)")
    
    plt.subplot2grid((2,3),(1,0), colspan=2)
    data_train.Age[data_train.Pclass == 1].plot(kind='kde')
    data_train.Age[data_train.Pclass == 2].plot(kind='kde')
    data_train.Age[data_train.Pclass == 3].plot(kind='kde')
    
    plt.xlabel(u"年龄")# plots an axis lable
    plt.ylabel(u"密度")
    plt.title(u"各等级的乘客年龄分布")
    plt.legend((u'头等舱', u'2等舱',u'3等舱'),loc='best') # sets our legend for our graph.
    
    plt.subplot2grid((2,3),(1,2))
    data_train.Embarked.value_counts().plot(kind='bar')
    plt.title(u"各登船口岸上船人数")
    plt.ylabel(u"人数")
    plt.show()
    
def passenger_level(data_train):
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    ##################################
    #看看各乘客等级的获救情况
    fig = plt.figure()
    fig.set(alpha=0.2)  # 设定图表颜色alpha参数
    
    Survived_0 = data_train.Pclass[data_train.Survived == 0].value_counts()
    Survived_1 = data_train.Pclass[data_train.Survived == 1].value_counts()
    df=pd.DataFrame({u'获救':Survived_1, u'未获救':Survived_0})
    df.plot(kind='bar', stacked=True)
    plt.title(u"各乘客等级的获救情况")
    plt.xlabel(u"乘客等级")
    plt.ylabel(u"人数")
    plt.show()
    
def passenger_gender(data_train):
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    #看看各性别的获救情况
    fig = plt.figure()
    fig.set(alpha=0.2)  # 设定图表颜色alpha参数
    Survived_m = data_train.Survived[data_train.Sex == 'male'].value_counts()
    Survived_f = data_train.Survived[data_train.Sex == 'female'].value_counts()
    df=pd.DataFrame({u'男性':Survived_m, u'女性':Survived_f})
    df.plot(kind='bar', stacked=True)
    plt.title(u"按性别看获救情况")
    plt.xlabel(u"性别")
    plt.ylabel(u"人数")
    plt.show()
    
def passenger_cang(data_train):
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    #然后我们再来看看各种舱级别情况下各性别的获救情况
    fig=plt.figure()
    fig.set(alpha=0.65) # 设置图像透明度，无所谓
    plt.title(u"根据舱等级和性别的获救情况")
    ax1=fig.add_subplot(141)
    data_train.Survived[data_train.Sex == 'female'][data_train.Pclass != 3].value_counts().plot(kind='bar', label="female highclass", color='#FA2479')
    ax1.set_xticklabels([u"获救", u"未获救"], rotation=0)
    ax1.legend([u"女性/高级舱"], loc='best')
    ax2=fig.add_subplot(142, sharey=ax1)
    data_train.Survived[data_train.Sex == 'female'][data_train.Pclass == 3].value_counts().plot(kind='bar', label='female, low class', color='pink')
    ax2.set_xticklabels([u"未获救", u"获救"], rotation=0)
    plt.legend([u"女性/低级舱"], loc='best')
    ax3=fig.add_subplot(143, sharey=ax1)
    data_train.Survived[data_train.Sex == 'male'][data_train.Pclass != 3].value_counts().plot(kind='bar', label='male, high class',color='lightblue')
    ax3.set_xticklabels([u"未获救", u"获救"], rotation=0)
    plt.legend([u"男性/高级舱"], loc='best')
    ax4=fig.add_subplot(144, sharey=ax1)
    data_train.Survived[data_train.Sex == 'male'][data_train.Pclass == 3].value_counts().plot(kind='bar', label='male low class', color='steelblue')
    ax4.set_xticklabels([u"未获救", u"获救"], rotation=0)
    plt.legend([u"男性/低级舱"], loc='best')
    plt.show()

def arrival_survived(data_train):
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    #各登船港口的获救情况。
    fig = plt.figure()
    fig.set(alpha=0.2)  # 设定图表颜色alpha参数
    Survived_0 = data_train.Embarked[data_train.Survived == 0].value_counts()
    Survived_1 = data_train.Embarked[data_train.Survived == 1].value_counts()
    df=pd.DataFrame({u'获救':Survived_1, u'未获救':Survived_0})
    df.plot(kind='bar', stacked=True)
    plt.title(u"各登录港口乘客的获救情况")
    plt.xlabel(u"登录港口")
    plt.ylabel(u"人数")
    plt.show()
    

if __name__ == '__main__':
    data_train = train_info()
    all_view(data_train)
#     passenger_level(data_train)
#     passenger_gender(data_train)
#     passenger_cang(data_train)
