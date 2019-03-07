# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
导入省市信息
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
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)

logger = logging.getLogger('province_city')
LOG_FILE = 'province_city.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

s = requests.Session()


def get_url(url):
    try:
        UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        REFER = "http://city.bitauto.com/"
        header = {"User-Agent":UA, "Referer":REFER, "method":"GET"}
        r = s.get(url, headers=header)
        r.encoding = "utf-8"
        # logger.info("response in below:\n" + r.text)
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


def parseProvinceAndCityInfo(api):
    resp = get_url(api)
    res_list = resp.split(';')
    #zxs = res_list[0].split('=')[1]  # 直辖市信息
    region = str(res_list[1].split('=')[1])  # 区域信息
    province = res_list[2].split('=')[1]  # 省级信息
    city = res_list[3].split('=')[1]  # 城市信息
    ''''
    logger.info(str(type(zxs)) + " | zxs:{}".format(zxs))
    logger.info(str(type(region)) + " | region:{}".format(region))
    logger.info(str(type(province)) + " | province:{}".format(province))
    logger.info(str(type(city)) + " | city:{}".format(city))
    '''
    return (region, province, city)


def saveRegion(region):
    region = str(region.replace('[[', '').replace(']]', ''))
    region_lst = region.split("],[")
    param = []
    for reg in region_lst:
        reg_id = str(reg.split(',')[0]).strip()
        reg_name = reg.split(',')[1].replace("'", '')
        # logger.info('reg_id:{} | reg_name:{}'.format(reg_id, reg_name))
        regExsit = checkRegionExist(reg_id)
        if regExsit:
            logger.error('region id:{} already exists'.format(str(reg_id)))
        else:
            insert_sql = 'insert into region_list values(%s,%s)'
            param.append([str(reg_id), str(reg_name)])
    if len(param) > 0:
        insert_count = conn.insertmany(insert_sql, param)
        conn.end('commit')
        logger.info('saveRegion |  successful! count:{}'.format(str(insert_count)))
    else:
        logger.info("saveRegion | param is null!")


def checkRegionExist(reg_id):
    select_sql = 'select distinct id from region_list t where t.id= "' + str(reg_id) + '" '
    try:
        res = conn.queryone(select_sql)
        if res:
            return True
        else:
            return False
    except Exception as e:
        logger.error('checkRegionExist exception' + e)
        return False


def saveProvice(province):
    province = str(province.replace('"[', '').replace(']"', ''))
    province_lst = province.split("],[")
    param = []
    for prov in province_lst:
        prov_id = str(prov.split(',')[0]).strip()
        prov_name = prov.split(',')[1].replace("'", '')
        prov_en = prov.split(',')[2].replace("'", '')
        reg_id = prov.split(',')[3].replace("'", '').strip()
        provExsit = checkProvinceExist(prov_id)
        if provExsit:
            logger.error('province id:{} already exists'.format(str(prov_id)))
        else:
            insert_sql = 'insert into province_list values(%s,%s,%s,%s)'
            param.append([str(prov_id), str(prov_name), str(prov_en), str(reg_id)])
    if len(param) > 0:
        insert_count = conn.insertmany(insert_sql, param)
        conn.end('commit')
        logger.info("saveProvice | successful! count:{}".format(str(insert_count)))
    else:
        logger.info("saveProvice | param is null!")


def checkProvinceExist(prov_id):
    select_sql = 'select distinct id from province_list t where t.id= "' + str(prov_id) + '" '
    try:
        res = conn.queryone(select_sql)
        if res:
            return True
        else:
            return False
    except Exception as e:
        logger.error('checkProvinceExist exception' + e)
        return False


def saveCity(city):
    city = str(city.replace('"[', '').replace(']"', ''))
    city_lst = city.split("],[")
    param = []
    for city in city_lst:
        city_id = str(city.split(',')[0]).strip()
        city_name = city.split(',')[1].replace("'", '')
        city_en = city.split(',')[2].replace("'", '')
        unkwn_id = city.split(',')[3].replace("'", '').strip()
        prov_id = city.split(',')[4].replace("'", '').strip()
        reg_id = city.split(',')[5].replace("'", '').strip()
        cityExsit = checkCityExist(city_id)
        if cityExsit:
            logger.error('city id:{} already exists'.format(str(city_id)))
        else:
            insert_sql = 'insert into city_list values(%s,%s,%s,%s,%s,%s)'
            param.append([str(city_id), str(city_name), str(city_en), str(unkwn_id), str(prov_id), str(reg_id)])
    if len(param) > 0:
        insert_count = conn.insertmany(insert_sql, param)
        conn.end('commit')
        logger.info("saveCity | successful! count:{}".format(str(insert_count)))
    else:
        logger.info("saveCity | param is null!")


def checkCityExist(city_id):
    select_sql = 'select distinct id from city_list t where t.id= "' + str(city_id) + '" '
    try:
        res = conn.queryone(select_sql)
        if res:
            return True
        else:
            return False
    except Exception as e:
        logger.error('checkCityExist exception' + e)
        return False


def saveProvinceAndCity(api):
    logger.info("saveProvinceAndCity using:{}".format(api))
    (region, province, city) = parseProvinceAndCityInfo(api)
    
    saveRegion(region)
    saveProvice(province)
    saveCity(city)
    

def init_parser():
    logger.info('start parse arguments')
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url",
                        type=str,
                        dest='api',
                        required=True,
                        help="城市地域信息接口地址"
                        )
    return parser


if __name__ == '__main__':
    conn = MySQLConnPool('yc')
    config_logger()
    
    parser = init_parser()
    args = parser.parse_args()
    api = args.api
    
    saveProvinceAndCity(api)
    # getPhoneLocation('http://cx.shouji.360.cn/phonearea.php?number=', '13839508196')
    conn.dispose(1)
