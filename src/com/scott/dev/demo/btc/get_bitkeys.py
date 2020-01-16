# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
https://bitkeys.work/?page=0
@author: user
'''
import os, sys
import logging
import requests
#from com.scott.dev.util.mysqlpool import MySQLConnPool
from bs4 import BeautifulSoup
#from importlib import reload
import time,random
import brotli

reload(sys) 
sys.setdefaultencoding('utf8')

#PY_GEN_PATH = "E:/data/priv".replace('/', os.sep)
PY_GEN_PATH = "/vagrant/priv".replace('/', os.sep)
ADDR_URL_PREFIX = "https://bitkeys.work/?page={}"
logger = logging.getLogger('get_bitkeys')
LOG_FILE = 'get_bitkeys.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
#LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'
LOG_FORMATTER = '%(message)s'

s = requests.Session()


def get_url(url, refer):
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
        ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        ACCEPT_ENCODING = "gzip, deflate, br"
        ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9"
        CONNECTION = "keep-alive"
        HOST = "bitkeys.work"
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
            logger.error('response code:{}'.format(str(sc)))
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


def parseBitkeysworkPage(page, url):
    logger.info("parseBtc1AddrPage,url:{}".format(url))
    html = get_url(url, url)
    if html is None:
        logger.error('response is null')
        return
    soup = BeautifulSoup(html, "lxml")
    body = soup.find("body")
    main = body.find("main")
    div_center = main.find("div",attrs={"class":"display-area justify-center"})
    div_disp_key_lst = div_center.findAll("div",attrs={"class":"display-keys"})
    
    for div in div_disp_key_lst:
        div_indiv = div.find("div",attrs={"class":"individual-rows"})
        balance = div_indiv.find("span",attrs={"class":"balance"}).get_text()
        addr = div_indiv.find("span",attrs={"class":"keys-with-balance"}).find("a").find("span",attrs={"class":"display-keys-w-balance"}).get_text().strip()
        #log format: page_num|addr|balance
        logger.info("{}|{}|{}".format(str(page), str(addr), str(balance)))


def saveBitkeysworkInfo():
    #logger.info("saveBitkeysworkInfo start")
    i = 0
    for i in range(60320, 100001):
        time.sleep(random.randint(1,3))
        url = ADDR_URL_PREFIX.format(str(i))
        parseBitkeysworkPage(i, url)
        i = i + 1


if __name__ == '__main__':
    config_logger()

    saveBitkeysworkInfo()
