# -*- coding:utf-8 -*-
'''
Created on 2019年4月18日

@author: user
'''

import os, sys, json
import logging
import requests
from com.scott.dev.util.mysqlpool import MySQLConnPool
from bs4 import BeautifulSoup 
from importlib import reload

reload(sys)  

IP_API="http://ip-api.com/json/{}?lang=zh-CN"
s = requests.Session()
PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)

logger = logging.getLogger('test')
LOG_FILE = 'test_dev.log'
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

def get_url(url):
    try:
        UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
        ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        ACCEPT_ENCODING = "gzip, deflate"
        ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9"
        CONNECTION = "keep-alive"
        HOST="ip-api.com"
        header = {"User-Agent":UA, "Accept":ACCEPT, 'HOST':HOST,"Accept-Encoding":ACCEPT_ENCODING, "Accept-Language":ACCEPT_LANGUAGE, "Connection":CONNECTION}
        r = s.get(url, headers=header)
        r.encoding = "utf-8"
        # logger.info("response:\n" + r.text)
    except Exception as e:
        logger.error(e)
    return r.text

def test_getRealId():
    long_id = 1159395429071226629
    print (long_id & 0xffff)

def test_getIPLocation(ip):
    real_api = IP_API.format(str(ip))
    ip_info_json = get_url(real_api)
    ip_info_json = json.loads(ip_info_json)
    status = ip_info_json['status']
    if status =='success':
        net_type = ip_info_json['as']
        city = ip_info_json['city']
        country = ip_info_json['country']
        countryCode = ip_info_json['countryCode']
        isp = ip_info_json['isp']
        lat = ip_info_json['lat']
        lon = ip_info_json['lon']
        ip = ip_info_json['query']
        region = ip_info_json['region']
        regionName = ip_info_json['regionName']
        timezone = ip_info_json['timezone']
        logger.info('\n{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(str(net_type),str(city),str(country),str(countryCode),str(isp),str(lat),str(lon),str(ip),str(region),str(regionName),str(timezone)))
#     ipObj = json.loads(ip_info_json)

if __name__ == '__main__':
    config_logger()
    #test_getRealId()
    ip='61.158.146.46'
    test_getIPLocation(ip)
