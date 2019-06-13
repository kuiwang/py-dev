# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日

@author: user
'''
import os, sys, json
import hashlib, datetime
import logging
import requests
from importlib import reload
import random
import argparse

reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/".replace('/', os.sep)
logger = logging.getLogger('picc')
LOG_FILE = 'picc.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

s = requests.Session()
PICC_BASE_PATH = "http://mar.zhongyuanib.com"
PICC_LDS_API = PICC_BASE_PATH + "/thirdPartyLeaveMsg/insert?accessKeyId={}&timestamp={}&unique={}&sign={}"


def post_url(url, send_data):
    data = None
    try:
        UA_LST = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
              'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
              'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
              'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
              'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
              'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']
        ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        ACCEPT_ENCODING = "gzip, deflate, br"
        ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9"
        CONTENT_TYPE = "application/json;chartset=UTF-8"
        HOST = 'mar.zhongyuanib.com'
        header = {"User-Agent":UA_LST[random.randrange(0, len(UA_LST))], "Content-Type":CONTENT_TYPE, 'HOST':HOST, 'Cache-Control':'no-cache', "Accept":ACCEPT, "Accept-Encoding":ACCEPT_ENCODING, "Accept-Language":ACCEPT_LANGUAGE}
        r = s.post(url, data=send_data, headers=header)
        txt = r.text
        logger.info("response:" + txt)
    except Exception as e:
        logger.error(e)
    return data


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


def picc_leads(api_key, api_sec, api_prodno):
    ts = int(time.time() * 1000)
    m2 = hashlib.md5()
    hash_str = (api_key + api_sec + str(ts) + str(ts)).encode('utf-8')
    m2.update(hash_str)
    sign = m2.hexdigest()
    api = PICC_LDS_API.format(api_key, str(ts), str(ts), str(sign))
    logger.info('api:{}'.format(api))
    
    user_info = {
        "productNo":api_prodno,
        "userInfo":{
            "name":"测试人员",
            "mobilePhone":"13123456789"
        }
    }
    
    json_user_info = json.dumps(user_info).encode('utf-8')
    # logger.info("user_info:" + json_user_info)
    # unsign_data = json_user_info + token + str(ts)
    
    logger.info("post_data:" + str(json_user_info))
    post_url(api, json_user_info)


def init_parser():
    logger.info('start parse arguments')
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key",
                        type=str,
                        dest='key',
                        required=True,
                        help="api key"
                        )
    parser.add_argument("-s", "--secret",
                        type=str,
                        dest='secret',
                        required=True,
                        help="api secret"
                        )
    parser.add_argument("-p", "--prodno",
                        type=str,
                        dest='prodno',
                        required=True,
                        help="api prodno"
                        )
    return parser


if __name__ == '__main__':
    import time
    config_logger()
    
    parser = init_parser()
    args = parser.parse_args()
    api_key = args.key
    api_sec = args.secret
    api_prodno = args.prodno
    
    picc_leads(api_key, api_sec, api_prodno)
