# -*- coding:utf-8 -*-

'''
Created on 2019年2月19日

@author: user
'''
import os, sys
import logging
from com.scott.dev.util.mysqlpool import MySQLConnPool
import argparse
import base64
from importlib import reload

reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
logger = logging.getLogger('conv_info_import')
LOG_FILE = 'conv_info_import.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'


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


def init_parser():
    logger.info('start parse arguments')
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url",
                        type=str,
                        dest='url',
                        required=True,
                        help="csv文件位置"
                        )
    return parser


def saveConvInfo(filename):
    param = []
    with open(filename, 'r', encoding='utf-8') as f:
        title = f.readline()
        insert_sql = 'insert into conv_info(`zid`,`ts`,`url`,`refer`,`ip`,`ua`,`conv_id`,`conv_type`,`company_id`,`info`,`user_name`,`phone`,`lds_city` ,`minute` ,`hour`,`day`,`month`,`year`)'
        insert_sql = insert_sql + ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        content = f.readlines()
        num = 0 
        for conv_info in content:
            num = num + 1
            conv_info = conv_info.strip()
            lst_conv_info = conv_info.split('"')
            size = len(lst_conv_info)
            if size == 7:
                zid = lst_conv_info[0].replace('"', '').split(',')[0]
                ts = lst_conv_info[0].replace('"', '').split(',')[1]
                url = lst_conv_info[1].replace('"', '')
                refer = lst_conv_info[3].replace('"', '')
                ip = getip(lst_conv_info[4].replace('"', '').split(',')[1])
                ua = lst_conv_info[5].replace('"', '')
                other = lst_conv_info[6].replace('"', '')
                lst_other = other.split(',')
                conv_id = lst_other[1]
                conv_type = lst_other[2]
                company_id = lst_other[3]
                info = lst_other[4]
                user_name = info.split('|')[1]
                phone = base64.b64decode(info.split('|')[2]).decode()
                lds_city = info.split('|')[3]
                minute = lst_other[5]
                hour = lst_other[6]
                day = lst_other[7]
                month = lst_other[8]
                year = lst_other[9]
                param.append([str(zid), str(ts), str(url), str(refer), str(ip) ,
                                  str(ua), str(conv_id), str(conv_type), str(company_id),
                                  str(info), str(user_name), str(phone), str(lds_city), str(minute), str(hour), str(day),
                                  str(month), str(year)])
                if (num % 1000 == 0):
                    insert_count = conn.insertmany(insert_sql, param)
                    conn.end('commit')
                    logger.info('No:' + str((num / 1000)) + " | save count:" + str(insert_count))
                    param = []
            elif size == 5:
                size_0 = len(lst_conv_info[0].replace('"', '').split(','))
                if size_0 == 3:
                    zid = lst_conv_info[0].replace('"', '').split(',')[0]
                    ts = lst_conv_info[0].replace('"', '').split(',')[1]
                    url = lst_conv_info[1].replace('"', '')
                    refer = 'size-5_refer-null'
                    ip = getip(lst_conv_info[2].replace('"', '').split(',')[2])
                    ua = lst_conv_info[3].replace('"', '')
                    other = lst_conv_info[4].replace('"', '')
                    lst_other = other.split(',')
                    conv_id = lst_other[1]
                    conv_type = lst_other[2]
                    company_id = lst_other[3]
                    info = lst_other[4]
                    user_name = info.split('|')[1]
                    phone = base64.b64decode(info.split('|')[2]).decode()
                    lds_city = info.split('|')[3]
                    minute = lst_other[5]
                    hour = lst_other[6]
                    day = lst_other[7]
                    month = lst_other[8]
                    year = lst_other[9]
                elif size_0 == 4:
                    zid = lst_conv_info[0].replace('"', '').split(',')[0]
                    ts = lst_conv_info[0].replace('"', '').split(',')[1]
                    url = lst_conv_info[0].replace('"', '').split(',')[2]
                    refer = lst_conv_info[1]
                    ip = getip(lst_conv_info[2].replace('"', '').split(',')[1])
                    ua = lst_conv_info[3].replace('"', '')
                    other = lst_conv_info[4].replace('"', '')
                    lst_other = other.split(',')
                    conv_id = lst_other[1]
                    conv_type = lst_other[2]
                    company_id = lst_other[3]
                    info = lst_other[4]
                    user_name = info.split('|')[1]
                    phone = base64.b64decode(info.split('|')[2]).decode()
                    lds_city = info.split('|')[3]
                    minute = lst_other[5]
                    hour = lst_other[6]
                    day = lst_other[7]
                    month = lst_other[8]
                    year = lst_other[9]
                param.append([str(zid), str(ts), str(url), str(refer), str(ip) ,
                                  str(ua), str(conv_id), str(conv_type), str(company_id),
                                  str(info), str(user_name), str(phone), str(lds_city), str(minute), str(hour), str(day),
                                  str(month), str(year)])
                if (num % 1000 == 0):
                    insert_count = conn.insertmany(insert_sql, param)
                    conn.end('commit')
                    logger.info('No:' + str((num / 1000)) + " | save count:" + str(insert_count))
                    param = []
            elif size == 3:
                lst_conv = lst_conv_info[0].replace('"', '').split(',')
                zid = lst_conv[0]
                ts = lst_conv[1]
                url = lst_conv[2]
                refer = lst_conv[3]
                ip = getip(lst_conv[4])
                ua = lst_conv_info[1].replace('"', '')
                other = lst_conv_info[2].replace('"', '')
                lst_other = other.split(',')
                conv_id = lst_other[1]
                conv_type = lst_other[2]
                company_id = lst_other[3]
                info = lst_other[4]
                user_name = info.split('|')[1]
                phone = base64.b64decode(info.split('|')[2]).decode()
                lds_city = info.split('|')[3]
                minute = lst_other[5]
                hour = lst_other[6]
                day = lst_other[7]
                month = lst_other[8]
                year = lst_other[9]
                param.append([str(zid), str(ts), str(url), str(refer), str(ip) ,
                                  str(ua), str(conv_id), str(conv_type), str(company_id),
                                  str(info), str(user_name), str(phone), str(lds_city), str(minute), str(hour), str(day),
                                  str(month), str(year)])
                if (num % 1000 == 0):
                    insert_count = conn.insertmany(insert_sql, param)
                    conn.end('commit')
                    logger.info('No:' + str((num / 1000)) + " | save count:" + str(insert_count))
                    param = []
            else:
                zid = lst_conv_info[0].replace('"', '').split(',')[0]
                ts = lst_conv_info[0].replace('"', '').split(',')[1]
                # logger.error("size:{} | zid:{} | ts:{} | lst_conv_info:{}".format(str(size), zid, str(ts),str(lst_conv_info)))
                for x in range(size):
                    logger.info('lst_conv_info[{}] = {}'.format(str(x), str(lst_conv_info[x])))
        insert_count = conn.insertmany(insert_sql, param)
        conn.end('commit')
        logger.info("save count:" + str(insert_count))


def getip(ip_long):
    ip_long = int(ip_long)
    ip1 = (ip_long >> 24) & 0xff
    ip2 = (ip_long >> 16) & 0xff
    ip3 = (ip_long >> 8) & 0xff
    ip4 = ip_long & 0xff
    return str(ip1) + "." + str(ip2) + "." + str(ip3) + "." + str(ip4)


def getShortId(id_long):
    return id_long & 0xffff


if __name__ == '__main__':
    conn = MySQLConnPool('yc')
    config_logger()
    
    parser = init_parser()
    args = parser.parse_args()
    csv_url = args.url
    
    try:
        saveConvInfo(csv_url)
    except Exception as e:
        logger.error(e)
    
    conn.dispose(1)
