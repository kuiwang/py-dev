# -*- coding:utf-8 -*-

'''
Created on 2019年2月19日

@author: user
'''
import os, sys, json
import logging
import requests
from com.scott.dev.util.mysqlpool import MySQLConnPool
import argparse
from importlib import reload

reload(sys)  
#sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
logger = logging.getLogger('sendleads')
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
    with open(filename, 'r') as f:
        title = f.readline()
        header = f.readline()
        # logger.info(title)
        # logger.info(header)
        insert_sql = 'insert into send_info(`id`,send_time,`car_info`,`city_name`,`user_name`,`cs_name`,`recv_shop`,`recv_csid` ,`send_csid` ,`send_remark`,`send_shop`,`client_ip`,`send_status`,recv_time,`conv_url` )'
        insert_sql = insert_sql + ' values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        content = f.readlines()
        num = 0 
        abnormal = 0
        for send_info in content:
            num = num + 1
            send_info = send_info.strip().decode('gbk')
            # logger.info(send_info)
            if send_info.find('http') < 0:
                abnormal = abnormal + 1 
                logger.info("abormal info:" + send_info)
                lst_without_conv = send_info.split(',')
                conv_url = lst_without_conv[-1].replace('"', '')
                pid = lst_without_conv[0].replace('"', '')
                send_time = lst_without_conv[1].replace('"', '')
                car_info = lst_without_conv[2].replace('"', '')
                city_name = lst_without_conv[3].replace('"', '')
                user_name = lst_without_conv[4].replace('"', '')
                cs_name = lst_without_conv[5].replace('"', '')
                recv_shop = lst_without_conv[6].replace('"', '')
                recv_csid = lst_without_conv[7].replace('"', '')
                send_csid = lst_without_conv[8].replace('"', '')
                send_remark = lst_without_conv[9].replace('"', '')
                send_shop = lst_without_conv[-5].replace('"', '')
                client_ip = lst_without_conv[-4].replace('"', '')
                send_status = lst_without_conv[-3].replace('"', '')
                recv_time = lst_without_conv[-2].replace('"', '')
                if pid == '':
                    logger.info('without_http_pid_null | send_info:' + send_info)
                param.append([str(pid), str(send_time), str(car_info), str(city_name) ,
                                  str(user_name), str(cs_name), str(recv_shop), str(recv_csid),
                                  str(send_csid), str(send_remark), str(send_shop), str(client_ip),
                                  str(send_status), str(recv_time), str(conv_url)])
                if (num % 1000 == 0):
                    insert_count = conn.insertmany(insert_sql, param)
                    logger.info('No:' + str((num / 1000)) + " | save insert_count:" + str(insert_count))
                    param = []
            else:
                lst_send = send_info.split('http')
                before_conv_url = lst_send[0].replace('"', '')
                lst_without_conv = before_conv_url.split(',')
                conv_url = 'http' + lst_send[1].replace('"', '')
                lst_without_conv = lst_without_conv[:-1]
                pid = lst_without_conv[0].replace('"', '')
                send_time = lst_without_conv[1].replace('"', '')
                car_info = lst_without_conv[2].replace('"', '')
                city_name = lst_without_conv[3].replace('"', '')
                user_name = lst_without_conv[4].replace('"', '')
                cs_name = lst_without_conv[5].replace('"', '')
                recv_shop = lst_without_conv[6].replace('"', '')
                recv_csid = lst_without_conv[7].replace('"', '')
                send_csid = lst_without_conv[8].replace('"', '')
                send_remark = lst_without_conv[9].replace('"', '')
                send_shop = lst_without_conv[-4].replace('"', '')
                client_ip = lst_without_conv[-3].replace('"', '')
                send_status = lst_without_conv[-2].replace('"', '')
                recv_time = lst_without_conv[-1].replace('"', '')
                if pid == '':
                    logger.info('with_http_pid_null | send_info:' + send_info)
                # logger.info(pid + " | " + car_info)
                param.append([str(pid), str(send_time), str(car_info), str(city_name) ,
                                  str(user_name), str(cs_name), str(recv_shop), str(recv_csid),
                                  str(send_csid), str(send_remark), str(send_shop), str(client_ip),
                                  str(send_status), str(recv_time), str(conv_url)])
                if (num % 1000 == 0):
                    insert_count = conn.insertmany(insert_sql, param)
                    conn.commit()
                    logger.info('No:' + str((num / 1000)) + " | save insert_count:" + str(insert_count))
                    param = []
        insert_count = conn.insertmany(insert_sql, param)
        conn.commit()
        logger.info("save insert_count:" + str(insert_count))
        logger.info("abnormal count:" + str(abnormal) + " | total num:" + str(num))


if __name__ == '__main__':
    conn = MySQLConnPool('yc')
    config_logger()
    
    parser = init_parser()
    args = parser.parse_args()
    csv_url = args.url
    
    try:
        saveRecvInfo(csv_url)
    except Exception, e:
        logger.error(e)
    
    conn.dispose(1)
