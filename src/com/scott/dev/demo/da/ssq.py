# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日

@author: user
'''
import os, sys, json
import logging
import requests
import mysqlutils
import argparse
from bs4 import BeautifulSoup 

reload(sys)  
sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/ssq".replace('/', os.sep)
YC_INDEX_FILE = "bitauto_index.xml"
YC_FEED_LOC = "bitauto_loc.xml"
logger = logging.getLogger('bitauto_feed')
LOG_FILE = 'bitauto_feed_import.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

s = requests.Session()


def get_url(url):
    try:
        UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
        ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        ACCEPT_ENCODING = "gzip, deflate"
        ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9"
        CONNECTION = "keep-alive"
        HOST = "kaijiang.zhcw.com"
        header = {"User-Agent":UA, "Accept":ACCEPT, 'Host':HOST, "Accept-Encoding":ACCEPT_ENCODING, "Accept-Language":ACCEPT_LANGUAGE, "Connection":CONNECTION}
        r = s.get(url, headers=header)
        r.encoding = "utf-8"
    except Exception, e:
        logger.error(e)
    return r.text


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


def saveSSQ(url):
    getPageNum(url)


def getPageNum(url):
    logger.info("getPageNum | url:" + url)
    num = 0
    content = get_url(url)
    soup = BeautifulSoup(content)


def init_parser():
    logger.info('start parse arguments')
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url",
                        type=str,
                        dest='url',
                        required=True,
                        help="数据url"
                        )
    return parser


if __name__ == '__main__':
    conn = mysqlutils.connect_mysql()
    config_logger()
    
    parser = init_parser()
    args = parser.parse_args()
    url = args.url
    
    saveSSQ(url)
    
    conn.close()
