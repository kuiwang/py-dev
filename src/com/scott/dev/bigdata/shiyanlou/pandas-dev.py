# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
https://www.shiyanlou.com/courses/906/learning/
@author: user
'''

import os, sys, logging
from importlib import reload

reload(sys) 
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/data/priv".replace('/', os.sep)
# PY_GEN_PATH = "/vagrant/priv".replace('/', os.sep)
logger = logging.getLogger('syl-pandas-dev')
LOG_FILE = 'syl-pandas-dev.log'
LOG_FORMATTER = '%(message)s'

'''
数据类型
Pandas的数据类型主要有以下几种，
它们分别是：Series（一维数组），DataFrame（二维数组），Panel（三维数组），Panel4D（四维数组），
PanelND（更多维数组）。
其中 Series 和 DataFrame 应用的最为广泛，几乎占据了使用频率 90% 以上。

Series
Series 是 Pandas 中最基本的一维数组形式。其可以储存整数、浮点数、字符串等类型的数据。
Series 基本结构如下：
pandas.Series(data=None, index=None)

其中，data 可以是字典，或者NumPy 里的 ndarray 对象等。index 是数据索引，索引是 Pandas 数据结构中的一大特性，它主要的功能是帮助我们更快速地定位数据。
下面，我们基于 Python 字典新建一个示例 Series。


'''

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


if __name__ == '__main__':
    config_logger()

