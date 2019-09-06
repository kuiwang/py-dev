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
from multiprocessing import Process

reload(sys)
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
TABLE_NUM = 1000
logger = logging.getLogger('walt_whatever_gen2')
LOG_FILE = 'walt_whatever_gen2.log'
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


def get_address():
    # 生成随机私钥
    valid_private_key = False
    while not valid_private_key:
        private_key = bitcoin.random_key()
        decoded_private_key = bitcoin.decode_privkey(private_key, 'hex')
        valid_private_key = 0 < decoded_private_key < bitcoin.N
        
        # 将私钥转换为WIF格式
        wif_enc_priv = bitcoin.encode_privkey(decoded_private_key, 'wif')
        
        dec_enc_priv = bitcoin.encode_privkey(decoded_private_key, 'decimal')
        bin_enc_priv = bitcoin.encode_privkey(decoded_private_key, 'bin')
        bin_compress_enc_priv = bitcoin.encode_privkey(decoded_private_key, 'bin_compressed')
        
        hex_compress_enc_priv = bitcoin.encode_privkey(decoded_private_key, 'hex_compressed')
        wif_compress_enc_priv = bitcoin.encode_privkey(decoded_private_key, 'wif_compressed')

        # 添加后缀'01'以指示压缩的私钥
        compressed_priv = private_key + '01'

        # 从压缩私钥生成WIF格式（WIF压缩）
        wif_compressed_priv = bitcoin.encode_privkey(bitcoin.decode_privkey(compressed_priv, 'hex'), 'wif')
        wif_compressed_private_key_direct = bitcoin.encode_privkey(compressed_priv, 'wif')

        # 将EC生成器G与私钥相乘以获得公钥点
        public_key = bitcoin.fast_multiply(bitcoin.G, decoded_private_key)

        # 编码为十六进制，前缀为04
        hex_encoded_public_key = bitcoin.encode_pubkey(public_key, 'hex')  # uncompressed public key
        
        decimal_enc_pub = bitcoin.encode_pubkey(public_key, 'decimal')
        bin_enc_public_key = bitcoin.encode_pubkey(public_key, 'bin')
        bin_compress_encoded_pub = bitcoin.encode_pubkey(public_key, 'bin_compressed')
        bin_electrum_enc_pub = bitcoin.encode_pubkey(public_key, 'bin_electrum')
        hex_electrum_enc_pub = bitcoin.encode_pubkey(public_key, 'hex_electrum')
        
        # 压缩公钥，根据y是偶数还是奇数调整前缀
        (public_key_x, public_key_y) = public_key
        if (public_key_y % 2) == 0:
            compressed_prefix = '02'
        else:
            compressed_prefix = '03'
        
        # 压缩后的公钥  compressed_public_key
        hex_compress_pub = compressed_prefix + bitcoin.encode(public_key_x, 16)

        # 从公钥生成比特币地址
        normal_addr = bitcoin.pubkey_to_address(public_key)

        # 从压缩公钥生成压缩比特币地址
        compress_addr = bitcoin.pubkey_to_address(hex_compress_pub.encode('utf-8'))
        
        return wif_enc_priv, normal_addr, wif_compressed_priv, compress_addr, private_key, hex_encoded_public_key, hex_compress_pub


def checkRandAndPrivExists(rand_key, priv_key, addr, tbl):
    select_sql = 'select rand_key from gen_wallet1 t where t.rand_key= "{}" and priv_key="{}" and addr="{}"'.format(str(rand_key), str(priv_key), str(addr))
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
def saveWlt(num):
    logger.info("saveWlt start at: {}".format(time.ctime()))
    param = []
    error_param = []
    times = 0
    
    for i in range(1, num + 1):
        address_give = get_address()
        wif_encoded_private_key = address_give[0] 
        normal_addr = address_give[1]
        wif_compressed_private_key = address_give[2]
        compress_addr = address_give[3]
        rand_key = address_give[4]
        uncompress_pub = address_give[5]
        compress_pub = address_give[6]
        priv_key_hex = bitcoin.decode_privkey(rand_key, 'hex')
        insert_gen_sql = 'insert into gen_wallet1(rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key) values(%s,%s,%s,%s,%s,%s)'
        insert_err_sql = 'insert into error_info(rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key,save_time) values(%s,%s,%s,%s,%s,%s,now())'
        try:
            param.append([str(rand_key), str(wif_encoded_private_key), 'wif_normal', normal_addr, priv_key_hex, uncompress_pub])
            param.append([str(rand_key), str(wif_compressed_private_key), 'wif_compressed', compress_addr, priv_key_hex, compress_pub])
            size = len(param)
            if ((size % 10000) == 0):
                insert_gen_count1 = conn.insertmany(insert_gen_sql, param)
                conn.end('commit')
                times = times + 1
                logger.info('times:{} | count:{}'.format(str(times), str(insert_gen_count1)))
                param = []
        except Exception as e:
            error_param.append([str(rand_key), str(wif_encoded_private_key), 'wif_normal', normal_addr, priv_key_hex, uncompress_pub])
            error_param.append([str(rand_key), str(wif_compressed_private_key), 'wif_compressed', compress_addr, priv_key_hex, compress_pub])
            error_count = conn.insertmany(insert_err_sql, error_param)
            logger.error(e)
            logger.error('error count:{} | rand_key:{} '.format(str(error_count), str(rand_key)))
            conn.end('commit')
            error_param = []
    if len(param) > 0:
        insert_gen_count = conn.insertmany(insert_gen_sql, param)
        conn.end('commit')
        logger.info('saveWlt successful at last! count:{}'.format(str(insert_gen_count)))
    logger.info("saveWlt end at: {} ".format(time.ctime()))


if __name__ == '__main__':
    processlist = []
    conn = MySQLConnPool('btc_new')
    config_logger()
    
    saveWlt(90000000)
    
    conn.dispose(1)
