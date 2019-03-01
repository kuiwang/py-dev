# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
查询手机归属地
@author: user
'''
import os, sys, json
import logging
import requests
from com.scott.dev.util.mysqlpool import MySQLConnPool
from bs4 import BeautifulSoup 
import argparse
from importlib import reload

reload(sys)  
#sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)

logger = logging.getLogger('phone_location')
LOG_FILE = 'get_phone_location.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

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
    except Exception, e:
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


def getPhoneList(startDate, endDate):
    logger.info('getPhoneList between ' + startDate + ' and ' + endDate)
    phoneLst = []
    select_sql = 'select distinct phone from recv_info t where t.report_time between "' + startDate + '" and "' + endDate + '" '
    try:
        res = conn.queryall(select_sql)
        for row in res:
            phoneLst.append(row[0])
        return phoneLst
    except Exception, e:
        logger.error('getPhoneList exception' + e)
        return []


def isPhoneExist(phone):
    size = 0
    size = len(phone)
    if size != 11:
        logger.error("phone length is:" + str(size))
        return False
    logger.info('check phone:' + phone + " exists or not ?")
    select_sql = 'select distinct phone from phone_info t where t.phone= "' + phone + '" '
    try:
        res = conn.queryone(select_sql)
        if res:
            logger.info("phone:" + phone + " exists in database")
            return True
        else:
            return False
    except Exception, e:
        logger.error('isPhoneExist exception' + e)
        return False


def getPhoneLocation(api, phone):
    logger.info("getPhoneLocation from api")
    real_api = api + phone
    phone_info_json = get_url(real_api)
    phoneObj = json.loads(phone_info_json)
    '''
    logger.info(phoneObj)
    logger.info('code:' + str(phoneObj['code']))
    logger.info('province:' + phoneObj['data']['province'])
    logger.info('city:' + phoneObj['data']['city'])
    logger.info('sp:' + phoneObj['data']['sp'])
    '''
    return phoneObj


def savePhone2DB(phone, phoneObj):
    logger.info('savePhone2DB | save phone:' + phone + " | phoneObj:" + json.dumps(phoneObj))
    param = []
    province = phoneObj['data']['province']
    city = phoneObj['data']['city']
    carrier = phoneObj['data']['sp']
    insert_sql = 'insert into phone_info values(%s,%s,%s,%s)'
    param.append([str(phone), str(province), str(city), str(carrier)])
    insert_count = conn.insertmany(insert_sql, param)
    conn.commit()
    logger.info('save phone:' + phone + " and phoneObj " + json.dumps(phoneObj) + " successful! count:" + str(insert_count))


def savePhoneLocation(startDate, endDate, api):
    logger.info("savePhoneLocation here")
    phoneLst = getPhoneList(startDate, endDate)
    size = len(phoneLst)
    if size > 0:
        logger.info('phoneList size:' + str(size))
        for i in range(size):
            phone = phoneLst[i]
            phone_len = len(phone)
            isExist = isPhoneExist(phone)
            if (not isExist) and (phone_len == 11):
                # query from api and save to database
                phoneObj = getPhoneLocation(api, phone)
                savePhone2DB(phone, phoneObj)
        logger.info('savePhoneLocation | phoneListSize' + str(size) + ' | startDate:' + startDate + " | endDate:" + endDate)
    else:
        logger.error('savePhoneLocation | phoneList is null between ' + startDate + ' and ' + endDate)


def init_parser():
    logger.info('start parse arguments')
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start",
                        type=str,
                        dest='startDate',
                        required=True,
                        help="起始日期"
                        )
    parser.add_argument("-e", "--end",
                        type=str,
                        dest='endDate',
                        required=True,
                        help="结束日期"
                        )
    parser.add_argument("-u", "--url",
                        type=str,
                        dest='api',
                        required=True,
                        help="手机归属地API"
                        )
    return parser


if __name__ == '__main__':
    conn = MySQLConnPool('yc')
    config_logger()
    
    parser = init_parser()
    args = parser.parse_args()
    startDate = args.startDate
    endDate = args.endDate
    api = args.api
    
    savePhoneLocation(startDate, endDate, api)
    # getPhoneLocation('http://cx.shouji.360.cn/phonearea.php?number=', '13839508196')
    conn.dispose(1)
