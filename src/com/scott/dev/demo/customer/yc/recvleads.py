# -*- coding:utf-8 -*-

'''
Created on 2019年2月19日

@author: user
'''
import os, sys, json
import base64
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
        cur = conn.cursor()
        insert_sql = 'insert into `recv_info` (`id`,`report_time`,`ad_id`,`cs_id`,`car_id`,car_name,user_name,bs64_phone,phone,province,city,4sname,4scode,replaceorder,`user_info`,`client_ip`,`shops`,`code`,`status`,`leads_url` )'
        insert_sql = insert_sql + ' values(%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        content = f.readlines()
        num = 0 
        abnormal = 0
        for recv_info in content:
            num = num + 1
            # recv_info = recv_info.strip().decode('gbk').replace('"', '')
            recv_info = recv_info.strip().decode('gbk')
            name_4s = ''
            code_4s = ''
            replaceorder = ''
            car_name = ''
            user_name = ''
            bs64_phone = ''
            real_phone = ''
            province = ''
            city = ''
            dict_usr_info = ''
            # logger.info(recv_info)
            if recv_info.find('http://') < 0:
                abnormal = abnormal + 1 
                logger.info("abormal info:" + recv_info)
                
                left_big_idx = recv_info.find("{")  # 从左开始找第一个{
                right_big_idx = recv_info.rfind("}")  # 从右开始找第一个}
                user_info = recv_info[left_big_idx:right_big_idx + 1]
                # logger.info('abnormal_usr_info:' + user_info)
                if user_info == '':
                    logger.info('user info is null and recv_info:' + recv_info)
                    continue
                try:
                    tmp_usr_info = user_info.replace(':""""', ':"no-value"').replace('"""",', '"",').replace('""', '"')
                    dict_usr_info = json.loads(tmp_usr_info)
                    # dict_usr_info = json.loads(user_info)
                except Exception , e:
                    logger.error('json exception')
                if dict_usr_info.has_key('car_name'): 
                    name_4s = dict_usr_info['car_name']
                else:
                    name_4s = 'None_car_name'
                if dict_usr_info.has_key('name'): 
                    user_name = dict_usr_info['name']
                else:
                    user_name = 'None_car_name'
                if dict_usr_info.has_key('phone'): 
                    bs64_phone = dict_usr_info['phone']
                    real_phone = base64.b64decode(bs64_phone).decode()
                else:
                    bs64_phone = 'None_car_name'
                    real_phone = 'real_phone'
                if dict_usr_info.has_key('province'): 
                    province = dict_usr_info['province']
                else:
                    province = 'None_province'
                if dict_usr_info.has_key('city'): 
                    city = dict_usr_info['city']
                else:
                    city = 'None_city'
                if dict_usr_info.has_key('4sname'): 
                    name_4s = dict_usr_info['4sname']
                else:
                    name_4s = 'None_4sname'
                if dict_usr_info.has_key('4scode'):
                    code_4s = dict_usr_info['4scode']
                else:
                    code_4s = 'None_4scode'
                if dict_usr_info.has_key('replaceorder'):
                    replaceorder = dict_usr_info['replaceorder']
                else:
                    replaceorder = 'None_replaceorder'
                
                lst_recv_info = recv_info.split(user_info)
                lst_before_usr_info = recv_info.split(user_info)[0].replace('"', '').split(',')
                pid = lst_before_usr_info[0]
                report_time = lst_before_usr_info[1]
                ad_id = lst_before_usr_info[2]
                cs_id = lst_before_usr_info[3]
                car_id = lst_before_usr_info[4]
                
                lst_after_usr_info = recv_info.split(user_info)[1].replace('"', '').split(',')
                client_ip = lst_after_usr_info[1]
                shops = lst_after_usr_info[2]
                code = lst_after_usr_info[3]
                status = lst_after_usr_info[4]
                leads_url = lst_after_usr_info[5]
                
                param.append([str(pid), str(report_time), str(ad_id), str(cs_id) ,
                                  str(car_id), str(car_name), str(user_name), str(bs64_phone), str(real_phone),
                                  str(province), str(city), str(name_4s), str(code_4s), str(replaceorder),
                                  str(user_info), str(client_ip), str(shops),
                                  str(code), str(status), str(leads_url)])
                if (num % 1000 == 0):
                    insert_count = cur.executemany(insert_sql, param)
                    conn.commit()
                    logger.info('No:' + str((num / 1000)) + " | save insert_count:" + str(insert_count))
                    param = []
            else:
                lst_send = recv_info.split('http://')
                before_leads_url = lst_send[0]
                
                lst_without_leads = before_leads_url.split(',')
                left_big_idx = before_leads_url.find("{")
                right_big_idx = before_leads_url.rfind("}")
                user_info = before_leads_url[left_big_idx:right_big_idx + 1]
                logger.info('usr_info:' + user_info)
                if user_info == '':
                    logger.info('user info is null and recv_info:' + recv_info)
                    continue
                try:
                    tmp_usr_info = user_info.replace(':""""', ':"no-value"').replace('"""",', '"",').replace('""', '"')
                    dict_usr_info = json.loads(tmp_usr_info.replace('""', '"'))
                except Exception , e:
                    logger.error('json exception')
                if dict_usr_info.has_key('car_name'): 
                    name_4s = dict_usr_info['car_name']
                else:
                    name_4s = 'None_car_name'
                # car_name = dict_usr_info['car']
                if dict_usr_info.has_key('name'): 
                    user_name = dict_usr_info['name']
                else:
                    user_name = 'None_car_name'
                if dict_usr_info.has_key('phone'): 
                    bs64_phone = dict_usr_info['phone']
                    real_phone = base64.b64decode(bs64_phone).decode()
                else:
                    bs64_phone = 'None_car_name'
                    real_phone = 'real_phone'
                if dict_usr_info.has_key('province'): 
                    province = dict_usr_info['province']
                else:
                    province = 'None_province'
                if dict_usr_info.has_key('city'): 
                    city = dict_usr_info['city']
                else:
                    city = 'None_city'
                if dict_usr_info.has_key('4sname'): 
                    name_4s = dict_usr_info['4sname']
                else:
                    name_4s = 'None_4sname'
                if dict_usr_info.has_key('4scode'):
                    code_4s = dict_usr_info['4scode']
                else:
                    code_4s = 'None_4scode'
                if dict_usr_info.has_key('replaceorder'):
                    replaceorder = dict_usr_info['replaceorder']
                else:
                    replaceorder = 'None_replaceorder'
                
                leads_url = 'http://' + lst_send[1]
                lst_before_usr_info = before_leads_url.split(user_info)[0].replace('"', '').split(',')
                lst_without_leads = lst_without_leads[:-1]
                # 表字段信息
                pid = lst_before_usr_info[0]
                report_time = lst_before_usr_info[1]
                ad_id = lst_before_usr_info[2]
                cs_id = lst_before_usr_info[3]
                car_id = lst_before_usr_info[4]
                
                lst_after_usr_info = before_leads_url.split(user_info)[1].replace('"', '').split(',')
                client_ip = lst_after_usr_info[1]
                shops = lst_after_usr_info[2]
                code = lst_after_usr_info[3]
                status = lst_after_usr_info[4] + "," + lst_after_usr_info[5]
                
                # logger.info(pid + " | " + ad_id)
                param.append([str(pid), str(report_time), str(ad_id), str(cs_id) ,
                                  str(car_id), str(car_name), str(user_name), str(bs64_phone), str(real_phone),
                                  str(province), str(city), str(name_4s), str(code_4s), str(replaceorder),
                                  str(user_info), str(client_ip), str(shops),
                                  str(code), str(status), str(leads_url)])
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
''
