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

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
ADDR_URL_PREFIX = "https://bitinfocharts.com/top-100-richest-bitcoin-addresses-{}.html"
logger = logging.getLogger('top_addr')
LOG_FILE = 'top_addr.log'
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
        HOST = "bitinfocharts.com"
        header = {"HOST":HOST, "METHOD":"GET", "User-Agent":UA_LST[random.randrange(0, len(UA_LST))], 'Cache-Control':'no-cache', 'Referer':refer, "Accept":ACCEPT, "Accept-Encoding":ACCEPT_ENCODING, "Accept-Language":ACCEPT_LANGUAGE, "Connection":CONNECTION}
        r = s.get(url, headers=header)
        if r.status_code == 200:
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
            # return r.text
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


def parseBtcAnalyticsPage(url):
    logger.info("parseBtcAnalyticsPage,url:{}".format(url))
    param = []
    insert_sql = 'insert into btc_top_analytics values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    html = get_url(url, url)
    soup = BeautifulSoup(html, "lxml")
    body = soup.find("body")
    # div_lst = body.findAll('div', attrs={"align":"center"})
    tblOne = body.find("table", attrs={"id":"tblOne"})
    tr_lst = tblOne.find("tbody").findAll("tr")
    tblOne2 = body.find("table", attrs={"id":"tblOne2"})
    #logger.info(tblOne2)
    tr_lst2 = tblOne2.findAll("tr")
    #logger.info(tr_lst2)
    for tr in tr_lst:
        td_lst = tr.findAll("td")
        len_td = len(td_lst)
        num = td_lst[0].get_text()
        # addr = td_lst[1].find("a").get("href").split('/')[-1]
        addr = td_lst[1].find("a").get_text()
        sig_type = ''
        sup = td_lst[1].find("sup")
        if sup is None:
            sig_type = "null_multisignature"
        else:
            sig_type = sup.get("title")
            
        wallet_type = ''
        small_tag = td_lst[1].find("small")
        if small_tag is None:
            wallet_type = "null_wallettype"
        else:
            # wallet_type = small_tag.find("a").get("href").split("/")[-1]
            wallet_type = small_tag.find("a").get_text()
        balance = td_lst[2].get_text()
        balance_btc = balance.split(" ($")[0].split(" BTC")[0].replace(",", '')
        balance_usd = balance.split(" ($")[1].split(" ")[0].replace(",", '')
        btc_rate = td_lst[3].get_text()
        first_in = td_lst[4].get_text()
        last_in = td_lst[5].get_text()
        num_in = td_lst[6].get_text()
        first_out = ''
        last_out = ''
        num_out = ''
        if(len_td == 10):
            first_out = td_lst[7].get_text()
            last_out = td_lst[8].get_text()
            num_out = td_lst[9].get_text()
        
        regExsit = checkExistsInAnalytics(addr)
        if regExsit:
            logger.error('addr:{} already exists'.format(str(addr)))
        else:
            param.append([str(num), str(addr), str(sig_type), str(wallet_type), str(balance), str(balance_btc), str(balance_usd), str(btc_rate),
                          str(first_in), str(last_in), str(num_in), str(first_out), str(last_out), str(num_out)
                          ])
    for tr in tr_lst2:
        td_lst = tr.findAll("td")
        len_td = len(td_lst)
        num = td_lst[0].get_text()
        # addr = td_lst[1].find("a").get("href").split('/')[-1]
        addr = td_lst[1].find("a").get_text()
        sig_type = ''
        sup = td_lst[1].find("sup")
        if sup is None:
            sig_type = "null_multisignature"
        else:
            sig_type = sup.get("title")
            
        wallet_type = ''
        small_tag = td_lst[1].find("small")
        if small_tag is None:
            wallet_type = "null_wallettype"
        else:
            # wallet_type = small_tag.find("a").get("href").split("/")[-1]
            wallet_type = small_tag.find("a").get_text()
        balance = td_lst[2].get_text()
        balance_btc = balance.split(" ($")[0].split(" BTC")[0].replace(",", '')
        balance_usd = balance.split(" ($")[1].split(" ")[0].replace(",", '')
        btc_rate = td_lst[3].get_text()
        first_in = td_lst[4].get_text()
        last_in = td_lst[5].get_text()
        num_in = td_lst[6].get_text()
        first_out = ''
        last_out = ''
        num_out = ''
        if(len_td == 10):
            first_out = td_lst[7].get_text()
            last_out = td_lst[8].get_text()
            num_out = td_lst[9].get_text()
        
        regExsit = checkExistsInAnalytics(addr)
        if regExsit:
            logger.error('addr:{} already exists'.format(str(addr)))
        else:
            param.append([str(num), str(addr), str(sig_type), str(wallet_type), str(balance), str(balance_btc), str(balance_usd), str(btc_rate),
                          str(first_in), str(last_in), str(num_in), str(first_out), str(last_out), str(num_out)
                          ])
    
    if len(param) > 0:
        insert_count = conn.insertmany(insert_sql, param)
        conn.end('commit')
        logger.info('parseBtcAnalyticsPage |  successful! count:{}'.format(str(insert_count)))
    else:
        logger.error("parseBtcAnalyticsPage | param is null!")


def checkExistsInAnalytics(addr):
    logger.info("checkExistsInAnalytics | addr:{}".format(str(addr)))
    select_sql = 'select addr from btc_top_analytics t where t.addr= "{}" '.format(str(addr))
    try:
        res = conn.queryone(select_sql)
        if res:
            return True
        else:
            return False
    except Exception as e:
        logger.error('checkExistsInAnalytics exception' + e)
        return False


def saveBtcAddrAnalyticsInfo():
    logger.info("saveCoinAddrInfo start")
    for i in range(1, 101):
        url = ADDR_URL_PREFIX.format(str(i))
        parseBtcAnalyticsPage(url)


if __name__ == '__main__':
    conn = MySQLConnPool('btc')
    config_logger()
    
    saveBtcAddrAnalyticsInfo()
    '''
    url = 'https://bitinfocharts.com/top-100-richest-bitcoin-addresses-1.html'
    parseBtcAnalyticsPage(url)
    '''
    conn.dispose(1)
