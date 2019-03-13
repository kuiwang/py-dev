# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
获得相似车型信息
@author: user
'''
import os, sys
import logging
import requests
from com.scott.dev.util.mysqlpool import MySQLConnPool
from bs4 import BeautifulSoup 
from importlib import reload
import random

reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
MODEL_PREFIX = "https://car.bitauto.com"
logger = logging.getLogger('chekuan')
LOG_FILE = 'chekuan.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

s = requests.Session()


def get_url(url, refer):
    try:
        UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
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
        CONNECTION = "keep-alive"
        HOST = 'car.bitauto.com'
        header = {"User-Agent":UA_LST[random.randrange(0, len(UA_LST))], 'HOST':HOST, 'Cache-Control':'no-cache', 'Referer':refer, "Accept":ACCEPT, "Accept-Encoding":ACCEPT_ENCODING, "Accept-Language":ACCEPT_LANGUAGE, "Connection":CONNECTION}
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


def getCarModel():
    logger.info("getCarModel start")
    select_sql = 'select pid,url,leads_url from yc_info t where instr(t.pid,"-")=0 order by pid '
    return conn.queryall(select_sql)


def parseCarModelPage(model_id, url):
    param = []
    html = get_url(url, url)
    soup = BeautifulSoup(html, "lxml")
    body = soup.find("body")
    div_container = body.find("div", attrs={'class':'container cartype-section summary'})
    div_row = div_container.find("div", attrs={"class":"row section-layout"})
    div_col = div_row.findAll("div", attrs={"class":"col-xs-3"})
    len_div_col = len(div_col)
    if len_div_col > 1: 
        div_col = div_col[2]
    else:
        div_col = div_col[0]
    div_section_right = div_col.findAll("div", attrs={"class":"section-right"})
    # logger.info("len section_right:" + str(len(div_section_right)))
    len_section_right = len(div_section_right)
    if len_section_right < 2:
        logger.error("貌似这款车没有相似车型啊!model_id:{} | url:{}".format(str(model_id), url))
        return
    div_look_sidebar = div_section_right[1].find("div", attrs={"class":"layout-1 looking-sidebar"})
    if div_look_sidebar is None:
        logger.error("div_look_sidebar is null | model_id:{} | url:{} 没有相似车型".format(str(model_id), url))
        return 
    div_similar = div_look_sidebar.find("div", attrs={"id":"divSimilarSerial"})
    
    dvlst = div_similar.findAll(name="div", attrs={"class":"img-info-layout-vertical"})
    for div in dvlst:
        itemLst = div.find("ul", attrs={"class":'p-list'}).findAll("li")
        similar_url = MODEL_PREFIX + itemLst[0].find('a').get("href")
        similar_name = itemLst[0].find('a').get("title")
        similar_id = itemLst[2].find('a').get("href").split('/')[-2].split('-')[-1]
        
        regExsit = checkSimilarModelExist(model_id, similar_id)
        if regExsit:
            logger.error('model_id:{} | similar_id:{} already exists'.format(str(model_id), str(similar_id)))
        else:
            insert_sql = 'insert into similar_model_info values(%s,%s,%s,%s)'
            param.append([str(model_id), str(similar_id), str(similar_name), str(similar_url)])
    
    if len(param) > 0:
        insert_count = conn.insertmany(insert_sql, param)
        conn.end('commit')
        logger.info('parseCarModelPage |  successful! count:{}'.format(str(insert_count)))
    else:
        logger.error("parseCarModelPage | param is null!")


def checkSimilarModelExist(model_id, similar_id):
    logger.info("checkSimilarModelExist | model_id:{} | similar_id:{}".format(str(model_id), str(similar_id)))
    select_sql = 'select id,similar_id from similar_model_info t where t.id= "{}" and t.similar_id="{}"'.format(str(model_id), str(similar_id))
    try:
        res = conn.queryone(select_sql)
        if res:
            return True
        else:
            return False
    except Exception as e:
        logger.error('checkSimilarModelExist exception' + e)
        return False


def saveLooklikeModelInfo():
    logger.info("saveLooklikeModelInfo start")
    model_lst = getCarModel()
    size = len(model_lst)
    logger.info("car model size:{}".format(size))
    for i in range(size):
        model_id = ''.join(model_lst[i][0])
        model_url = ''.join(model_lst[i][1])
        model_url = model_url[:model_url.index('?')]
        logger.info('{} | model_url:{}'.format(str(model_id), model_url))
        parseCarModelPage(model_id, model_url)


if __name__ == '__main__':
    conn = MySQLConnPool('yc')
    config_logger()
    
    saveLooklikeModelInfo()
    '''
    model_id='2573'
    url = 'http://car.bitauto.com/xinaodia6l/'
    parseCarModelPage(model_id,url)
    '''
    
    conn.dispose(1)
