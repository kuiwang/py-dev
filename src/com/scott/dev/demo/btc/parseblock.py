# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
解析blk.dat文件
@author: user
'''
import os, sys, datetime, time
import logging,json
from importlib import reload
from com.scott.dev.util.mysqlpool import MySQLConnPool
from blockchain_parser.blockchain import Blockchain, get_files, get_blocks
from blockchain_parser.block import Block
  
# 58 character alphabet used

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


def get_blk_files(path):
    """
    Given the path to the .bitcoin directory, returns the sorted list of .blk
    files contained in that directory
    """
    files = os.listdir(path)
    files = [f for f in files if f.startswith("blk") and f.endswith(".dat")]
    files = map(lambda x: os.path.join(path, x), files)
    return sorted(files)


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


# generate walt
def saveBlock(num):
    logger.info("saveWlt start at: {}".format(time.ctime()))
    param = []
    error_param = []
    # insert_gen_sql = 'insert into gen_wallet_(rand_key,priv_key,priv_key_type,addr) values(%s,%s,%s,%s)'
    for i in range(1, num + 1):
        insert_gen_sql = 'insert into gen_wallet_' + str(tbl_idx) + '(rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key) values(%s,%s,%s,%s,%s,%s)'
        insert_err_sql = 'insert into error_info(rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key,tbl_idx,save_time) values(%s,%s,%s,%s,%s,%s,%s,now())'
        try:
            param.append([str(rand_key), str(wif_encoded_private_key), 'wif_normal', normal_addr, priv_key_hex, uncompress_pub])
            param.append([str(rand_key), str(wif_compressed_private_key), 'wif_compressed', compress_addr, priv_key_hex, compress_pub])
            insert_gen_count1 = conn.insertmany(insert_gen_sql, param)
            conn.end('commit')
            # logger.info('i={}'.format(str(i)))
            param = []
        except Exception as e:
            error_param.append([str(rand_key), str(wif_encoded_private_key), 'wif_normal', normal_addr, priv_key_hex, uncompress_pub, str(tbl_idx)])
            error_param.append([str(rand_key), str(wif_compressed_private_key), 'wif_compressed', compress_addr, priv_key_hex, compress_pub, str(tbl_idx)])
            error_count = conn.insertmany(insert_err_sql, error_param)
            logger.error(e)
            logger.error('error count:{} | rand_key:{} | table:{}'.format(str(error_count), str(rand_key), str(tbl_idx)))
            conn.end('commit')
            error_param = []
        
    if len(param) > 0:
        insert_gen_count = conn.insertmany(insert_gen_sql, param)
        conn.end('commit')
        logger.info('saveWlt successful at last! count:{}'.format(str(insert_gen_count)))
    logger.info("saveWlt end at: {} ".format(time.ctime()))

def test_parse_blk():
    start = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    logger.info('start at:{}'.format(str(start)))
    blk_path = 'C:/Users/user/AppData/Roaming/Bitcoin/blocks/'
    # blk_name = 'blk01000.dat'
    blk_name = 'blk00001.dat'
    blk_path = os.path.join(blk_path, blk_name)
    logger.info('blkpath:{}'.format(blk_path))
    blocks = get_blocks(blk_path)
    # logger.info('blk size:{}'.format(str(len(blk))))
    cur_blk_num = 0
    for raw_block in blocks:
        if cur_blk_num >= 1:
            break
        cur_blk_num = cur_blk_num + 1
        block = Block(raw_block)
        #json.dumps(block)
        #logger.info(block.__dict__)
        blk_hash = block.hash
        blk_header = block.header
        blk_height = block.height
        blk_hex = block.hex
        blk_n_transactions = block.n_transactions
        blk_size = len(blk_hex)
        blk_transactions = block.transactions
        
        #header:
        bits = blk_header.bits
        difficulty = blk_header.difficulty
        merkle_root = blk_header.merkle_root
        nonce = blk_header.nonce
        prev_block_hash = blk_header.previous_block_hash
        ts=blk_header.timestamp
        version = blk_header.version
        
        logger.info('transactions_lst size:{}'.format(str(len(blk_transactions))))
        for tx in blk_transactions:
            # logger.info(tx.__dict__)
            tx_hash = tx.hash
            tx_hex = tx.hex
            tx_inputs = tx.inputs
            tx_locktime = tx.locktime
            tx_n_inputs = tx.n_inputs
            tx_n_outputs = tx.n_outputs
            tx_outputs = tx.outputs
            tx_size = tx.size
            tx_version = tx.version
            
            '''
            enums = enumerate(tx.outputs)
            for no, output in enums:
                logger.info('tx:{} | output_no={} | type={} | value={}'.format(str(tx.hash), str(no), str(output.type), str(output.value)))
            '''
    end = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
    logger.info('end at:{}'.format(str(end)))


if __name__ == '__main__':
    conn = MySQLConnPool('btc')
    config_logger()
    test_parse_blk()
