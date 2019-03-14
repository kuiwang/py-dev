# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
获得车款信息
@author: user
'''
import os, sys
import logging
import requests
from com.scott.dev.util.mysqlpool import MySQLConnPool
from bs4 import BeautifulSoup 
from importlib import reload

reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
DEALER_PREFIX = "https://dealer.bitauto.com/zuidijia/nb{}"
logger = logging.getLogger('chekuan')
LOG_FILE = 'chekuan.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

s = requests.Session()


def get_url(url, refer):
    try:
        UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
        ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        ACCEPT_ENCODING = "gzip, deflate, br"
        ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9"
        CONNECTION = "keep-alive"
        header = {"User-Agent":UA, 'Cache-Control':'no-cache', 'Referer':refer, "Accept":ACCEPT, "Accept-Encoding":ACCEPT_ENCODING, "Accept-Language":ACCEPT_LANGUAGE, "Connection":CONNECTION}
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
  getSimilarCarModelfo("getCarModel startgetSimilarCarModelct_sql = 'select pid,url,leads_url from yc_info t where instr(t.pid,"-")=0 order by pid '
    return conn.queryall(select_sql)


def parseLeadPage(model_id, leads_url, refer):
    param = []
    html = get_url(leads_url, refer)
    soup = BeautifulSoup(html, "lxml")
    ul_lst = soup.find("body").find("div", attrs={'id':'line-box'}).find('div', attrs={'class':'col-xs-12'}).find('form', attrs={'id':'form1'}).find('div', attrs={'class':'input-group'}).find('div', attrs={'id':'divSelectCar'}).find('div', attrs={'id':'divSelectCarGroup'}).find('ul', attrs={'id':'dropCar'})
    li = ul_lst.findAll(name="li")
    for item in li:
        car_id = item.get('data_id')
        car_name = item.get('data_name')
        car_name_seo = item.get('data_name_seo')
        ''''
        a = item.find("a")
        href = a.get('href')
        name = a.find("img").get("alt")
        id = href.split("/")[-1]
        '''
        regExsit = checkSimilarModelExist(model_id, car_id)
        if regExsit:
            logger.error('model_id:{} | car_id:{} already exists'.format(str(model_id), str(car_id)))
        else:
            insert_sql = 'insert into model_car_info values(%s,%s,%s,%s)'
            param.append([str(model_id), str(car_id), str(car_name), str(car_name_seo)])
    
    if len(param) > 0:
        insert_count = conn.insertmany(insert_sql, param)
        conn.end('commit')
        logger.info('parseLeadPage |  successful! count:{}'.format(str(insert_count)))
    else:
        logger.error("parseLeadPage | param is null!")


def checkSimilarModelExist(model_id, similar_id):
    logger.info("checkSimilarModelExist | model_id:{} | similar_id:{}".format(str(model_id), str(similar_id)))
    select_sql = 'select model_id,similar_id from model_car_info t where t.model_id= "{}" and t.similar_id="{}"'.format(str(model_id), str(similar_id))
    try:
        res = conn.queryone(select_sql)
        if res:
            return True
        else:
            return False
    except Exception as e:
        logger.error('checkSimilarModelExist exception' + e)
        return False


def saveCarInfo():
    logger.info("saveCarInfo start")
    model_lst = getCarModel()
   getSimilarCarModel(model_lst)
    logger.info("size:{}".format(size))
    for i in range(size):
        # logger.info('model[{}] = {}'.format(str(i),str(''.join(model_lst[i]))))
        model_id = ''.join(model_lst[i][0])
        model_url = ''.join(model_lst[i][1])
        model_url = model_url[:model_url.index('?')]
        lds_url = ''.join(model_lst[i][2])
        lds_url = lds_url[:lds_url.index('?')]
        # leads_url = DEALER_PREFIX.format(model_id)
        logger.info('{} | model_url:{} | qry_lds:{}'.format(str(model_id), model_url, lds_url))
        parseLeadPage(model_id, lds_url, model_url)


if __name__ == '__main__':
    conn = MySQLConnPool('yc')
    config_logger()
    
    saveCarInfo()
    '''
    model_id = '2573'
    leads_url = 'https://dealer.bitauto.com/zuidijia/nb2573'
    refer = 'http://car.bitauto.com/xinaodia6l/'
    parseLeadPage(model_id, leads_url, refer)
    '''
    conn.dispose(1)
