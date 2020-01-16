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
import itertools
from hashlib import sha256
from bitcoinutils.keys import  P2shAddress, PrivateKey

reload(sys)  
# sys.setdefaultencoding('utf8')

# PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
PY_GEN_PATH = "E:/data/priv".replace('/', os.sep)
MULTI_API = "https://blockchain.info/multiaddr?active={}"
BALANCE_MULTI_API = "https://blockchain.info/balance?active={}"
SINGLE_API = "https://blockchain.info/rawaddr/{}"
BTC_API_MULTI = "https://chain.api.btc.com/v3/address/{}"
#addr_file = 'D:/data/priv/addr.log'
addr_file = 'E:/data/adrs'
digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
PROCESS_NUM = 50
logger = logging.getLogger('blockchain_api')
logger_req = logging.getLogger('requests')
LOG_FILE = 'blockchain_api.log'
LOG_REQ_FILE = 'requests.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_REQ_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'
LOG_FORMATTER = '%(message)s'
'''
#sock5 proxy
SOCKS5_PROXY_HOST = '127.0.0.1'  # socks 代理IP地址
SOCKS5_PROXY_PORT = 10900  # socks 代理本地端口
default_socket = socket.socket
socks.set_default_proxy(socks.SOCKS5, SOCKS5_PROXY_HOST, SOCKS5_PROXY_PORT)
socket.socket = socks.socksocket
'''
s = requests.Session()


def decode_base58(bc, length):
    n = 0
    for char in bc:
        n = n * 58 + digits58.index(char)
    return n.to_bytes(length, 'big')


def check_bc(bc):
    try:
        bcbytes = decode_base58(bc, 25)
        return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]
    except Exception:
        return False


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
        ACCEPT_ENCODING = "gzip, deflate, br"
        ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9"
        CONNECTION = "keep-alive"
        HOST = "blockchain.info"
        # HOST = "chain.api.btc.com"
        header = {"HOST":HOST, "METHOD":"GET", "User-Agent":UA_LST[random.randrange(0, len(UA_LST))], 'Cache-Control':'no-cache', 'Referer':refer, "Accept":ACCEPT, "Accept-Encoding":ACCEPT_ENCODING, "Accept-Language":ACCEPT_LANGUAGE, "Connection":CONNECTION}
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
            logger_req.error('response_code:{}'.format(str(sc)))
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
    
    logger_req.setLevel(logging.DEBUG)
    handler = logging.FileHandler(os.path.join(PY_GEN_PATH, LOG_REQ_FILE))
    handler.setLevel(logging.DEBUG)
    fmter = logging.Formatter(LOG_REQ_FORMATTER)
    handler.setFormatter(fmter)
    logger_req.addHandler(handler)

    # 控制台打印
    
    console = logging.StreamHandler()
    console.setLevel(level=logging.DEBUG)  # 设置为INFO级别
    console.setFormatter(fmter)
    logger.addHandler(console)
    


def singleGetBalanceInfo():
    logger.info("singleGetBalanceInfo start")
    i = 0
    with open(addr_file, 'r') as f:
        addr = f.readline().strip()
        while addr:
            i = i + 1
            
            single_qry = SINGLE_API.format(str(addr))
            resp_json = get_url(single_qry, single_qry)
            addr_info = json.loads(resp_json)
            balance = addr_info['final_balance']
            logger.info('{} | balance:{}'.format(str(addr), str(balance)))
            addr = f.readline().strip()


def batchGetBalanceInfo():
    # logger.info("batchGetBalanceInfo start")
    param = []
    i = 0
    with open(addr_file, 'r') as f:
        addr = f.readline().strip()
        while addr:
            i = i + 1
            addr_valid = check_bc(addr)
            if addr_valid:
                param.append(addr)
            size = len(param)
            if(size % PROCESS_NUM == 0):
                qry = '|'.join(param)
                # logger.info(qry)
                batch_api = MULTI_API.format(str(qry))
                resp_json = get_url(batch_api, batch_api)
                try:
                    batch_addr_info = json.loads(resp_json)
                    address_lst = batch_addr_info['addresses']
                    for address in address_lst:
                        a = address['address']
                        b = address['final_balance']
                        if int(b) > 0:
                            logger.info('{}|{}'.format(str(a), str(b)))
                        else:
                            logger.info('{}'.format(str(a)))
                    param = []
                except Exception as e:
                    logger.error(qry)
                    # continue
            addr = f.readline().strip()
        logger.info("sum={}".format(str(i)))
        size = len(param)
        if size > 0:
            qry = '|'.join(param)
            batch_api = MULTI_API.format(str(qry))
            resp_json = get_url(batch_api, batch_api)
            try:
                batch_addr_info = json.loads(resp_json)
                address_lst = batch_addr_info['addresses']
                for address in address_lst:
                    a = address['address']
                    b = address['final_balance']
                    if int(b) > 0:
                        logger.info('{}|{}'.format(str(a), str(b)))
                    else:
                        logger.info('{}'.format(str(a)))
                param = []
            except Exception as e:
                logger.error(qry)
            logger.info("size:{}".format(str(size)))


def batchGetBalanceHarvestApi():
    # logger.info("batchGetBalanceInfo start")
    # test_file = "E:/data/priv/test_simple.log"
    param = []
    i = 0
    times = 0
    with open(addr_file, 'r') as f:
        addr = f.readline().strip()
        while addr:
            i = i + 1
            addr_valid = check_bc(addr)
            if addr_valid:
                param.append(addr)
            size = len(param)
            if(size % PROCESS_NUM == 0):
                qry = '|'.join(param)
                # logger.info(qry)
                time.sleep(random.randint(0, 2))
                batch_api = BALANCE_MULTI_API.format(str(qry))
                times = times + 1
                logger.info("call_api1:{}".format(str(times)))
                resp_json = get_url(batch_api, batch_api)
                try:
                    balance_lst_info = json.loads(resp_json)
                    for k, v in balance_lst_info.items():
                        a = k
                        b = v['final_balance']
                        if int(b) > 0:
                            logger.info('{}|b:{}'.format(str(a), str(b)))
#                         else:
#                             logger.info('{}|{}'.format(str(a), str(b)))
                    param = []
                except Exception as e:
                    # logger.error('qry_size:{}|{}'.format(str(len(qry)), qry))
                    for p in param:
                        time.sleep(random.randint(0, 2))
                        batch_api = BALANCE_MULTI_API.format(str(p))
                        times = times + 1
                        logger.info("call_api2:{}".format(str(times)))
                        resp_json = get_url(batch_api, batch_api)
                        try:
                            balance_lst_info = json.loads(resp_json)
                            if balance_lst_info:
                                for k, v in balance_lst_info.items():
                                    a = k
                                    b = v['final_balance']
                                    if int(b) > 0:
                                        logger.info('{}|b:{}'.format(str(a), str(b)))
#                                     else:
#                                         logger.info('{}|{}'.format(str(a), str(b)))
                        except Exception as e:
                            logger.error('error_addr1:{}'.format(str(p)))
                            continue
                    param = []
                    # continue
            addr = f.readline().strip()
        size = len(param)
        if size > 0:
            qry = '|'.join(param)
            batch_api = BALANCE_MULTI_API.format(str(qry))
            time.sleep(random.randint(0, 2))
            resp_json = get_url(batch_api, batch_api)
            times = times + 1
            logger.info("call_api3:{}".format(str(times)))
            try:
                balance_lst_info = json.loads(resp_json)
                for k, v in balance_lst_info.items():
                    a = k
                    b = v['final_balance']
                    if int(b) > 0:
                        logger.info('{}|b:{}'.format(str(a), str(b)))
#                     else:
#                         logger.info('{}|{}'.format(str(a), str(b)))
                param = []
            except Exception as e:
                # logger.error('qry_size:{}|{}'.format(str(len(qry)), qry))
                for p in param:
                    batch_api = BALANCE_MULTI_API.format(str(p))
                    time.sleep(random.randint(0, 2))
                    resp_json = get_url(batch_api, batch_api)
                    times = times + 1
                    logger.info("call_api4:{}".format(str(times)))
                    try:
                        balance_lst_info = json.loads(resp_json)
                        if balance_lst_info:
                            for k, v in balance_lst_info.items():
                                a = k
                                b = v['final_balance']
                                if int(b) > 0:
                                    logger.info('{}|{}'.format(str(a), str(b)))
#                                     else:
#                                         logger.info('{}|{}'.format(str(a), str(b)))
                    except Exception as e:
                        logger.error('error_addr2:{}'.format(str(p)))
                        continue
                param = []


def batchGetBalanceInfoViaBTC():
    # logger.info("batchGetBalanceInfo start")
    param = []
    with open(addr_file, 'r') as f:
        addr = f.readline().strip()
        while addr:
            param.append(addr)
            size = len(param)
            if(size % 10 == 0):
                qry = ','.join(param)
                # logger.info(qry)
                batch_api = BTC_API_MULTI.format(str(qry))
                resp_json = get_url(batch_api, batch_api)
                batch_addr_info = json.loads(resp_json)
                data = batch_addr_info['data']
                for d in data:
                    if d:
                        a = d['address']
                        b = d['balance']
                        if int(b) > 0:
                            logger.info('{}|{}'.format(str(a), str(b)))
#                         else:
#                             logger.info('{}'.format(str(a)))
                param = []
            addr = f.readline().strip()
        size = len(param)
        if size > 0:
            qry = ','.join(param)
            batch_api = BTC_API_MULTI.format(str(qry))
            resp_json = get_url(batch_api, batch_api)
            batch_addr_info = json.loads(resp_json)
            data = batch_addr_info['data']
            for d in data:
                if d:
                    a = d['address']
                    b = d['balance']
                    if int(b) > 0:
                            logger.info('{}|{}'.format(str(a), str(b)))
                    # else:
                    #    logger.info('{}'.format(str(a)))
            param = []


def saveSimpleAddrInfo(pre, post):
    a = []
    digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    for i in digits58:
        a.append(i)
    b = 21
    i = 0
    j = 0
    for x in itertools.product(*[a] * b):
        p = ''.join(x)
        priv = str(pre + str(p) + post).strip()
        i = i + 1
        try:
            canConvert = PrivateKey.from_wif(priv)
        except Exception as e:
            continue


def dev():
    #priv_orig = '5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAbuatmU'
    priv_orig = '5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAbuat'
    size = len(priv_orig)
    digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    a = []
    for i in digits:
        a.append(i)
    b = 2
    for x in itertools.product(*[a] * b):
        p = ''.join(x)
        for i in range(1, size + 1):
            pre = priv_orig[:i]
            post = priv_orig[i:size + 1]
            pk = pre + p + post
            try:
                #logger.info(pk)
                pvk = PrivateKey.from_wif(pk)
                logger.info(pk)
            except Exception as e:
                continue


def test():
    bc = '5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAbuatmU'


if __name__ == '__main__':
    config_logger()
    #dev()
    batchGetBalanceInfo()
    # batchGetBalanceInfoViaBTC()
    #batchGetBalanceInfoBalanceApi()
    '''
    url = 'https://bitinfocharts.com/top-100-richest-bitcoin-addresses-1.html'
    parseBtcAnalyticsPage(url)
    '''
