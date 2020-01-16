# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
查询手机归属地
@author: user
'''
import os, sys, json
import logging
import requests
from com.scott.dev.util.mysqlpool import MySQLConnPool
from bs4 import BeautifulSoup 
import argparse
from importlib import reload

reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)

logger = logging.getLogger('get_paste_bin')
LOG_FILE = 'get_paste_bin.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
# LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'
LOG_FORMATTER = '%(message)s'
s = requests.Session()

API_LOGIN = "https://pastebin.com/api/api_login.php"
API_GET_RAW = "https://pastebin.com/api/api_raw.php"
API_DEV_KEY = "6ee53c285be05540b24ab48e8611b643"



def get_url(url):
    try:
        UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
        ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        ACCEPT_ENCODING = "gzip, deflate"
        ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9"
        CONNECTION = "keep-alive"
        header = {"User-Agent":UA, "Accept":ACCEPT, "Accept-Encoding":ACCEPT_ENCODING, "Accept-Language":ACCEPT_LANGUAGE, "Connection":CONNECTION}
        r = s.get(url, headers=header)
        r.encoding = "utf-8"
        # logger.info("response:\n" + r.text)
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


def getPhoneLocation(api, phone):
    logger.info("getPhoneLocation from api")
    real_api = api + phone
    phone_info_json = get_url(real_api)
    phoneObj = json.loads(phone_info_json)
    return phoneObj


def init_parser():
    logger.info('start parse arguments')
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user",
                        type=str,
                        dest='user',
                        required=True,
                        help="用户名"
                        )
    parser.add_argument("-p", "--passwd",
                        type=str,
                        dest='password',
                        required=True,
                        help="密码"
                        )
    parser.add_argument("-k", "--keyword",
                        type=str,
                        dest='keyword',
                        required=True,
                        help="关键词"
                        )
    return parser


if __name__ == '__main__':
    config_logger()
    
    parser = init_parser()
    args = parser.parse_args()
    user = args.user
    pwd = args.password
    kw = args.keyword
    
    api_option = "show_paste"
    data_login = {
        "api_dev_key":API_DEV_KEY,
        "api_user_name":API_USER,
        "api_user_password":API_PWD
    }
    api_user_key = requests.post(API_LOGIN, data=data_login).text
    logger.info('user_key:{}'.format(api_user_key))
    data_raw = {
        "api_dev_key":API_DEV_KEY,
        "api_user_key":api_user_key,
        "api_paste_key":kw,
        "api_option":api_option
    }
    raw_content = requests.post(API_GET_RAW,data=data_raw).text
    logger.info(raw_content)
    
