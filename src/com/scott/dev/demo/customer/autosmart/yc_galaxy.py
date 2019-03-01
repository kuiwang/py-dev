# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日

@author: user
'''
import os, sys, json
import logging
import requests
from com.scott.dev.util.mysqlpool import MySQLConnPool
from importlib import reload

reload(sys)
#sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/".replace('/', os.sep)
logger = logging.getLogger('yc_galaxy')
LOG_FILE = 'yiche_galaxy.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

YC_GALAXY_API = "http://galaxy.auto-smart.com/car/queryCarServlet"
s = requests.Session()


def post_url(url, send_data):
    data = None
    try:
        HEADER_UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
        HEADER_CONTENT_TYPE = "application/x-www-form-urlencoded;charset=UTF-8"
        HEADER_ACCEPT = "application/json, text/plain, */*"
        HEADER_ACCEPT_ENCODING = "gzip, deflate"
        header = {"User-Agent":HEADER_UA, "Content-Type":HEADER_CONTENT_TYPE, "Accept":HEADER_ACCEPT, "Accept-Encoding":HEADER_ACCEPT_ENCODING}
        r = s.post(url, data=send_data, headers=header)
        txt = r.text
        logger.info("response:" + txt)
    except Exception as e:
        logger.error(e)
    return txt


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


def queryInfo(type, month_start, month_end):
    import datetime
    ts = datetime.datetime.now()
    logger.info("ts:" + str(ts) + " | type:" + str(type) + " | month_start:" + month_start + " | month_end:" + month_end)
    post_data = {
        "type":type,
        "date": month_start + "," + month_end
    }
    return json.loads(post_url(YC_GALAXY_API, post_data))


def saveBrand(month_start, month_end):
    brand_info = queryInfo(0, month_start, month_end)
    data = brand_info["data"]
    param = []
    for d in data:
        pv = d["pv"]
        name = d["name"]
        id = d["id"]
        param.append([str(id), name, str(pv), str(month_start) + "," + str(month_end)])
    sql = "insert into brand_info(id ,name,pv,month) values(%s,%s,%s,%s)"
    logger.info("insert sql:\n" + sql)
    insert_count = conn.insertmany(sql, param)
    logger.info("save insert_count:" + str(insert_count))


def saveCorp(month_start, month_end):
    corp_info = queryInfo(1, month_start, month_end)
    data = corp_info["data"]
    param = []
    for d in data:
        pv = d["pv"]
        name = d["name"]
        id = d["id"]
        param.append([str(id), name, str(pv), str(month_start) + "," + str(month_end)])
    sql = "insert into corp_info(id ,name,pv,month) values(%s,%s,%s,%s)"
    logger.info("insert sql:\n" + sql)
    insert_count = conn.insertmany(sql, param)
    logger.info("save insert_count:" + str(insert_count))


def saveModel(month_start, month_end):
    model_info = queryInfo(2, month_start, month_end)
    data = model_info["data"]
    param = []
    for d in data:
        pv = d["pv"]
        name = d["name"]
        id = d["id"]
        param.append([str(id), name, str(pv), str(month_start) + "," + str(month_end)])
    sql = "insert into model_info(id ,name,pv,month) values(%s,%s,%s,%s)"
    logger.info("insert sql:\n" + sql)
    insert_count = conn.insertmany(sql, param)
    logger.info("save insert_count:" + str(insert_count))

    
def saveCar(month_start, month_end):
    car_info = queryInfo(3, month_start, month_end)
    data = car_info["data"]
    param = []
    for d in data:
        pv = d["pv"]
        name = d["name"]
        id = d["id"]
        param.append([str(id), name, str(pv), str(month_start) + "," + str(month_end)])
    sql = "insert into car_info(id ,name,pv,month) values(%s,%s,%s,%s)"
    logger.info("insert sql:\n" + sql)
    insert_count = conn.insertmany(sql, param)
    logger.info("save insert_count:" + str(insert_count))


def saveData(year):
    logger.info("saveDate function")
    for m in range(1, 13):
        if m < 10:
            m = "0" + str(m)
        else:
            m = str(m)
        cond_start_month = str(year) + "-" + str(m)
        saveBrand(cond_start_month, cond_start_month)
        saveCorp(cond_start_month, cond_start_month)
        saveModel(cond_start_month, cond_start_month)
        saveCar(cond_start_month, cond_start_month)


if __name__ == '__main__':
    conn = MySQLConnPool('yc')
    config_logger()
    saveData("2018")
    conn.dispose(1)
    # testParseAlbumPageAndSave()
