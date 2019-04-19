# -*- coding:utf-8 -*-
'''
Created on 2019年2月13日

@author: user
'''
import os, sys, logging
from importlib import reload

reload(sys)

pwd = os.getcwd()

PY_GEN_PATH = "D:/download/pygen/ml".replace('/', os.sep)
logger = logging.getLogger('kaggle_titanic')
LOG_FILE = 'kaggle_titanic.log'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

train_file = 'train.csv'
test_file = 'test.csv'
train_path = os.path.join(PY_GEN_PATH, train_file)
test_path = os.path.join(PY_GEN_PATH, test_file)


def config_logger():
    logger.setLevel(logging.DEBUG)
    if not os.path.exists(PY_GEN_PATH):
        logger.info("文件夹不存在,已自行创建")
        os.makedirs(PY_GEN_PATH, 777)
    handler = logging.FileHandler(os.path.join(PY_GEN_PATH, LOG_FILE))
    handler.setLevel(logging.DEBUG)
    fmter = logging.Formatter(LOG_FORMATTER)
    handler.setFormatter(fmter)
    logger.addHandler(handler)

    # 控制台打印
    console = logging.StreamHandler()
    console.setLevel(level=logging.DEBUG)  # 设置为INFO级别
    console.setFormatter(fmter)
    logger.addHandler(console)


def train_info():
    import pandas as pd  # 数据分析
    import numpy as np  # 科学计算
    from pandas import Series, DataFrame
    dt = pd.read_csv(train_path)
    # logger.info(dt)
    logger.info(dt.info())
    logger.info( dt.describe())
    
    return dt


def view_all(data_train):
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    fig = plt.figure()
    fig.set(alpha=0.2)  # 设定图表颜色alpha参数

    plt.subplot2grid((2, 3), (0, 0))  # 在一张大图里分列几个小图
    data_train.Survived.value_counts().plot(kind='bar')  # 柱状图 
    plt.title(u"获救情况 (1为获救)")  # 标题
    plt.ylabel(u"人数")  
    
    plt.subplot2grid((2, 3), (0, 1))
    data_train.Pclass.value_counts().plot(kind="bar")
    plt.ylabel(u"人数")
    plt.title(u"乘客等级分布")
    
    plt.subplot2grid((2, 3), (0, 2))
    plt.scatter(data_train.Survived, data_train.Age)
    plt.ylabel(u"年龄")  # 设定纵坐标名称
    plt.grid(b=True, which='major', axis='y') 
    plt.title(u"按年龄看获救分布 (1为获救)")
    
    plt.subplot2grid((2, 3), (1, 0), colspan=2)
    data_train.Age[data_train.Pclass == 1].plot(kind='kde')   
    data_train.Age[data_train.Pclass == 2].plot(kind='kde')
    data_train.Age[data_train.Pclass == 3].plot(kind='kde')
    plt.xlabel(u"年龄")  # plots an axis lable
    plt.ylabel(u"密度") 
    plt.title(u"各等级的乘客年龄分布")
    plt.legend((u'头等舱', u'2等舱', u'3等舱'), loc='best')  # sets our legend for our graph.
    
    plt.subplot2grid((2, 3), (1, 2))
    data_train.Embarked.value_counts().plot(kind='bar')
    plt.title(u"各登船口岸上船人数")
    plt.ylabel(u"人数")  
    plt.show()
    

if __name__ == '__main__':
    config_logger()
    data_train = train_info()
    # view_all(data_train)
