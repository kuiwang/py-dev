# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
解析blk.dat文件
@author: user
'''
import os, sys, datetime, time
import logging, json
#from importlib import reload
from com.scott.dev.util.mysqlpool import MySQLConnPool
from blockchain_parser.blockchain import Blockchain, get_files, get_blocks
from blockchain_parser.block import Block

  
# 58 character alphabet used

#reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)

logger = logging.getLogger('parse_block_dev')
LOG_FILE = 'parse_block_dev.log'
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


def get_blk_files(path):
    """
    Given the path to the .bitcoin directory, returns the sorted list of .blk
    files contained in that directory
    """
    files = os.listdir(path)
    files = [f for f in files if f.startswith("blk") and f.endswith(".dat")]
    files = map(lambda x: os.path.join(path, x), files)
    return sorted(files)


def test_parse_blk():
    start = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    logger.info('start at:{}'.format(str(start)))
    blk_path = 'E:/data/btc/blocks'
    blk_index_path=os.path.join(blk_path,'/index')
    blockchain = Blockchain(blk_path)
    blocks = blockchain.get_unordered_blocks()
    #blocks = blockchain.get_ordered_blocks(blk_index_path)
    
    cur_blk_num = 0
    param = []
    
    for block in blocks:
        # logger.info('block name:{}'.format(block.get))
        # if cur_blk_num >= 50000:
        #    break
        tbl = cur_blk_num % 10000
        
        insert_gen_sql = 'insert into tx_output_addr_' + str(tbl) + '(addr) values(%s)'
        
        blk_hash = block.hash
        logger.info('cur_blk_num:{} | table:{} | block_hash:{} start'.format(str(cur_blk_num), str(tbl), str(blk_hash)))
        blk_header = block.header
        blk_height = block.height
        blk_hex = block.hex
        blk_n_transactions = block.n_transactions
        blk_size = len(blk_hex)
        blk_transactions = block.transactions
        
        # header:
        bits = blk_header.bits
        difficulty = blk_header.difficulty
        merkle_root = blk_header.merkle_root
        nonce = blk_header.nonce
        prev_block_hash = blk_header.previous_block_hash
        ts = blk_header.timestamp
        version = blk_header.version
        
        for tx in blk_transactions:
            tx_hash = tx.hash
            tx_hex = tx.hex
            tx_inputs = tx.inputs
            tx_locktime = tx.locktime
            tx_n_inputs = tx.n_inputs
            tx_n_outputs = tx.n_outputs
            tx_outputs = tx.outputs
            tx_size = tx.size
            tx_version = tx.version
            enums_inputs = enumerate(tx_inputs)
            
            enums_outputs = enumerate(tx_outputs)
            for no, output in enums_outputs:
                try:
                    addr_lst = output.addresses
                    for addr in addr_lst:
                        address = str(addr.address).strip()
                        isExist = checkOutputAddrExists(address, tbl)
                        if not isExist :
                            cnt = param.count([address])
                            if not cnt:
                                param.append([address])
                        # else:
                            # logger.error("addr:{} exists!".format(str(address)))
                except Exception as e:
                    logger.error('cur_blk_num:{} | block_hash:{} error occurs'.format(str(cur_blk_num), str(blk_hash)))
                    continue
        len_param = len(param)
        if (len_param > 0):
            insert_gen_count = conn.insertmany(insert_gen_sql, param)
            end = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
            logger.info("cur_blk_num:{} | table:{} | block_hash:{} | end at:{} | addr_count:{}".format(str(cur_blk_num), str(tbl), str(blk_hash), str(end), str(insert_gen_count)))
            conn.end('commit')
            param = []
        cur_blk_num = cur_blk_num + 1
    end = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    logger.info('end at:{}'.format(str(end)))


def checkOutputAddrExists(addr, tbl):
    select_sql = 'select addr  from tx_output_addr_{} t where addr="{}" '.format(str(tbl), str(addr))
    try:
        res = conn.queryone(select_sql)
        if  res :
            return True
        else:
            return False
    except Exception as e:
        logger.error('checkOutputAddrExists exception' + e)
        return False


if __name__ == '__main__':
    conn = MySQLConnPool('btc_new')
    config_logger()
    
    test_parse_blk()
    
    conn.dispose(1)
