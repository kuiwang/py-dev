# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
获得车款信息
@author: user
'''
import os, sys, datetime, random
# import json #标准库无法解决json中key不包含双引号的情况,去掉了
import demjson
import logging
import requests
from com.scott.dev.util.mysqlpool import MySQLConnPool
from importlib import reload
from urllib.parse import quote, unquote, urlencode
from com.scott.dev.bigdata.feeds.issue.util.test_function import datetime_test
import threading

reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
API_CITY_PREFIX = "https://dealer.bitauto.com/zuidijia/ashx/getDealers.ashx?car={}&city={}&recordDR=1"
DEALER_PREFIX = "https://dealer.bitauto.com/zuidijia/nb{}"
logger = logging.getLogger('get4s')
LOG_FILE = 'get4s.log'
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


def getModelCarInfo():
    logger.info("getModelCarInfo start")
    select_sql = 'select model_id,car_id from model_car_info t where is_op="0" order by model_id  '
    return conn.queryall(select_sql)


def getCityInfo():
    logger.info("getCityInfo start")
    select_sql = 'select distinct id from city_list t order by id '
    return conn.queryall(select_sql)


def check4sExist(id_4s):
    # logger.info("check4sExist | 4s_id:{}".format(str(id_4s)))
    select_sql = 'select id from 4s_list t where t.id= "{}"'.format(str(id_4s))
    try:
        res = conn.queryone(select_sql)
        if res:
            return True
        else:
            return False
    except Exception as e:
        logger.error('check4sExist exception' + e)
        return False


def checkCarCity4sExist(carid, cityid, id_4s):
    # logger.info("checkCarCity4sExist | carid:{} | cityid:{} | 4sid:{}".format(str(carid), str(cityid), str(id_4s)))
    select_sql = 'select car_id,city_id,4s_id from car_city_4s t where t.car_id= "{}" and t.city_id="{}" and t.4s_id="{}" '.format(str(carid), str(cityid), str(id_4s))
    try:
        res = conn.queryone(select_sql)
        if res:
            return True
        else:
            return False
    except Exception as e:
        logger.error('checkCarCity4sExist exception' + e)
        return False


def get4SInfo(model_id, car_id, city_id):
    refer = DEALER_PREFIX.format(str(model_id))
    url = API_CITY_PREFIX.format(str(car_id), str(city_id))
    # logger.info('get4SInfo | model_id:{} | car_id:{} | city_id:{} | url:{} | refer:{}'.format(str(model_id), str(car_id), str(city_id), str(url), str(refer)))
    try:
        resp_json = get_url(url, refer)
    except Exception as e:
        logger.error("get_url exception | url:{} | refer:{}".format(url, refer))
    # logger.info('resp_json:\n{}'.format(resp_json))
    if str(resp_json).find('carid') <= 0:
        logger.error('出错了,resp_json is:{}'.format(str(resp_json)))
        return
    resp_arr = demjson.decode(resp_json, 'utf8')
    size = len(resp_arr)
    for i in range(size):
        param_4s = []
        param_carcity4s = []
        info_dict = resp_arr[i]
        carid = info_dict['carid'] or 'carid_none'
        cityid = info_dict['cityid'] or 'cityid_none'
        # cityName = info_dict['cityName'] or 'cityName_none'
        locid = info_dict['locid'] or 'locid_none'
        data = info_dict['data']
        if cityid == locid: 
            same = 1  # 城市ID和locId一致时,则4s店是位于查询城市一个地域的,否则是其他地域也售卖该城市的
        else:
            same = 0
        len_data = len(data)
        for j in range(len_data):
            cur_data = data[j]
            id_4s = cur_data['id'] or '4s_id_none'
            name = unquote(cur_data['name']) or '4s_name_none'
            ad = unquote(cur_data['ad']) or '4s_ad_none'
            te = unquote(cur_data['te']) or '4s_te_none'
            if 'cityAreaName' in cur_data:
                cityAreaName = unquote(cur_data['cityAreaName']) 
            else:
                cityAreaName = '4s_cityAreaName_none'
            cn = cur_data['cn'] or '4s_cn_none'
            pn = cur_data['pn'] or '4s_pn_none'
            is4sExist = check4sExist(id_4s)
            '''
            if is4sExist:
                logger.error("4s_id:{} already exist ".format(str(id_4s)))
            else:
                insert_4s_sql = 'insert into 4s_list(id,name,address,tel,area,city,prov) values(%s,%s,%s,%s,%s,%s,%s) '
                param_4s.append([str(id_4s), str(name), str(ad), str(te), str(cityAreaName), str(cn), str(pn)])
            '''
            if not is4sExist:
                insert_4s_sql = 'insert into 4s_list(id,name,address,tel,area,city,prov) values(%s,%s,%s,%s,%s,%s,%s) '
                param_4s.append([str(id_4s), str(name), str(ad), str(te), str(cityAreaName), str(cn), str(pn)])
            
            isCarCity4sExist = checkCarCity4sExist(carid, cityid, id_4s)
            '''
            if isCarCity4sExist:
                logger.error("car_id:{} | city_id:{} | 4s_id:{} already exist ".format(str(carid), str(cityid), str(id_4s)))
            else:
                insert_carcity_sql = 'insert into car_city_4s(car_id ,city_id ,4s_id , is_same) values(%s,%s,%s,%s) '
                param_carcity4s.append([str(carid), str(cityid), str(id_4s), str(same)])
            '''
            if not isCarCity4sExist:
                insert_carcity_sql = 'insert into car_city_4s(car_id ,city_id ,4s_id , is_same) values(%s,%s,%s,%s) '
                param_carcity4s.append([str(carid), str(cityid), str(id_4s), str(same)])
    if len(param_4s) > 0:
        insert_4s_count = conn.insertmany(insert_4s_sql, param_4s)
        conn.end('commit')
        logger.info('save 4s_info successful! count:{}'.format(str(insert_4s_count)))
    '''
    else:
        logger.error("get4SInfo | param_4s is null!")
    '''
    if len(param_carcity4s) > 0:
        insert_carcity4s_count = conn.insertmany(insert_carcity_sql, param_carcity4s)
        conn.end('commit')
        logger.info('save car_city_4s_info successful! count:{}'.format(str(insert_carcity4s_count)))
    '''
    else:
        logger.error("get4SInfo | param_carcity4s is null!")
    '''


def save4sInfo():
    starttime = datetime.datetime.now()
    logger.info("save4sInfo start at:{}".format(str(starttime)))
    car_lst = getModelCarInfo()
    city_lst = getCityInfo()
    car_size = len(car_lst)
    city_size = len(city_lst)
    logger.info("car_size:{} | city_size:{} | will execute:{}".format(str(car_size), str(city_size), str(car_size * city_size)))
    count = 0
    for i in range(car_size):
        model_id = ''.join(car_lst[i][0])
        car_id = ''.join(car_lst[i][1])
        for j in range(city_size):
            count = count + 1
            slp_time = random.randint(0, 2)
            logger.info('times:{} | sleep {}s'.format(str(count), str(slp_time)))
            city_id = ''.join(city_lst[j])
            # time.sleep(slp_time)
            get4SInfo(model_id, car_id, city_id)
        update_sql = 'update model_car_info t set is_op="1" where model_id="' + str(model_id) + '" and car_id="' + str(car_id) + '"  '
        cnt = conn.update(update_sql)
        logger.info("update model_id:{} | car_id:{} ,count:{}".format(str(model_id), str(car_id), str(cnt)))
        conn.end("commit")
    endtime = datetime.datetime.now()
    logger.info("save4sInfo end at:{} | elapse:{}".format(str(endtime), str(endtime - starttime)))


if __name__ == '__main__':
    conn = MySQLConnPool('yc')
    config_logger()
    
    save4sInfo()
    '''
    #model_id:1605 | car_id:15629 | city_id:912 | url:https://dealer.bitauto.com/zuidijia/ashx/getDealers.ashx?car=15629&city=912&recordDR=1
    api = 'https://dealer.bitauto.com/zuidijia/ashx/getDealers.ashx?car=15629&city=912&recordDR=1'
    car_id = '15629'
    city_id = '912'
    model_id = '1605'
    get4SInfo(model_id, car_id, city_id)
    
    car_id = '16507'
    city_id = '912'
    model_id = '2770'
    get4SInfo(model_id, car_id, city_id)
    '''
    conn.dispose(1)
