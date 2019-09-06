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

logger = logging.getLogger('imp_ne')
LOG_FILE = 'imp_ne.log'
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
    files = [f for f in files if f.endswith(".txt")]
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
            info_lst = info.replace('"', '').split('----')
            k = info_lst[0]
            v = info_lst[1]
            isExist = checkEmlExists(k)
            # logger.info('name:{},id:{},tbl:{}'.format(str(name), str(ctfId)))
            insert_sql = 'insert into eml_record values(%s,%s)'
            if not isExist:
                param.append([str(k), str(v)])
                if (num % 1000 == 0):
                    insert_count = conn.insertmany(insert_sql, param)
                    logger.info('No:' + str((num / 1000)) + " | save insert_count:" + str(insert_count))
                    param = []
            else:
                logger.error('eml:{} exists'.format(str(k)))
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


def checkEmlExists(eml):
    select_sql = 'select eml from eml_record t where t.eml= "{}" '.format(str(eml))
    try:
        res = conn.queryone(select_sql)
        if res:
            return True
        else:
            return False
    except Exception as e:
        logger.error('checkEmlExists exception' + e)
        return False


if __name__ == '__main__':
    conn = MySQLConnPool('eml')
    config_logger()
    
    parser = init_parser()
    args = parser.parse_args()
    csv_path = args.path
    csv_lst = get_csv_files(csv_path)
    for csv_url in csv_lst:
        # logger.info('csv url:{}'.format(csv_url))
        saveHotelInfo(csv_url)
    
    conn.dispose(1)
