# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
查询IP归属地
@author: user
'''
import os, sys, json
import logging
import requests
from com.scott.dev.util.mysqlpool import MySQLConnPool
import argparse
import time,random
from importlib import reload

reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)

logger = logging.getLogger('ip_location')
LOG_FILE = 'get_ip_location.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

s = requests.Session()

IP_API = "http://ip.taobao.com/service/getIpInfo.php?ip={}"


def get_url(url):
    try:
        UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
        ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        ACCEPT_ENCODING = "gzip, deflate"
        ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9"
        CONNECTION = "keep-alive"
        HOST = "ip.taobao.com"
        header = {"User-Agent":UA, "Accept":ACCEPT, 'HOST':HOST, "Accept-Encoding":ACCEPT_ENCODING, "Accept-Language":ACCEPT_LANGUAGE, "Connection":CONNECTION}
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


def getIPList():
    logger.info('getIPList here')
    ipLst = []
    select_sql = 'select distinct ip from conv_info t '
    try:
        res = conn.queryall(select_sql)
        for row in res:
            ipLst.append(row[0])
        return ipLst
    except Exception as e:
        logger.error('getIPList exception' + e)
        return []


def isIPExist(ip):
    logger.info("isIPExist:({})".format(str(ip)))
    size = 0
    # logger.info('check ip:' + ip + " exists or not ?")
    select_sql = 'select distinct ip from ip_info_tb t where t.ip= "' + ip + '" '
    try:
        res = conn.queryone(select_sql)
        if res:
            logger.info("ip:" + ip + " exists in database")
            return True
        else:
            return False
    except Exception as e:
        logger.error('isIPExist exception' + e)
        return False


def getIPLocation(ip):
    real_api = IP_API.format(str(ip))
    logger.info("getIPLocation from api:{}".format(real_api))
    ip_info_json = get_url(real_api)
    ipObj = json.loads(ip_info_json)
    
    return ipObj


def saveIP2DB(ip, ipObj):
    logger.info('saveIP2DB | save ip:' + ip)
    param = []
    status = str(ipObj['code'])
    if status == '0':
        ip = ipObj['data']['ip']
        country = ipObj['data']['country']
        region = ipObj['data']['region']
        city = ipObj['data']['city']
        isp = ipObj['data']['isp']
        country_id = ipObj['data']['country_id']
        region_id = ipObj['data']['region_id']
        city_id = ipObj['data']['city_id']
        isp_id = ipObj['data']['isp_id']

        insert_sql = 'insert into ip_info_tb values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        param.append([str(ip), str(country), str(region), str(city), str(isp), str(country_id), str(region_id),
                      str(city_id), str(isp_id)])
        insert_count = conn.insertmany(insert_sql, param)
        conn.end('commit')
        logger.info('save ip:' + ip + " successful! count:" + str(insert_count))


def saveIPLocation():
    logger.info("saveIPLocation here")
    ipLst = getIPList()
    size = len(ipLst)
    if size > 0:
        logger.info('phoneList size:' + str(size))
        for i in range(size):
            ip = ipLst[i]
            isExist = isIPExist(ip)
            if (not isExist):
                slp = random.randint(10,12);
                logger.info("sleep {}s before query ip api".format(str(slp)))
                time.sleep(slp)
                ipObj = getIPLocation(ip)
                saveIP2DB(ip, ipObj)
        logger.info('saveIPLocation | ipListSize' + str(size))
    else:
        logger.error('saveIPLocation | ipList is null ')


def init_parser():
    logger.info('start parse arguments')
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start",
                        type=str,
                        dest='startDate',
                        required=False,
                        help="起始日期"
                        )
    parser.add_argument("-e", "--end",
                        type=str,
                        dest='endDate',
                        required=False,
                        help="结束日期"
                        )
    return parser


if __name__ == '__main__':
    conn = MySQLConnPool('yc')
    config_logger()
    
    parser = init_parser()
    args = parser.parse_args()
    
    saveIPLocation()
    conn.dispose(1)
