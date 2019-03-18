# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
所有可能的排列
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
logger = logging.getLogger('ssq_seq')
LOG_FILE = 'ssq_seq.log'
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


def saveAllSSQ():
    count = 0
    times = 0
    param = []
    insert_sql = "insert into ssq_seq (r1,r2,r3,r4,r5,r6,b1)" + ' values(%s,%s,%s,%s,%s,%s,%s)'
    for i1 in range(1, 29):
        if (i1 < 10):
            v1 = '0' + str(i1)
        else:
            v1 = i1
        for i2 in range(i1 + 1, 30):
            if i2 < 10:
                v2 = '0' + str(i2)
            else:
                v2 = i2
            for i3 in range(i2 + 1, 31):
                if i3 < 10:
                    v3 = '0' + str(i3)
                else:
                    v3 = i3
                for i4 in range(i3 + 1, 32):
                    if i4 < 10:
                        v4 = '0' + str(i4)
                    else:
                        v4 = i4
                    for i5 in range(i4 + 1, 33):
                        if i5 < 10:
                            v5 = '0' + str(i5)
                        else:
                            v5 = i5
                        for i6 in range(i5 + 1, 34):
                            if i6 < 10:
                                v6 = '0' + str(i6)
                            else:
                                v6 = i6
                            for i7 in range(1, 17):
                                count += 1
                                if i7 < 10:
                                    v7 = '0' + str(i7)
                                else:
                                    v7 = i7
                                param.append([str(v1), str(v2), str(v3), str(v4), str(v5), str(v6), str(v7)])
                                if count % 100000 == 0:
                                    times = times + 1
                                    insert_count = conn.insertmany(insert_sql, param)
                                    conn.end('commit')
                                    logger.info("times:" + str(times) + " | saveAllSSQ  successful! count:" + str(insert_count))
                                    param = []
    times = times + 1
    insert_count = conn.insertmany(insert_sql, param)
    conn.end('commit')
    logger.info("times:" + str(times) + " | saveAllSSQ  successful! count:" + str(insert_count))


if __name__ == '__main__':
    conn = MySQLConnPool("da")
    config_logger()
    
    saveAllSSQ()
    conn.dispose(1)
