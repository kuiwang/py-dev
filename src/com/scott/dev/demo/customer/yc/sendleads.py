# -*- coding:utf-8 -*-

'''
Created on 2019年2月19日

@author: user
'''
import os, sys, json
import csv, codecs
import logging
import requests
import mysqlutils
import argparse

reload(sys)  
sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
YC_INDEX_FILE = "bitauto_index.xml"
YC_FEED_LOC = "bitauto_loc.xml"
logger = logging.getLogger('bitauto_feed')
LOG_FILE = 'bitauto_autoleads.log'
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

def saveRecvInfo(filename):
    param = []
    cur = conn.cursor()
    with open(filename, 'r') as f:
        title = f.readline()
        header = f.readline()
        # logger.info(title)
        # logger.info(header)
        cur = conn.cursor()
        insert_sql = 'insert into send_info(`id`,send_time,`car_info`,`city_name`,`user_name`,`cs_name`,`recv_shop`,`recv_csid` ,`send_csid` ,`send_remark`,`send_shop`,`client_ip`,`send_status`,recv_time,`conv_url` )'
        insert_sql = insert_sql + ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        content = f.readlines()
        num = 0 
        abnormal = 0
        for send_info in content:
            num = num + 1
            send_info = send_info.strip().decode('gbk').replace('"', '')
            # logger.info(send_info)
            if send_info.find('http') < 0:
                abnormal = abnormal + 1 
                logger.info("abormal info:" + send_info)
                lst_without_conv = send_info.split(',')
                conv_url = lst_without_conv[14]
                pid = lst_without_conv[0]
                send_time = lst_without_conv[1]
                car_info = lst_without_conv[2]
                city_name = lst_without_conv[3]
                user_name = lst_without_conv[4]
                cs_name = lst_without_conv[5]
                recv_shop = lst_without_conv[6]
                recv_csid = lst_without_conv[7]
                send_csid = lst_without_conv[8]
                send_remark = lst_without_conv[9]
                send_shop = lst_without_conv[10]
                client_ip = lst_without_conv[11]
                send_status = lst_without_conv[12]
                recv_time = lst_without_conv[13]
                param.append([str(pid), str(send_time), str(car_info), str(city_name) ,
                                  str(user_name), str(cs_name), str(recv_shop), str(recv_csid),
                                  str(send_csid), str(send_remark), str(send_shop), str(client_ip),
                                  str(send_status), str(recv_time), str(conv_url)])
                if (num % 1000 == 0):
                    insert_count = cur.executemany(insert_sql, param)
                    conn.commit()
                    logger.info('No:' + str((num / 1000)) + " | save insert_count:" + str(insert_count))
                    param = []
            else:
                lst_send = send_info.split('http')
                before_conv_url = lst_send[0]
                lst_without_conv = before_conv_url.split(',')
                conv_url = 'http' + lst_send[1]
                lst_without_conv = lst_without_conv[:-1]
                size = len(lst_without_conv)
                pid = lst_without_conv[0]
                send_time = lst_without_conv[1]
                car_info = lst_without_conv[2]
                city_name = lst_without_conv[3]
                user_name = lst_without_conv[4]
                cs_name = lst_without_conv[5]
                recv_shop = lst_without_conv[6]
                recv_csid = lst_without_conv[7]
                send_csid = lst_without_conv[8]
                send_remark = lst_without_conv[9]
                send_shop = lst_without_conv[10]
                client_ip = lst_without_conv[11]
                send_status = lst_without_conv[12]
                recv_time = lst_without_conv[13]
                # logger.info(pid + " | " + car_info)
                param.append([str(pid), str(send_time), str(car_info), str(city_name) ,
                                  str(user_name), str(cs_name), str(recv_shop), str(recv_csid),
                                  str(send_csid), str(send_remark), str(send_shop), str(client_ip),
                                  str(send_status), str(recv_time), str(conv_url)])
                if (num % 1000 == 0):
                    insert_count = cur.executemany(insert_sql, param)
                    conn.commit()
                    logger.info('No:' + str((num / 1000)) + " | save insert_count:" + str(insert_count))
                    param = []
        insert_count = cur.executemany(insert_sql, param)
        conn.commit()
        logger.info("save insert_count:" + str(insert_count))
        logger.info("abnormal count:" + str(abnormal) + " | total num:" + str(num))
        cur.close()


if __name__ == '__main__':
    conn = mysqlutils.connect_mysql()
    config_logger()
    
    parser = init_parser()
    args = parser.parse_args()
    csv_url = args.url
    
    try:
        saveRecvInfo(csv_url)
    except Exception, e:
        logger.error(e)
    
    conn.close()
