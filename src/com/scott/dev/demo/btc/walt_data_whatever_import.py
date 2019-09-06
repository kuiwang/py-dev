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
import requests, json

reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
TABLE_NUM = 1000
OLD_TABLE_NUM = 100
RECORD_LIMIT = 3000
logger = logging.getLogger('data_import')
LOG_FILE = 'data_import.log'
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


def getAllOldRecord():
    logger.info("getOldRecord start")
    select_sql = 'select rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key from gen_wallet t where priv_key_hex%1000=0'
    return conn.queryall(select_sql)


def getSpecifiedTblOldRecord(tbl_num, tbl_idx, start, limit):
    logger.info("getSpecifiedTblOldRecord start | tbl_num:{},tbl_idx:{}".format(str(tbl_num), str(tbl_idx)))
    select_sql = 'select rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key from gen_wallet t where SUBSTR(t.`priv_key_hex`,LENGTH(t.`priv_key_hex`)-2)%' + str(tbl_num) + '=' + str(tbl_idx) + " limit " + str(start) + " , " + str(limit)
    logger.info('getSpecifiedTblOldRecord sql:{}'.format(str(select_sql)))
    return conn.queryall(select_sql)


def getSpecifiedTblOldRecord2(tbl_num, tbl_idx):
    logger.info("getSpecifiedTblOldRecord start | tbl_num:{},tbl_idx:{}".format(str(tbl_num), str(tbl_idx)))
    select_sql = 'select rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key from gen_wallet1 t where SUBSTR(t.`priv_key_hex`,LENGTH(t.`priv_key_hex`)-2)%' + str(tbl_num) + '=' + str(tbl_idx)
    logger.info('getSpecifiedTblOldRecord sql:{}'.format(str(select_sql)))
    return conn.queryall(select_sql)

'''
def getSpecifiedTblOldRecord2(tbl_num, tbl_idx):
    logger.info("getSpecifiedTblOldRecord start | tbl_num:{},tbl_idx:{}".format(str(tbl_num), str(tbl_idx)))
    select_sql = 'select rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key from gen_wallet t where SUBSTR(t.`priv_key_hex`,LENGTH(t.`priv_key_hex`)-2)%' + str(tbl_num) + '=' + str(tbl_idx)
    logger.info('getSpecifiedTblOldRecord sql:{}'.format(str(select_sql)))
    return conn.queryall(select_sql)
'''

def getOldRecordNum(tbl_num, tbl_idx):
    logger.info("getSpecifiedTblOldRecord start | tbl_num:{},tbl_idx:{}".format(str(tbl_num), str(tbl_idx)))
    select_sql = 'select count(1) as pv from gen_wallet t where SUBSTR(t.`priv_key_hex`,LENGTH(t.`priv_key_hex`)-4)%' + str(tbl_num) + '=' + str(tbl_idx)
    logger.info('getSpecifiedTblOldRecord sql:{}'.format(str(select_sql)))
    return conn.queryone(select_sql)


# 需要将旧表里的数据根据priv_key_hex重新计算一下导入到哪个新表中
def importDataToNew(new):
    logger.info("saveWlt start at: {}".format(time.ctime()))
    param = []
    # insert_gen_sql = 'insert into gen_wallet_(rand_key,priv_key,priv_key_type,addr) values(%s,%s,%s,%s)'
    # m = 0
    old_record_lst = getAllOldRecord()
    len_old_lst = len(old_record_lst)
    logger.info("count:{}".format(str(len_old_lst)))
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
            logger.info('import from table to new table:{} | priv_key_hex:{}'.format(str(new_tbl), str(priv_key_hex)))
            param = []
    logger.info("saveWlt end at: {} ".format(time.ctime()))

# 需要将旧表里的数据根据priv_key_hex重新计算一下导入到哪个新表中


def importDataToNew1(tbl_num):
    logger.info("saveWlt start at: {}".format(time.ctime()))
    param = []
    # insert_gen_sql = 'insert into gen_wallet_(rand_key,priv_key,priv_key_type,addr) values(%s,%s,%s,%s)'
    # m = 0
    # for tbl_idx in range(tbl_num + 1):
    for tbl_idx in range(214, tbl_num + 1):
        total_record_lst = getOldRecordNum(tbl_num, tbl_idx)
        total_record = total_record_lst[0]
        logger.info("table:{} | total:{}".format(str(tbl_idx), str(total_record)))
        
        si = 0
        li = 0
        if total_record < RECORD_LIMIT:
            li = total_record
        else:
            li = RECORD_LIMIT
        
        logger.info('table:{} |  start:{} | limit:{}'.format(str(tbl_idx), str(si), str(li)))
        while ((si + li <= total_record) and (li > 0)):
            
            old_record_lst = getSpecifiedTblOldRecord(tbl_num, tbl_idx, si, li)
            len_old_lst = len(old_record_lst)
            logger.info("tbl_idx:{} | count:{}".format(str(tbl_idx), str(len_old_lst)))
            for i in range(len_old_lst):
                rand_key = old_record_lst[i][0]
                priv_key = old_record_lst[i][1]
                priv_key_type = old_record_lst[i][2]
                addr = old_record_lst[i][3]
                priv_key_hex = old_record_lst[i][4]
                pub_key = old_record_lst[i][5]
                new_tbl = int(priv_key_hex) % tbl_num
                
                # isPrivAndAddrExist = checkRandAndPrivExists(rand_key, priv_key, addr, new_tbl)
                isPrivAndAddrExist = False
                if not isPrivAndAddrExist:
                    insert_new_sql = 'insert into gen_wallet_{} values(%s,%s,%s,%s,%s,%s)'.format(str(new_tbl))
                    param.append([str(rand_key), str(priv_key), priv_key_type, addr, priv_key_hex, pub_key])
                    len_param = len(param)
                    times = 0
                    if((len_param % 10000) == 0):
                        insert_gen_count1 = conn.insertmany(insert_new_sql, param)
                        conn.end('commit')
                        times = times + 1
                        logger.info('times:{} | import to new table:{} | priv_key_hex:{}'.format(str(times), str(new_tbl), str(priv_key_hex)))
                        param = []
            if (len(param) > 0):
                insert_gen_count1 = conn.insertmany(insert_new_sql, param)
                conn.end('commit')
                logger.info('import to new table:{} at last | count:{} '.format(str(tbl_idx), str(insert_gen_count1)))
                param = []
            logger.info("saveWlt end at: {} ".format(time.ctime()))
            #=============================================
            si = si + li
            if (total_record - si) <= RECORD_LIMIT:
                li = total_record - si
            else:
                li = RECORD_LIMIT


def importDataToNew2(tbl_num):
    logger.info("saveWlt start at: {}".format(time.ctime()))
    param = []
    # insert_gen_sql = 'insert into gen_wallet_(rand_key,priv_key,priv_key_type,addr) values(%s,%s,%s,%s)'
    # m = 0
    # for tbl_idx in range(tbl_num + 1):
    for tbl_idx in range(0, tbl_num):
        old_record_lst = getSpecifiedTblOldRecord2(tbl_num, tbl_idx)
        len_old_lst = len(old_record_lst)
        logger.info("tbl_idx:{} | count:{}".format(str(tbl_idx), str(len_old_lst)))
        for i in range(len_old_lst):
            rand_key = old_record_lst[i][0]
            priv_key = old_record_lst[i][1]
            priv_key_type = old_record_lst[i][2]
            addr = old_record_lst[i][3]
            priv_key_hex = old_record_lst[i][4]
            pub_key = old_record_lst[i][5]
            new_tbl = int(priv_key_hex) % tbl_num
            
            # isPrivAndAddrExist = checkRandAndPrivExists(rand_key, priv_key, addr, new_tbl)
            isPrivAndAddrExist = False
            if not isPrivAndAddrExist:
                insert_new_sql = 'insert into gen_wallet_{} values(%s,%s,%s,%s,%s,%s)'.format(str(new_tbl))
                param.append([str(rand_key), str(priv_key), priv_key_type, addr, priv_key_hex, pub_key])
                len_param = len(param)
                times = 0
                if((len_param % 10000) == 0):
                    insert_gen_count1 = conn.insertmany(insert_new_sql, param)
                    conn.end('commit')
                    times = times + 1
                    logger.info('times:{} | import to new table:{} | priv_key_hex:{}'.format(str(times), str(new_tbl), str(priv_key_hex)))
                    param = []
        if (len(param) > 0):
            insert_gen_count1 = conn.insertmany(insert_new_sql, param)
            conn.end('commit')
            logger.info('import to new table:{} at last | count:{} '.format(str(tbl_idx), str(insert_gen_count1)))
            param = []
        logger.info("saveWlt end at: {} ".format(time.ctime()))


def dev_start_limit():
        total_record = 100
        page = int(total_record) / int(RECORD_LIMIT)
        n = 0
        if page > int(int(total_record) / int(RECORD_LIMIT)):
            n = int(page) + 1
        else:
            n = page
        logger.info("n={}".format(n))
        j = 0
        si = 0
        li = 0
        if total_record < RECORD_LIMIT:
            li = total_record
        else:
            li = RECORD_LIMIT
        
        while ((si + li <= total_record) and (li > 0)):
            logger.info('start:{},limit:{}'.format(str(si), str(li)))
            si = si + li
            if (total_record - si) <= RECORD_LIMIT:
                li = total_record - si
            else:
                li = RECORD_LIMIT


if __name__ == '__main__':
    conn = MySQLConnPool('btc_new')
    config_logger()
    
    # importDataToNew(TABLE_NUM)
    
    # importDataToNew1(TABLE_NUM)
    importDataToNew2(TABLE_NUM)
    
    conn.dispose(1)

'''
if __name__ == '__main__':
    config_logger()
    dev_start_limit()
'''
