# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
获得top address,
因使用了br编码，引入了 brotli包
@author: user
'''
import os, sys
import logging
import requests
# from com.scott.dev.util.mysqlpool import MySQLConnPool
from bs4 import BeautifulSoup
from importlib import reload
import time, random
import brotli
import bitcoin
# random, secrets
from bitcoinutils.setup import setup
from bitcoinutils.keys import  P2shAddress, PrivateKey
import itertools
'''
https://bitcointalk.org/index.php?topic=5166284.0
'''

reload(sys) 
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/data/priv".replace('/', os.sep)
# PY_GEN_PATH = "/vagrant/priv".replace('/', os.sep)
ADDR_URL_PREFIX = "https://privatekeys.pw/bitcoin/keys/{}"
logger = logging.getLogger('i-have-paid')
LOG_FILE = 'i-have-paid.log'
RECORD_NUM = 45
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
# LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'
LOG_FORMATTER = '%(message)s'
digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
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
    '''
    console = logging.StreamHandler()
    console.setLevel(level=logging.DEBUG)  # 设置为INFO级别
    console.setFormatter(fmter)
    logger.addHandler(console)
    '''


def gen_address_by_hex(priv_param):
    setup('mainnet')
    # 生成随机私钥
    # logger.info(priv_param)
    # normal private key
    uncompressed_priv_key = priv_param
    # logger.info('uncompressed_priv_key:{}'.format(str(uncompressed_priv_key)))
    priv = PrivateKey.from_wif(uncompressed_priv_key)
    
    normal_priv_key = priv.to_wif(compressed=False)
    compressed_priv_key = priv.to_wif(compressed=True)
    # logger.info('normal_priv_key:{}'.format(str(normal_priv_key)))
    # logger.info('compressed_priv_key:{}'.format(str(compressed_priv_key)))
    
    pub = priv.get_public_key()
    # uncompressed_pub = pub.to_hex(compressed=False)
    # compressed_pub = pub.to_hex(compressed=True)
    
    uncompressed_addr = pub.get_address(compressed=False)
    uncompressed_address = uncompressed_addr.to_address()  # wif_normal address
    compressed_addr = pub.get_address(compressed=True)
    compressed_address = compressed_addr.to_address()  # wif_compressed address
    
    # btc1 address
    segwit_addr = pub.get_segwit_address()
    segwit_address = segwit_addr.to_address()
    segwit_hash = segwit_addr.to_hash()
    uncompressed_btc1_segwit_addr = pub.get_segwit_address_uncompressed()
    uncompressed_btc1_addr = uncompressed_btc1_segwit_addr.to_address()

    seg_addr_2spk = segwit_addr.to_script_pub_key()
    segwit_p2sh_addr = P2shAddress.from_script(seg_addr_2spk).to_address()
    uncompress_addr_2spk = uncompressed_btc1_segwit_addr.to_script_pub_key()
    uncompress_p2sh_addr = P2shAddress.from_script(uncompress_addr_2spk).to_address()
    seg_addr_2spk_hex = seg_addr_2spk.to_hex()
    
    # logger format
    # priv_hex|compressed_priv_key|normal_priv_key
    logger.info('{}|{}|{}|{}|{}|{}|{}|{}|{}|'.
                format(str(priv_param),
                       str(compressed_priv_key), str(normal_priv_key),
                       str(compressed_address), str(uncompressed_address),
                       str(segwit_p2sh_addr), str(uncompress_p2sh_addr),
                       str(segwit_address), str(uncompressed_btc1_addr)))
        # return uncompressed_priv_key, uncompressed_address, compressed_priv_key, compressed_address, private_key, uncompressed_pub, compressed_pub, decoded_private_key, segwit_address, segwit_hash, uncomp_p2sh_addr, uncomp_addr_2spk_hex, comp_p2sh_addr, comp_addr_2spk_hex, segwit_p2sh_addr, seg_addr_2spk_hex, p2wsh_address, pswpkh_pub_hex, p2sh_p2wsh_address, p2sh_pub_hex


def check_bc(bc):
    try:
        bcbytes = decode_base58(bc, 25)
        return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]
    except Exception:
        return False


def saveSimpleAddrInfo(pre, post):
    
    # priv_pre = '5HwcyzKDae5kpek'
    # priv_last = 'WaZCBavso3BvGaB'
    
    a = []
    digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    for i in digits58:
        a.append(i)
    b = 21
    i = 0
    j = 0
    for x in itertools.product(*[a] * b):
        p = ''.join(x)
        priv = str(pre + str(p) + post).strip()
        i = i + 1
        if ((i % 100000000000) == 0):
            logger.info("priv:{}-p:{}-i:{}-ts:{} ".format(str(priv), str(p), str(i), time.ctime()))
        try:
            canConvert = PrivateKey.from_wif(priv)
            #if canConvert:
            gen_address_by_hex(priv)
        except Exception as e:
            # logger.error("_")
            continue
        # print(priv)
        
        # logger.info(priv)


if __name__ == '__main__':
    setup('mainnet')
    config_logger()
    addr = '1C8oHWB7htH139na4y8kG4w99MFrepseUv'
    pre = '5HwcyzKDae5kpek'
    post = 'WaZCBavso3BvGaB'
    saveSimpleAddrInfo(pre, post)
    
    addr = '15BVzV9iXXVeZTLhP4V2MuhVMx6Tfo3XiC'
    pre = '5kHNq7eBo8M6BWa'
    post = 'LEYcZEHwcyzKDae'
    saveSimpleAddrInfo(pre, post)
    # pvk='5J7VseRcwkirjcUyCTaSUAGEdPBZeaRzWt871U7EB9WbKagyEok'
    # gen_address_by_hex(pvk)
    # dev()
