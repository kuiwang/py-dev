# coding: utf-8
import time
import os, sys
import json
import logging
import requests
from com.scott.dev.util.mysqlpool import MySQLConnPool
import random
from db import REDIS
from importlib import reload
import demjson
reload(sys)

PY_GEN_PATH = "D:/download/pygen/gh".replace('/', os.sep)
MODEL_PREFIX = "https://car.bitauto.com"
logger = logging.getLogger('gh_search')
LOG_FILE = 'gh_search.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

s = requests.Session()

REPO_SHOW = '1'
REPO_HIDDEN = '0'

# SEARCH_API = 'https://api.github.com/search/repositories?q=%s&sort=updated&order=desc&page=%s'
SEARCH_API = 'https://api.github.com/search/repositories?q={}&sort=updated&order=desc&page={}'


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


def search_github(keyword):
    # 爬取 20 页最新的列表
    for i in range(1, 2):
        
        url = SEARCH_API.format(keyword, str(i))
        res = requests.get(url)
        logger.info("url:{},keyword:{}".format(url, keyword))
        # res = get_url(url)
        repo_list = res.json()['items']
        # logger.info(res.json())
        logger.info(repo_list)
        for repo in repo_list:
            repo_name = repo['html_url']
            repo_desc = repo['description']
            repo_star = repo['stargazers_count']
            logger.info(repo_name)
            is_show = REPO_SHOW
#             desc = {
#                 'repo_desc': repo['description'],
#                 'star': repo['stargazers_count'],
#                 'is_show': REPO_SHOW
#             }
        time.sleep(10)


if __name__ == '__main__':
    conn = MySQLConnPool('test')
    config_logger()
    
    # keywords = raw_input('input your keyword in below:')
    keyword = input('input your keyword in below ,0 to quit:')
    while  str(keyword) != str(0) :
        search_github(keyword)
        keyword = input('input your keyword in below ,0 to quit:')
    
    conn.dispose(1)
