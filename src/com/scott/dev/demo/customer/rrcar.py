# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日

@author: user
'''
import os, sys, json
import hashlib
import logging
import requests
from importlib import reload

reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/".replace('/', os.sep)
logger = logging.getLogger('renrencar')
LOG_FILE = 'renrencar.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

s = requests.Session()


def post_url(url, send_data):
    data = None
    try:
        header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"}
        r = s.post(url, data=send_data, headers=header)
        txt = r.text
        logger.info("response:" + txt)
    except Exception, e:
        logger.error(e)
    return data


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


def rrc_c1():
    api = "http://123.56.187.192:2872/v1/clue/saler"
    token = "JD8NF6SLIAF9JDS7NDSY"
    # ts = int(time.time())
    ts = 1529925605
    logger.info("current timestamp:" + str(ts))
    # sign = md5(user_info + token + time)
    m2 = hashlib.md5()
    
    name = "dev_name"
    mobile = "13801234567"
    city = "北京"
    brand = "未知"
    series = "未知"
    model = "未知"
    kilometer = 10
    licensed_date_year = 2010
    is_operation = ""
    seat_number = ""
    is_accidented = ""
    '''user_info = {
        "name":name,
        "mobile":mobile,
        "city":city,
        "brand":brand,
        "series":series,
        "model":model,
        "kilometer":kilometer,
        "licensed_date_year":licensed_date_year,
        "is_operation":is_operation,
        "seat_number":seat_number,
        "is_accidented":is_accidented
    }'''
    user_info = {
        'name' : 'song',
        'mobile' : '13310008620',
        'city' : '北京',
        'brand' : '奥迪',
        'series' : '奥迪A4L',
        'model' : '2018款 30周年版 40 TFSI 时尚版',
        'kilometer' : '1.2',
        'licensed_date_year' : '2012',
        'is_operation' : '',
        'is_accidented' : ''
    }
    json_user_info = json.dumps(user_info).encode()
    logger.info("user_info:" + json_user_info)
    # unsign_data = json_user_info + token + str(ts)
    data_list = [json_user_info, token, str(ts)]
    unsign_data = ''.join(data_list)
    logger.info("before md5 ,data:" + unsign_data)
    m2.update(unsign_data)
    sign = m2.hexdigest()
    logger.info("sign:" + sign)
    post_data = {
        "token":token,
        "time": str(ts),
        "sign":sign,
        "data":user_info
    }
    json_post_data = json.dumps(post_data).encode("utf-8")
    logger.info("post_data:" + str(json_post_data))
    # post_url(api, post_data)


if __name__ == '__main__':
    config_logger()
    rrc_c1()
