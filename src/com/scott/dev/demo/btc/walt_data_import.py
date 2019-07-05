# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
gen wallet
@author: user
'''
import os, sys, time
import logging
from importlib import reload
from com.scott.dev.util.mysqlpool import MySQLConnPool
import bitcoin, random
import requests, json

reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
TABLE_NUM = 1000
OLD_TABLE_NUM = 100
logger = logging.getLogger('old_data_import')
LOG_FILE = 'old_data_import.log'
LOG_FORMATTER = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

s = requests.Session()


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


def checkRandAndPrivExists(rand_key, priv_key, addr, tbl):
    select_sql = 'select rand_key from gen_wallet_{} t where t.rand_key= "{}" and priv_key="{}" and addr="{}"'.format(str(tbl), str(rand_key), str(priv_key), str(addr))
    try:
        res = conn.queryone(select_sql)
        if res:
            return True
        else:
            return False
    except Exception as e:
        logger.error('checkRandKeyExists exception' + e)
        return False


def getOldRecord(old):
    logger.info("getOldRecord start")
    select_sql = 'select rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key from gen_wallet_{}'.format(str(old))
    return conn_old.queryall(select_sql)


# 需要将旧表里的数据根据priv_key_hex重新计算一下导入到哪个新表中
def importDataToNew(old, new):
    logger.info("saveWlt start at: {}".format(time.ctime()))
    param = []
    # insert_gen_sql = 'insert into gen_wallet_(rand_key,priv_key,priv_key_type,addr) values(%s,%s,%s,%s)'
    # m = 0
    for old_tbl in range(0, old + 1):
        old_record_lst = getOldRecord(old_tbl)
        len_old_lst = len(old_record_lst)
        for i in range(len_old_lst):
            rand_key = old_record_lst[i][0]
            priv_key = old_record_lst[i][1]
            priv_key_type = old_record_lst[i][2]
            addr = old_record_lst[i][3]
            priv_key_hex = old_record_lst[i][4]
            pub_key = old_record_lst[i][5]
            new_tbl = int(priv_key_hex) % new
        
            isPrivAndAddrExist = checkRandAndPrivExists(rand_key, priv_key, addr, new_tbl)
            if not isPrivAndAddrExist:
                insert_new_sql = 'insert into gen_wallet_{} values(%s,%s,%s,%s,%s,%s)'.format(str(new_tbl))
                param.append([str(rand_key), str(priv_key), priv_key_type, addr, priv_key_hex, pub_key])
                insert_gen_count1 = conn.insertmany(insert_new_sql, param)
                conn.end('commit')
                logger.info('import from table:{} to new table:{} | priv_key_hex:{}'.format(str(old_tbl), str(new_tbl), str(priv_key_hex)))
                param = []
    logger.info("saveWlt end at: {} ".format(time.ctime()))


if __name__ == '__main__':
    conn_old = MySQLConnPool('btc_new_old')
    conn = MySQLConnPool('btc_new')
    config_logger()
    
    importDataToNew(100, 1000)
    
    conn.dispose(1)
    conn_old.dispose(1)
