# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
处理csv文件
@author: user
'''
import os, sys
import logging
from importlib import reload
from com.scott.dev.util.mysqlpool import MySQLConnPool
import argparse

reload(sys)  

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)

logger = logging.getLogger('csv_op')
LOG_FILE = 'csv_op.log'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'
TABLE_NUM = 10


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


def get_csv_files(path):
    files = os.listdir(path)
    files = [f for f in files if f.endswith(".csv")]
    files = map(lambda x: os.path.join(path, x), files)
    return sorted(files)


def saveHotelInfo(filename):
    param = []
    logger.info('process file:{}'.format(filename))
    with open(filename, encoding='utf-8', mode='r') as f:
        header = f.readline()
        
        content = f.readlines()
        num = 0 
        for info in content:
            num = num + 1
            info = info.strip()
            logger.info(info)
            info_lst = info.replace('"', '').split(',')
            name = info_lst[0]
            # logger.info(name)
            card_no = info_lst[1]
            descriot = info_lst[2]
            ctfTp = info_lst[3]
            ctfId = info_lst[4]
            gender = info_lst[5]
            birth = info_lst[6]
            addr = info_lst[7]
            fzip = info_lst[8]
            dirty = info_lst[9]
            dist1 = info_lst[10]
            dist2 = info_lst[11]
            dist3 = info_lst[12]
            dist4 = info_lst[13]
            dist5 = info_lst[14]
            dist6 = info_lst[15]
            firstNm = info_lst[16]
            lastNm = info_lst[17]
            duty = info_lst[18]
            mobile = info_lst[19]
            tel = info_lst[20]
            fax = info_lst[21]
            email = info_lst[22]
            nation = info_lst[23]
            taste = info_lst[24]
            edu = info_lst[25]
            company = info_lst[26]
            ctel = info_lst[27]
            caddr = info_lst[28]
            czip = info_lst[29]
            family = info_lst[30]
            version = info_lst[31]
            f_id = info_lst[32]
            isExist = checkIDExists(ctfId)
            # logger.info('name:{},id:{},tbl:{}'.format(str(name), str(ctfId)))
            insert_sql = 'insert into hotel_record values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            if not isExist:
                param.append([
                    str(name), str(card_no), str(descriot), str(ctfTp), str(ctfId), str(gender), str(birth), str(addr), str(fzip),
                    str(dirty), str(dist1), str(dist2), str(dist3), str(dist4), str(dist5), str(dist6), str(firstNm), str(lastNm),
                    str(duty), str(mobile), str(tel), str(fax), str(email), str(nation), str(taste), str(edu), str(company),
                    str(ctel), str(caddr), str(czip), str(family), str(version), str(f_id)
                ])
                if (num % 1000 == 0):
                    insert_count = conn.insertmany(insert_sql, param)
                    logger.info('No:' + str((num / 1000)) + " | save insert_count:" + str(insert_count))
                    param = []
            else:
                logger.error('ctfid:{} exists'.format(str(ctfId)))
        insert_count = conn.insertmany(insert_sql, param)
        conn.commit()
        logger.info("save insert_count:" + str(insert_count))
        logger.info("total num:" + str(num))


def init_parser():
    logger.info('start parse arguments')
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path",
                        type=str,
                        dest='path',
                        required=True,
                        help="csv文件位置"
                        )
    return parser


def checkIDExists(fid):
    select_sql = 'select ctfid from hotel_record t where t.ctfid= "{}" '.format(str(fid))
    try:
        res = conn.queryone(select_sql)
        if res:
            return True
        else:
            return False
    except Exception as e:
        logger.error('checkIDExists exception' + e)
        return False


if __name__ == '__main__':
    conn = MySQLConnPool('hotel')
    config_logger()
    
    parser = init_parser()
    args = parser.parse_args()
    csv_path = args.path
    csv_lst = get_csv_files(csv_path)
    for csv_url in csv_lst:
        # logger.info('csv url:{}'.format(csv_url))
        saveHotelInfo(csv_url)
    
    conn.dispose(1)
