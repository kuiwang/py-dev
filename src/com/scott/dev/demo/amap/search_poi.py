# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
查询转化信息中手机的归属地
@author: user
'''
import os, sys, json
import logging
import requests
from com.scott.dev.util.mysqlpool import MySQLConnPool
import argparse
from importlib import reload

reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/amap".replace('/', os.sep)

logger = logging.getLogger('poi_search')
LOG_FILE = 'poi_search.log'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

AMAP_POI_SEARCH_API = 'https://restapi.amap.com/v3/place/text?key={}&keywords={}'
s = requests.Session()


def get_url(url):
    try:
        UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
        ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        ACCEPT_ENCODING = "gzip, deflate"
        ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9"
        CONNECTION = "keep-alive"
        header = {"User-Agent":UA, "Accept":ACCEPT, "Accept-Encoding":ACCEPT_ENCODING, "Accept-Language":ACCEPT_LANGUAGE, "Connection":CONNECTION}
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


def getPhoneList():
    logger.info('getPhoneList in convinfo')
    phoneLst = []
    select_sql = 'select distinct phone from poi_info t'
    try:
        res = conn.queryall(select_sql)
        for row in res:
            phoneLst.append(row[0])
        return phoneLst
    except Exception as e:
        logger.error('getPhoneList exception' + e)
        return []


def isPhoneExist(phone):
    size = 0
    size = len(phone)
    if size != 11:
        logger.error("phone length is:" + str(size))
        return False
    logger.info('check phone:' + phone + " exists or not ?")
    select_sql = 'select distinct phone from poi_info t where t.phone= "' + phone + '" '
    try:
        res = conn.queryone(select_sql)
        if res:
            logger.info("phone:" + phone + " exists in database")
            return True
        else:
            return False
    except Exception as e:
        logger.error('isPhoneExist exception' + e)
        return False


def getPhoneLocation(phone):
    logger.info("getPhoneLocation from api")
    real_api = PHONE_API.format(phone)
    phone_info_json = get_url(real_api)
    phoneObj = json.loads(phone_info_json)
    
    return phoneObj


def savePhone2DB(phone, phoneObj):
    logger.info('savePhone2DB | save phone:' + phone + " | phoneObj:" + json.dumps(phoneObj))
    param = []
    code = str(phoneObj['code'])
    if code == '0':
        province = phoneObj['data']['province']
        city = phoneObj['data']['city']
        carrier = phoneObj['data']['sp']
    else:
        province = 'province_{}'.format(str(code))
        city = 'city_{}'.format(str(code))
        carrier = 'carrier_{}'.format(str(code))
    insert_sql = 'insert into poi_info values(%s,%s,%s,%s)'
    param.append([str(phone), str(province), str(city), str(carrier)])
    insert_count = conn.insertmany(insert_sql, param)
    conn.end('commit')
    logger.info('save phone:' + phone + " and phoneObj " + json.dumps(phoneObj) + " successful! count:" + str(insert_count))


def savePoiInfo():
    logger.info("savePoiInfo here")


def init_parser():
    logger.info('start parse arguments')
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key",
                        type=str,
                        dest='apikey',
                        required=True,
                        help="api_key"
                        )
    return parser


if __name__ == '__main__':
    conn = MySQLConnPool('amap_dev')
    config_logger()
    
    parser = init_parser()
    args = parser.parse_args()
    key = args.apikey
    print(key)
    
    # AMAP_POI_SEARCH_API = AMAP_POI_SEARCH_API.format(*args, **kwargs)
    
    savePoiInfo()
    
    conn.dispose(1)
