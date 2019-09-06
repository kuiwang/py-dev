# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
获得top address,
因使用了br编码，引入了 brotli包
@author: user
'''
import os, sys
import logging
import requests
from com.scott.dev.util.mysqlpool import MySQLConnPool
from bs4 import BeautifulSoup 
from importlib import reload
import random
import brotli

reload(sys)  
# sys.setdefaultencoding('utf8')
# https://bitnodes.earn.com/nodes/?page=1&q=Satoshi:0.18.0
PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
NODE_URL_PREFIX = "https://bitnodes.earn.com/nodes/?q={}&page={}"
logger = logging.getLogger('get_nodeip')
LOG_FILE = 'get_nodeip.log'
REFER = "https://bitnodes.earn.com/"
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

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
        HOST = "bitnodes.earn.com"
        header = {"HOST":HOST, "METHOD":"GET", "User-Agent":UA_LST[random.randrange(0, len(UA_LST))], 'Cache-Control':'no-cache', 'Referer':refer, "Accept":ACCEPT, "Accept-Encoding":ACCEPT_ENCODING, "Accept-Language":ACCEPT_LANGUAGE, "Connection":CONNECTION}
        r = s.get(url, headers=header)
        sc = r.status_code
        if sc == 200:
            r.encoding = 'utf-8'
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
    console = logging.StreamHandler()
    console.setLevel(level=logging.DEBUG)  # 设置为INFO级别
    console.setFormatter(fmter)
    logger.addHandler(console)


def parseNodePage(url):
    logger.info("parseNodePage,url:{}".format(url))
    param = []
    insert_sql = 'insert into `btc_node`(ip) values(%s)'
    html = get_url(url, REFER)
    if html is None:
        logger.error('response is null')
        return
    soup = BeautifulSoup(html, "lxml")
    body = soup.find("body")
    tblOne = body.find("table", attrs={"class":"table table-striped table-hover table-condensed"})
    #logger.info(tblOne)
    tr_lst = tblOne.findAll("tr")
    len_tr_lst = len(tr_lst)
    for i in range(1, len_tr_lst):
        td = tr_lst[i].find("td", attrs={"class":"visible-xs"})
        addr = td.find("a").get_text()
        regExsit = checkIpExists(addr)
        if regExsit:
            logger.error('addr:{} already exists'.format(str(addr)))
        else:
            param.append(['sssg_' + str(addr)])
    if len(param) > 0:
        insert_count = conn.insertmany(insert_sql, param)
        conn.end('commit')
        logger.info('parseNodePage |  successful! count:{}'.format(str(insert_count)))
    else:
        logger.error("parseNodePage | param is null!")


def checkIpExists(addr):
    logger.info("checkIpExists | addr:{}".format(str(addr)))
    select_sql = 'select ip from btc_node t where t.ip= "{}" '.format(str(addr))
    try:
        res = conn.queryone(select_sql)
        if res:
            return True
        else:
            return False
    except Exception as e:
        logger.error('checkIpExists exception' + e)
        return False


def saveNodeInfo():
    logger.info("saveNodeInfo start")
    #qry = 'Satoshi:0.18.0'
    #qry = 'Satoshi:0.17.1'
    #qry = 'Satoshi:0.17.0'
    #qry = 'Satoshi:0.16.3'
    #qry = 'Satoshi:0.13.2'
    #qry = 'Satoshi:0.15.1'
    #qry = 'China'
    qry = 'Singapore'
    #qry = 'Japan'
    #qry = 'Korea,%20Republic%20of'
    #qry = 'Hong%20Kong'
    #qry = 'United%20States'
    #qry = 'Germany'
    #qry = 'France'
    #qry = 'Taiwan'
    for i in range(1, 8):
        url = NODE_URL_PREFIX.format(str(qry), str(i))
        parseNodePage(url)


if __name__ == '__main__':
    conn = MySQLConnPool('btc_new')
    config_logger()
    
    saveNodeInfo()
    '''
    url = 'https://bitinfocharts.com/top-100-richest-bitcoin-addresses-1.html'
    parseBtcAnalyticsPage(url)
    '''
    conn.dispose(1)
