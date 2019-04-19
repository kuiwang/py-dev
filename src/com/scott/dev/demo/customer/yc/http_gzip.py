# -*- coding:utf-8 -*-

'''
Created on 2019年4月4日

@author: user
'''
import os, sys
import logging
import requests
import json
from importlib import reload

reload(sys)  
s = requests.Session()
URL = "http://accept.dy-porn91.me/api/accept"

PY_GEN_PATH = "D:/download/pygen/".replace('/', os.sep)
logger = logging.getLogger('http_gzip')
LOG_FILE = 'http_gzip.log'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'


def config_logger():
    logger.setLevel(logging.DEBUG)
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


def post_url(url, refer=None):
    try:
        HEADER_UA = "QHAwemeDemo/1.0.5 (com.Xs.douyVideoK; build:7; iOS 12.1.4) Alamofire/4.8.1"
        HEADER_METHOD = "POST"
        HEADER_CONN = "keep-alive"
        HOST = "accept.dy-porn91.me"
        HEADER_CONTENT_TYPE = "application/json"
        HEADER_ACCEPT_ENCODING = "gzip;q=1.0, compress;q=0.5"
        HEADER_ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9"
        header = {"User-Agent":HEADER_UA, "Host":HOST, "method":HEADER_METHOD,
                  "device_id":"ba2a8ef509b85de263ce2c1c1af512e2", "Connection":HEADER_CONN,
                  "Accept":HEADER_CONTENT_TYPE, 'version':"1.0.5", "accept-language":HEADER_ACCEPT_LANGUAGE,
                  "Content-Type":HEADER_CONTENT_TYPE, "Accept-Encoding":HEADER_ACCEPT_ENCODING
        }
        
        data = {"data":"viDQmHGZ3XJGsoxN7qkdsvpk4\/PBaLFkLIuN510BC9nCZosj7wbm4PvRcS4HfaVxUQWsqprVXsgNXOzTmaCpwbSNrMmkO5XMRXcSxpd+G1Zo1RhPZh4x90t80X9cfSy\/TcbP1DEOl9WmWSAAgKyc8jbbx2EybrvuJoFRgN7LFiviKyYBnVFfjAFrov\/UPHBhZGZZ0ZiKsCeY\/17K9MFfG\/lyYaFqy5rPfOWY25lrXtRT+Gcm32GyRG3BuKH4fv1yaOAcLSthub7pXQD+BF+yZlxeLiEebePQcAwX0Td\/WmDoee\/2hiiZy0d625b1AsajzFKtESyPbIW4T18RGcz3p6wW9kL5l9Ky+nZEk+jGffO64s7DX5HWO1NRZTsiDvtizdSrR4vGChTiORCyDZnQiA=="}
        r = s.post(url, headers=header, data=json.dumps(data))
        content = r.content
        # data = brotli.decompress(content)
        # data1 = data.decode('utf-8')
        # logger.info("response:\n" + data1)
        return json.loads(content)
    except Exception as e:
        logger.error(e)
        print(e)
        pass


if __name__ == '__main__':
    import urllib
    config_logger()
    res = post_url(URL)
    logger.info(res)
    if res['message'] == 'success':
        result = res['result']
        result = urllib.parse.unquote(result)
        logger.info(result)
    
