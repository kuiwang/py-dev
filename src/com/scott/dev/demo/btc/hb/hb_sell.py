# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日

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
HB_BIG_SELL_API = 'https://otc-api-sz.eiijo.cn/v1/data/trade-market?coinId=1&currency=1&tradeType=buy&currPage={}&payMethod=0&country=37&blockType=block&online=1&range=0&amount='
HB_NORMAL_SELL_API = 'https://otc-api-sz.eiijo.cn/v1/data/trade-market?coinId=1&currency=1&tradeType=buy&currPage={}&payMethod=0&country=37&blockType=general&online=1&range=0&amount='
# HB_NORMAL =          'https://otc-api-sz.eiijo.cn/v1/data/trade-market?coinId=1&currency=1&tradeType=buy&currPage={}&payMethod=0&country=37&blockType=general&online=1&range=0&amount='
# HB_BIG=              'https://otc-api-sz.eiijo.cn/v1/data/trade-market?coinId=2&currency=1&tradeType=buy&currPage=1&payMethod=0&country=37&blockType=block&online=1&range=0&amount='
logger = logging.getLogger('hb_sell')
LOG_FILE = 'hb_sell.log'
LOG_FORMATTER = '%(message)s'
# LOG_FORMATTER = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

'''
#sock5 proxy
SOCKS5_PROXY_HOST = '127.0.0.1'  # socks 代理IP地址
SOCKS5_PROXY_PORT = 10900  # socks 代理本地端口
default_socket = socket.socket
socks.set_default_proxy(socks.SOCKS5, SOCKS5_PROXY_HOST, SOCKS5_PROXY_PORT)
socket.socket = socks.socksocket
'''
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
        ACCEPT_ENCODING = "gzip, deflate, br"
        ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9"
        CONNECTION = "keep-alive"
        ORIGIN = 'https://c2c.hbg.com'
        # HOST = "chain.api.btc.com"
        header = {"ORIGIN":ORIGIN, "METHOD":"GET", "User-Agent":UA_LST[random.randrange(0, len(UA_LST))], 'Cache-Control':'no-cache', 'Referer':refer, "Accept":ACCEPT, "Accept-Encoding":ACCEPT_ENCODING, "Accept-Language":ACCEPT_LANGUAGE, "Connection":CONNECTION}
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
    
    console = logging.StreamHandler()
    console.setLevel(level=logging.DEBUG)  # 设置为INFO级别
    console.setFormatter(fmter)
    logger.addHandler(console)


def get_hb_big_sell():
    cur_page = 1
    big_sell_api = HB_BIG_SELL_API.format(str(cur_page))
    resp_json = get_url(big_sell_api, big_sell_api)
    try:
        batch_sell_info = json.loads(resp_json)
        total_page = batch_sell_info['totalPage']
        data_lst = batch_sell_info['data']
        for data in data_lst:
            aid = data['id']
            uid = data['uid']
            userName = data['userName']
            merchantLevel = data['merchantLevel']
            coinId = data['coinId']
            currency = data['currency']
            tradeType = data['tradeType']
            blockType = data['blockType']
            payMethod = data['payMethod']
            payTerm = data['payTerm']
            payName = data['payName']
            json_pn = json.loads(payName)
            pay_content = '('
            for pn in json_pn:
                name = pn['bankName']
                btype = pn['bankType']
                b_id = pn['id']
                pay_content = pay_content + str(name) + "_" + str(btype) + "_" + str(b_id) + "+"
            pay_content = pay_content + ")"
            minTradeLimit = data['minTradeLimit']
            maxTradeLimit = data['maxTradeLimit']
            price = data['price']
            tradeCount = data['tradeCount']
            isOnline = data['isOnline']
            tradeMonthTimes = data['tradeMonthTimes']
            orderCompleteRate = data['orderCompleteRate']
            takerLimit = data['takerLimit']
            gmtSort = data['gmtSort']
            logger.info('{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(str(cur_page), str(aid), str(uid),
                    str(userName), str(merchantLevel), str(coinId), str(currency), str(tradeType), str(blockType),
                    str(payMethod), str(payTerm), str(pay_content), str(minTradeLimit), str(maxTradeLimit),
                    str(price), str(tradeCount), str(isOnline), str(tradeMonthTimes), str(orderCompleteRate),
                    str(takerLimit), str(gmtSort)
                    ))
        # cur_page1 = cur_page + 1
        for cur_page1 in range(2, total_page + 1):
        # while int(cur_page1) <= int(total_page):
            big_sell_api = HB_BIG_SELL_API.format(str(cur_page1))
            resp_json = get_url(big_sell_api, big_sell_api)
            try:
                batch_sell_info = json.loads(resp_json)
                total_page = batch_sell_info['totalPage']
                data_lst = batch_sell_info['data']
                for data in data_lst:
                    id = data['id']
                    uid = data['uid']
                    userName = data['userName']
                    merchantLevel = data['merchantLevel']
                    coinId = data['coinId']
                    currency = data['currency']
                    tradeType = data['tradeType']
                    blockType = data['blockType']
                    payMethod = data['payMethod']
                    payTerm = data['payTerm']
                    payName = data['payName']
                    json_pn = json.loads(payName)
                    pay_content = '('
                    for pn in json_pn:
                        name = pn['bankName']
                        btype = pn['bankType']
                        b_id = pn['id']
                        pay_content = pay_content + str(name) + "_" + str(btype) + "_" + str(b_id) + "+"
                    pay_content = pay_content + ")"
                    minTradeLimit = data['minTradeLimit']
                    maxTradeLimit = data['maxTradeLimit']
                    price = data['price']
                    tradeCount = data['tradeCount']
                    isOnline = data['isOnline']
                    tradeMonthTimes = data['tradeMonthTimes']
                    orderCompleteRate = data['orderCompleteRate']
                    takerLimit = data['takerLimit']
                    gmtSort = data['gmtSort']
                    logger.info('{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(str(cur_page1), str(id), str(uid),
                            str(userName), str(merchantLevel), str(coinId), str(currency), str(tradeType), str(blockType),
                            str(payMethod), str(payTerm), str(pay_content), str(minTradeLimit), str(maxTradeLimit),
                            str(price), str(tradeCount), str(isOnline), str(tradeMonthTimes), str(orderCompleteRate),
                            str(takerLimit), str(gmtSort)
                            ))
            except Exception as e:
                logger.info(e)
    except Exception as e:
        logger.error(e)


#
def get_hb_normal_sell():
    cur_page = 1
    big_sell_api = HB_NORMAL_SELL_API.format(str(cur_page))
    resp_json = get_url(big_sell_api, big_sell_api)
    try:
        batch_sell_info = json.loads(resp_json)
        total_page = batch_sell_info['totalPage']
        data_lst = batch_sell_info['data']
        for data in data_lst:
            aid = data['id']
            uid = data['uid']
            userName = data['userName']
            merchantLevel = data['merchantLevel']
            coinId = data['coinId']
            currency = data['currency']
            tradeType = data['tradeType']
            blockType = data['blockType']
            payMethod = data['payMethod']
            payTerm = data['payTerm']
            payName = data['payName']
            json_pn = json.loads(payName)
            pay_content = '('
            for pn in json_pn:
                if 'bankName' in pn:
                    name = pn['bankName'] or 'null-bankname'
                else:
                    name = 'no-bankname'
                btype = pn['bankType'] or 'null-banktype'
                b_id = pn['id'] or 'null-bankid'
                pay_content = pay_content + str(name) + "_" + str(btype) + "_" + str(b_id) + "+"
            pay_content = pay_content + ")"
            minTradeLimit = data['minTradeLimit']
            maxTradeLimit = data['maxTradeLimit']
            price = data['price']
            tradeCount = data['tradeCount']
            isOnline = data['isOnline']
            tradeMonthTimes = data['tradeMonthTimes']
            orderCompleteRate = data['orderCompleteRate']
            takerLimit = data['takerLimit']
            gmtSort = data['gmtSort']
            logger.info('{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(str(cur_page), str(aid), str(uid),
                    str(userName), str(merchantLevel), str(coinId), str(currency), str(tradeType), str(blockType),
                    str(payMethod), str(payTerm), str(pay_content), str(minTradeLimit), str(maxTradeLimit),
                    str(price), str(tradeCount), str(isOnline), str(tradeMonthTimes), str(orderCompleteRate),
                    str(takerLimit), str(gmtSort)
                    ))
        # cur_page1 = cur_page + 1
        # while int(cur_page1) <= int(total_page):
        for cur_page1 in range(2, total_page + 1):
            big_sell_api = HB_NORMAL_SELL_API.format(str(cur_page1))
            resp_json = get_url(big_sell_api, big_sell_api)
            try:
                batch_sell_info = json.loads(resp_json)
                # total_page = batch_sell_info['totalPage']
                data_lst = batch_sell_info['data']
                for data in data_lst:
                    id = data['id']
                    uid = data['uid']
                    userName = data['userName']
                    merchantLevel = data['merchantLevel']
                    coinId = data['coinId']
                    currency = data['currency']
                    tradeType = data['tradeType']
                    blockType = data['blockType']
                    payMethod = data['payMethod']
                    payTerm = data['payTerm']
                    payName = data['payName']
                    json_pn = json.loads(payName)
                    pay_content = '('
                    for pn in json_pn:
                        if 'bankName' in pn:
                            name = pn['bankName'] or 'null-bankname'
                        else:
                            name = 'no-bankname'
                        btype = pn['bankType'] or 'null-banktype'
                        b_id = pn['id'] or 'null-bankid'
                        pay_content = pay_content + str(name) + "_" + str(btype) + "_" + str(b_id) + "+"
                    pay_content = pay_content + ")"
                    minTradeLimit = data['minTradeLimit']
                    maxTradeLimit = data['maxTradeLimit']
                    price = data['price']
                    tradeCount = data['tradeCount']
                    isOnline = data['isOnline']
                    tradeMonthTimes = data['tradeMonthTimes']
                    orderCompleteRate = data['orderCompleteRate']
                    takerLimit = data['takerLimit']
                    gmtSort = data['gmtSort']
                    logger.info('{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'.format(str(cur_page1), str(id), str(uid),
                            str(userName), str(merchantLevel), str(coinId), str(currency), str(tradeType), str(blockType),
                            str(payMethod), str(payTerm), str(pay_content), str(minTradeLimit), str(maxTradeLimit),
                            str(price), str(tradeCount), str(isOnline), str(tradeMonthTimes), str(orderCompleteRate),
                            str(takerLimit), str(gmtSort)
                            ))
                # cur_page1 = cur_page1 + 1
            except Exception as e:
                logger.error(e)
    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    config_logger()
    #get_hb_big_sell()
    #logger.info('#')
    get_hb_normal_sell()
