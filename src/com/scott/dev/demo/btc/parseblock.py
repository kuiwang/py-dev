# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
解析blk.dat文件
@author: user
'''
import os, sys, datetime, time
import logging
from importlib import reload
from blockchain_parser.blockchain import Blockchain, get_files, get_blocks
from blockchain_parser.block import Block
import json

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
        # logger.info(block.__dict__)
        transactions_lst = block.transactions
        logger.info('transactions_lst size:{}'.format(str(len(transactions_lst))))
        for tx in transactions_lst:
            logger.info(tx.__dict__)
#            enums = enumerate(tx.outputs)
#             for no, output in enums:
#                 logger.info('tx:{} | output_no={} | type={} | value={}'.format(str(tx.hash), str(no), str(output.type), str(output.value)))
    end = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    logger.info('end at:{}'.format(str(end)))


if __name__ == '__main__':
    config_logger()
    test_parse_blk()
