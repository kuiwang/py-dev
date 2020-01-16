# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
获得top address,
因使用了br编码，引入了 brotli包
@author: user
'''
import os, sys
import logging
import requests, json
# from com.scott.dev.util.mysqlpool import MySQLConnPool
from bs4 import BeautifulSoup 
from importlib import reload
import socks, socket
import random, time
import brotli
from hashlib import sha256

reload(sys)  
# sys.setdefaultencoding('utf8')

# PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
PY_GEN_PATH = "E:/data/priv".replace('/', os.sep)
PROCESS_NUM = 200
MULTI_API = "http://51.68.204.150:4007/insight-api/addrs/{}"
addr_file = 'E:/data/priv/prime_addr'
logger = logging.getLogger('balance_harvest')
LOG_FILE = 'balance_harvest.log'
LOG_FORMATTER = '%(message)s'

s = requests.Session()


def get_url(url, refer, proxy=None):
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
        ACCEPT = "application/json"
        ACCEPT_ENCODING = "gzip, deflate"
        ACCEPT_LANGUAGE = "zh-cn"
        CONNECTION = "keep-alive"
        HOST = "51.68.204.150:4007"
        # HOST = "chain.api.btc.com"
        UAGENT = 'Harvester/4621 CFNetwork/976 Darwin/18.2.0'
        header = {"HOST":HOST, "User-Agent":UAGENT, "Accept":ACCEPT, "Accept-Encoding":ACCEPT_ENCODING, "Accept-Language":ACCEPT_LANGUAGE, "Connection":CONNECTION}
        r = s.get(url, headers=header)
        sc = r.status_code
        if sc == 200:
            r.encoding = 'utf-8'
            '''
            logger.info('headers in below:\n')
            header_lst = r.headers
            for k, v in header_lst.items():
                logger.info(k + "=" + v)
            logger.info('encoding:\n' + r.encoding)
            '''
            key = 'Content-Encoding'
            # print(response.headers[key])
            if(key in r.headers and r.headers['Content-Encoding'] == 'br'):
                data = brotli.decompress(r.content)
                data1 = data.decode('utf-8')
                # logger.info('data1：' + data1)
                return data1
            # logger.info('r.text:\n' + r.text)
            return r.text
        else:
            return None
    except Exception as e:
        logger.error(e)
        return None


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
    '''
    console = logging.StreamHandler()
    console.setLevel(level=logging.DEBUG)  # 设置为INFO级别
    console.setFormatter(fmter)
    logger.addHandler(console)
    '''


def batchGetBalanceHarvest():
    # logger.info("batchGetBalanceInfo start")
    param = []
    i = 0
    with open(addr_file, 'r') as f:
        addr = f.readline().strip()
        while addr:
            i = i + 1
            # zlogger.info(str(i))
            param.append(addr)
            size = len(param)
            tmp1 = i % PROCESS_NUM
            tmp2 = i / PROCESS_NUM
            if (tmp1 > 0 and tmp1 < PROCESS_NUM):
                page = int (tmp2) + 1
            else:
                page = int (tmp2)
            if(tmp1 == 0):
                
                qry = ','.join(param)
                batch_api = MULTI_API.format(str(qry))
                t = int(random.random() * 5)
                time.sleep(t)
                logger.info('{}-{}'.format(str(page), str(t)))
                resp_json = get_url(batch_api, batch_api)
                try:
                    batch_info = json.loads(resp_json)
                    for address in batch_info:
                        a = address['addrStr']
                        b = address['balance']
                        if int(b) > 0:
                            logger.info('{}|{}'.format(str(a), str(b)))
#                         else:
#                             logger.info('{}'.format(str(a)))
                    param = []
                except Exception as e:
                    logger.error(qry)
            addr = f.readline().strip()
        # logger.info("sum={}".format(str(i)))
        size = len(param)
        if size > 0:
            qry = ','.join(param)
            batch_api = MULTI_API.format(str(qry))
            resp_json = get_url(batch_api, batch_api)
            try:
                batch_info = json.loads(resp_json)
                for address in batch_info:
                    a = address['addrStr']
                    b = address['balance']
                    if int(b) > 0:
                        logger.info('{}|{}'.format(str(a), str(b)))
#                     else:
#                         logger.info('{}'.format(str(a)))
                param = []
            except Exception as e:
                logger.error(qry)
            logger.info("size:{}".format(str(size)))


if __name__ == '__main__':
    config_logger()
    batchGetBalanceHarvest()
    
