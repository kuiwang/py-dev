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
'''
https://bitcointalk.org/index.php?topic=5166284.0
'''

reload(sys) 
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "E:/data/priv".replace('/', os.sep)
# PY_GEN_PATH = "/vagrant/priv".replace('/', os.sep)
ADDR_URL_PREFIX = "https://privatekeys.pw/bitcoin/keys/{}"
logger = logging.getLogger('get_addr_from_specified_to_front1')
LOG_FILE = 'get_addr_826_to_front.log'
RECORD_NUM = 45
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
# LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'
LOG_FORMATTER = '%(message)s'

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


def gen_address_by_hex(i):
    setup('mainnet')
    # 生成随机私钥
    valid_private_key = False
    while not valid_private_key:
        # private_key = bitcoin.random_key()
        '''
        bits = secrets.randbits(256)
        # 46518555179467323509970270980993648640987722172281263586388328188640792550961
        bits_hex = hex(bits)
        # 0x66d891b5ed7f51e5044be6a7ebe4e2eae32b960f5aa0883f7cc0ce4fd6921e31
        private_key = bits_hex[2:]
        '''
        priv_hex_param = "%064x" % i
        private_key = priv_hex_param
        # 66d891b5ed7f51e5044be6a7ebe4e2eae32b960f5aa0883f7cc0ce4fd6921e31
        decoded_private_key = bitcoin.decode_privkey(private_key, 'hex')
        valid_private_key = 0 < decoded_private_key < bitcoin.N
        
        # normal private key
        uncompressed_priv_key = bitcoin.encode_privkey(decoded_private_key, 'wif')
        priv = PrivateKey.from_wif(uncompressed_priv_key)
        
        normal_priv_key = priv.to_wif(compressed=False)
        compressed_priv_key = priv.to_wif(compressed=True)
        
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
                    format(str(priv_hex_param),
                           str(compressed_priv_key), str(normal_priv_key),
                           str(compressed_address), str(uncompressed_address),
                           str(segwit_p2sh_addr), str(uncompress_p2sh_addr),
                           str(segwit_address), str(uncompressed_btc1_addr)))
        # return uncompressed_priv_key, uncompressed_address, compressed_priv_key, compressed_address, private_key, uncompressed_pub, compressed_pub, decoded_private_key, segwit_address, segwit_hash, uncomp_p2sh_addr, uncomp_addr_2spk_hex, comp_p2sh_addr, comp_addr_2spk_hex, segwit_p2sh_addr, seg_addr_2spk_hex, p2wsh_address, pswpkh_pub_hex, p2sh_p2wsh_address, p2sh_pub_hex


def saveSimpleAddrInfo():
    # logger.info("saveSimpleAddrInfo start")
    # i = 57896044618658097711785492504343953926634992332820282019728792003956564819968
    # tmp = 57896044618658097711785492504343953926634992332820282019728792003956564819968
    # i = 0x800000000000000000000000000000000000000000000000000000000000460f
    # i = 0x800000000000000000000000000000000000000000000000000000000007f75e
    # from 20190925
    # i = 0x000000000000000000000000000000000000000af55fc59c335c8ec67ed24826
    #i = 0x000000000000000000000000000000000000000af55fc59c335c8ec67ed2a482
    #i = 0x000000000000000000000000000000000000000af55fc59c335c8ec67ed336af
    i = 0x000000000000000000000000000000000000000af55fc59c335c8ec67ed68c92
    while(i >= 1):
        gen_address_by_hex(i)
        i = i + 1


if __name__ == '__main__':
    config_logger()

    saveSimpleAddrInfo()
