# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
https://bitkeys.work/?page=0
@author: user
'''
import os, sys, logging
from bs4 import BeautifulSoup
from importlib import reload
import time, random, requests

import numpy as np
import pandas as pd
import pickle
from pylab import matplotlib as mpl
from matplotlib import pyplot as plt
import seaborn as sns
import re
import wordcloud

reload(sys) 
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/data/priv".replace('/', os.sep)
# PY_GEN_PATH = "/vagrant/priv".replace('/', os.sep)
logger = logging.getLogger('scikit-dev')
LOG_FILE = 'scikit-dev.log'
LOG_FORMATTER = '%(message)s'
DATA_FILE = "D:/data/priv/20191112-20191118-760.csv"
DEV_DATA_FILE = "D:/data/priv/20191112-20191118-760-dev.csv1"
DEV_DATA_FILE = 'D:/data/priv/20191112-20191118-760-1.csv'
# GEN_FILE = 'D:/data/priv/dev_hotel.csv'
GEN_FILE = 'D:/data/priv/20191112-20191118-760-1.csv'
RECORD_COUNT = 10000
s = requests.Session()


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
    '''
    console = logging.StreamHandler()
    console.setLevel(level=logging.DEBUG)  # 设置为INFO级别
    console.setFormatter(fmter)
    logger.addHandler(console)
    '''

# see here: 
# https://www.cnblogs.com/pinard/p/6016029.html


# 获取数据
def load_data(file_name):
    dataMat = []
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            cur_line = line.strip().split('\t')
            dataMat.append(cur_line)
    return dataMat


def dev_scikit():
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn import datasets, linear_model
    import matplotlib.pyplot as plt
    
    # train = pd.read_table(DEV_DATA_FILE)
    data = pd.read_csv(DEV_DATA_FILE, delimiter='\t')
    
    # tail:读取最后5行，如果是前几行的话使用head()
    # print(data.tail(2))
    
    # 查看数据维度  , res:(1000, 11),表示有1000个样本,每个样本11列
    print(data.shape)
    # print(data)
    
    # 现在准备样本特征X,用11列作为样本特征
    # day,zid,zid_type,industry_id,advertiser_id,update_time,gid,gname,gprice,from_city,to_city
    # X = data[['day','zid','zid_type','industry_id','advertiser_id','update_time','gid','gname','gprice','from_city','to_city']]
    X = data[['day', 'zid', 'gid', 'gname', 'gprice', 'from_city', 'to_city']]
    print(X.head())

    
def zfsjfx1():
    # https://blog.csdn.net/qq_25174673/article/details/86019549
    from matplotlib import pyplot as plt
    import pandas as pd
    import jieba
    import wordcloud 
    from scipy.misc import imread
    
    plt.rcParams['font.family'] = 'SimHei'  # 配置中文字体
    plt.rcParams['font.size'] = 15  # 更改默认字体大小
    data = pd.read_csv(DEV_DATA_FILE, delimiter='\t')


def zfsjfx_2():
    # https://zhuanlan.zhihu.com/p/32095072
    # %matplotlib inline

    mpl.rcParams['font.sans-serif'] = ['Simhei']
    mpl.rcParams['axes.unicode_minus'] = False
    
    df = pd.read_csv(GEN_FILE, delimiter='\t')
    '''
    print('df size:')
    print(df.shape)
    print(df.head())
    '''
    # 1.删除冗余字段
    df2 = df.drop(['update_time', 'advertiser_id', 'industry_id'], axis=1)
    '''
    print('df2 size:')
    print(df2.shape)
    print(df2.head())
    '''
    
    # 2.删除重复数据
    uniq_zid = len(np.unique(df2.zid))
    print('uniq_zid:{}'.format(str(uniq_zid)))
    uniq_gid = len(np.unique(df2.gid))
    print('uniq_gid:{}'.format(str(uniq_gid)))
    
    df3 = df2
    print(df3.head())
    
    # 3.删除异常数据，此处删除to_city不为空的数据（即删除机票浏览人群的数据）
    
    print('df3({} rows) null value:\n'.format(df3.shape[0]))
    print(df3.isnull().sum())
    
    count_by_fromcity = df3.groupby(['from_city'])['zid'].count().sort_values(ascending=False)
    Make_Barplot(count_by_fromcity, title='酒店城市访客分布')
    

def Make_Barplot(group_date, title):
    """
    第一个参数：传入聚合后的数据集
    第二个参数：柱状图标题
    """
    fig = plt.figure(figsize=(10, 7))
    ax1 = plt.subplot(111)
    rect = ax1.bar(np.arange(len(group_date)), group_date.values, facecolor='orange', alpha=0.6, width=0.6)

    # 设置X轴刻度标签
    def auto_xtricks(rects, xticks):
        x = []
        for rect in rects:
            x.append(rect.get_x() + rect.get_width() / 2)
        x = tuple(x)
        plt.xticks(x, xticks)

    auto_xtricks(rect, group_date.index)
    ax1.set_xticklabels(group_date.index)

    # 设置数据标签
    def auto_tag(rects, data=None, offset=[0, 0]):
        for rect in rects:
            try:
                height = rect.get_height()
                plt.text(rect.get_x() + rect.get_width() / 2.4, 1.01 * height, '%s' % int(height)) 

            except AttributeError:
                x = range(len(data))
                y = data.values
                for i in range(len(x)):
                    plt.text(x[i] + offset[0] + 0.05 + offset[1], y[i]) 

    auto_tag(rect, offset=[-1, 0])
    ax1.set_title(title) 

    plt.show()


def gen_dev_file():
    header = 'day    zid    zid_type    industry_id    advertiser_id    update_time    gid    gname    gprice    from_city    to_city'
    dest_file_path = os.path.join(GEN_FILE)
    dest_file = open(dest_file_path, 'a', encoding='utf-8')
    dest_file.writelines(header + "\n")
    num = 0
    with open(DEV_DATA_FILE, 'r', encoding='utf-8') as f:
        content = f.readline().strip()
        while((num < RECORD_COUNT) and (content)):
            dest_file.writelines(content + "\n")
            num = num + 1
            content = f.readline().strip()
    dest_file.close()


if __name__ == '__main__':
    from sklearn import datasets
    config_logger()
    # dev_scikit()
    zfsjfx_2()
    # gen_dev_file()

