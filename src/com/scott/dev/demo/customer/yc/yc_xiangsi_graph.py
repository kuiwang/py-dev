# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
获得相似车型信息
@author: user
'''
'''
G    一个网络图
pos    图像的布局，可选择参数；如果是字典元素，则节点是关键字，位置是对应的值。如果没有指明，则会是spring的布局；也可以使用其他类型的布局，具体可以查阅networkx.layout
arrows    布尔值，默认True; 对于有向图，如果是True则会画出箭头
with_labels    布尔值，默认为True; 如果为True，则在节点上标注标签
ax    坐标设置，可选择参数；依照设置好的Matplotlib坐标画图
nodelist    一个列表，默认G.nodes(); 给定节点
edgelist    一个列表，默认G.edges();给定边
node_size    向量或者标量，默认300;表示节点的数目，必须和nodelist长度保持一致
node_color    颜色字符串，默认’r’;可以是单个颜色，也可以是和nodelist长度相等的一列颜色字符串。
node_shape    字符串，默认’o’;节点的形状。
alpha    浮点数，默认1;节点或者边的透明度
cmap    Matplotlib的颜色映射，默认None; 用来表示节点对应的强度
vmin,vmax    浮点数，默认None;节点颜色映射尺度的最大和最小值
linewidths    [None|标量|一列值];图像边界的线宽
width    浮点数，默认1;边的的线宽
edge_color    颜色字符串，默认’r’;边的颜色，可以是一个颜色值，也可以是一列颜色值，如果是一列颜色值，其长度必须和edgelist的长度保持一致
edge_cmap    Matplotlib的颜色映射，默认None; 用来表示边对应的强度
edge_vmin,edge_vmax    浮点数，默认None;边的颜色映射尺度的最大和最小值
style    字符参数，默认’solid’; 边的线的风格，可以是 soldid，dashed， dotted，dashdot
labels    字典元素，默认None;文本形式的节点标签
font_size    整型，默认None; 文本标签的字体大小
font_color    字符串，默认’k’(黑色)
font_weight    字符串，默认’normal’
font_family    字符串，默认’sans-serif’
label
'''
import os, sys
import logging
import requests
from com.scott.dev.util.mysqlpool import MySQLConnPool
from importlib import reload
import networkx as nx
import matplotlib.pyplot as plt

reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
MODEL_PREFIX = "https://car.bitauto.com"
logger = logging.getLogger('chekuan_graph')
LOG_FILE = 'chekuan_graph.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

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
    console = logging.StreamHandler()
    console.setLevel(level=logging.DEBUG)  # 设置为INFO级别
    console.setFormatter(fmter)
    logger.addHandler(console)


def getSimilarCarModel():
    logger.info("getSimilarCarModel start")
    select_sql = 'select y.pid as src_id, y.name as src_name, t.similar_id as dst_id, t.similar_name as dst_name from  ( select pid,url,name  from yc_info t  where instr(t.pid,"-")=0  order by pid desc  ) y join  similar_model_info t  on y.pid = t.id limit 50'
    return conn.queryall(select_sql)


def drawGraph():
    logger.info('生成一个空的有向图')
    G = nx.DiGraph()  # 一个网络图
    similar_lst = getSimilarCarModel()
    size = len(similar_lst)
    logger.info('为这个网络添加节点')
    for i in range(size):
        src_id = ''.join(similar_lst[i][0])
        src_name = ''.join(similar_lst[i][1])
        dest_id = ''.join(similar_lst[i][2])
        dest_name = ''.join(similar_lst[i][3])
        G.add_node(src_id)  # 添加节点
        G.add_weighted_edges_from([(src_id, dest_id, 1)])  # 添加带权中的边
    '''
    logger.info('输出网络中的节点...')
    logger.info(G.nodes())
    logger.info('输出网络中的边...')
    logger.info(G.edges())
    '''
    logger.info('输出网络中边的数目')
    logger.info(G.number_of_edges())
    logger.info('输出网络中节点的数目...')
    logger.info(G.number_of_nodes())
    logger.info('给网路设置布局...')
    
    # 图像的布局，可选择参数；如果是字典元素，则节点是关键字，位置是对应的值。如果没有指明，则会是spring的布局；也可以使用其他类型的布局，具体可以查阅networkx.layout
    pos = nx.spring_layout(G)
    #pos = nx.shell_layout(G)
    logger.info('画出网络图像：')
    # nx.draw(G,pos,with_labels=True, node_color='white', edge_color='red', node_size=400, alpha=0.5 )
    nx.draw_networkx(G, pos, with_labels=True, node_color='yellow', edge_color='red', node_size=50, alpha=0.5)
    plt.show()


if __name__ == '__main__':
    conn = MySQLConnPool('yc')
    config_logger()
    
    drawGraph()
    
    conn.dispose(1)
