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
logger = logging.getLogger('ssq_da')
LOG_FILE = 'ssq_da.log'
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
    except Exception as e:
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
    (total_page, total_record) = getPageAndRecordNum(url)
    for n in range(1, int(total_page) + 1):
        href = "http://kaijiang.zhcw.com/zhcw/html/ssq/list_" + str(n) + ".html"
        saveDetail(href)


def saveDetail(url):
    logger.info("saveDetail | url:" + url)
    content = get_url(url)
    soup = BeautifulSoup(content, "lxml")
    tbl = soup.find("body").find("table")
    tr_list = tbl.findAll(name="tr")
    for tr in tr_list:
        td_list = tr.findAll(name="td")
        td_size = len(td_list)
        if (td_list is None or td_size == 0):
            continue
        # logger.info("td size:" + str(td_size))
        if td_size == 7:
            kjrq = td_list[0].text
            qh = td_list[1].text
            em_list = td_list[2].findAll("em")
            zjhm = ""
            for em in em_list:
                zjhm = zjhm + em.text + ","
            xse = td_list[3].find("strong").text.replace(",","")
            cat1 = td_list[4].find("strong").text
            cat2 = td_list[5].find("strong").text
            logger.info(kjrq + " | " + str(qh) + " | " + zjhm + " | " + str(xse) + " | " + str(cat1) + " | " + str(cat2))


def getPageAndRecordNum(url):
    logger.info("getPageAndRecordNum | url:" + url)
    total_page = 0
    total_record = 0
    content = get_url(url)
    soup = BeautifulSoup(content, "lxml")
    tbl = soup.find("body").find("table")
    tr_list = tbl.findAll(name="tr")
    for tr in tr_list:
        td = tr.find("td", attrs={"colspan":"7"})
        if td is None:
            continue
        p_tag = td.find("p", attrs={"class":"pg"})
        strong_list = p_tag.findAll(name="strong")
        for strong in strong_list:
            total_page = strong.text
            total_record = strong.next_sibling.next_sibling.text
            break
    logger.info("page_num:" + str(total_page) + " | record_num:" + str(total_record))
    return (total_page, total_record)


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
    conn = MySQLConnPool("yc")
    config_logger()
    
    parser = init_parser()
    args = parser.parse_args()
    url = args.url
    
    # saveSSQ(url)
    saveDetail(url)
    conn.dispose(1)
