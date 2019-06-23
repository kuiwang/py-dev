# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
解析blk.dat文件
@author: user
'''
import os, sys, datetime, time
import logging
from importlib import reload
from com.scott.dev.util.mysqlpool import MySQLConnPool
from blockchain_parser.blockchain import Blockchain, get_files, get_blocks
from blockchain_parser.block import Block
  
# 58 character alphabet used
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)

logger = logging.getLogger('parse_block')
LOG_FILE = 'parse_block.log'
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


def test_parse_blk():
    start = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    logger.info('start at:{}'.format(str(start)))
    blk_path = 'C:/Users/user/AppData/Roaming/Bitcoin/blocks/'
    blk_name = 'blk00000.dat'
    blk_path = os.path.join(blk_path, blk_name)
    logger.info('blkpath:{}'.format(blk_path))
    blk = get_blocks(blk_path)
    # logger.info('blk size:{}'.format(str(len(blk))))
    block_num = 0
    for raw_block in blk:
        block_num = block_num + 1
        logger.info("block_num:{}".format(str(block_num)))
        block = Block(raw_block)
        logger.info(block.__dict__)
        transactions_lst = block.transactions
        logger.info('transactions_lst size:{}'.format(str(len(transactions_lst))))
        for tx in transactions_lst:
            # logger.info(tx.__dict__)
            enums = enumerate(tx.outputs)
            for no, output in enums:
                logger.info('tx:{} | output_no={} | type={} | value={}'.format(str(tx.hash), str(no), str(output.type), str(output.value)))
    end = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    logger.info('end at:{}'.format(str(end)))

def pcurve_dev():
    Pcurve = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1  # 有限域
    x = 0xd061e9c5891f579fd548cfd22ff29f5c642714cc7e7a9215f0071ef5a5723f69
    y = 0x1757b28e31be71f09f24673eed52348e58d53bcfd26f4d96ec6bf1489eab429d
    
    x_res = x ** 3 + 7
    y_res = y ** 2
    
    logger.info('equal ?{}'.format((x_res % Pcurve) == (y_res % Pcurve)))


if __name__ == '__main__':
    conn = MySQLConnPool('btc')
    config_logger()
    test_parse_blk()
