# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日

@author: user
'''
import os, sys, json
import logging
import requests
import argparse
from bs4 import BeautifulSoup 
from com.scott.dev.util.mysqlpool import MySQLConnPool
from importlib import reload

reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/ssq".replace('/', os.sep)
YC_INDEX_FILE = "bitauto_index.xml"
YC_FEED_LOC = "bitauto_loc.xml"
logger = logging.getLogger('ssq2')
LOG_FILE = 'ssq2.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'


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


def saveRedAndBlue():
    logger.info("saveRedAndBlue")
    param = []
    insert_sql = "insert into red (num)" + ' values(%s)'
    
    for n in range(1, 33):
        if n < 10:
            v = '0' + str(n)
        else:
            v = n
        param.append([str(v)])
    insert_count = conn.insertmany(insert_sql, param)
    conn.end('commit')
    logger.info("save red count:" + str(insert_count))
    
    insert_sql = "insert into blue (num)" + ' values(%s)'
    
    param = []
    for n in range(1, 17):
        if n < 10:
            v = '0' + str(n)
        else:
            v = n
        param.append([str(v)])
    insert_count = conn.insertmany(insert_sql, param)
    conn.end('commit')
    logger.info("save blue count:" + str(insert_count))


if __name__ == '__main__':
    conn = MySQLConnPool("test")
    config_logger()
    
    saveRedAndBlue()
    conn.dispose(1)
