# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
获得top address,
因使用了br编码，引入了 brotli包
@author: user
'''
import os, sys, math
import logging
import requests
#from com.scott.dev.util.mysqlpool import MySQLConnPool
from bs4 import BeautifulSoup
from importlib import reload
import time, random
import brotli
import bitcoin, random, secrets
from bitcoinutils.setup import setup
from bitcoinutils.script import Script
from bitcoinutils.keys import P2wpkhAddress, P2wshAddress, P2shAddress, PrivateKey, PublicKey

reload(sys) 
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "E:/data/priv".replace('/', os.sep)
ADDR_URL_PREFIX = "https://privatekeys.pw/bitcoin/keys/{}"
logger = logging.getLogger('get_addr_by_hex_from_middle_to_back')
LOG_FILE = 'get_addr_by_hex_from_middle_to_back.log'
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
    console = logging.StreamHandler()
    console.setLevel(level=logging.DEBUG)  # 设置为INFO级别
    console.setFormatter(fmter)
    logger.addHandler(console)


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

        # wrap in P2SH address
        '''
        uncomp_addr_2spk = uncompressed_addr.to_script_pub_key()
        uncomp_p2sh_addr = P2shAddress.from_script(uncomp_addr_2spk).to_address()
        uncomp_addr_2spk_hex = uncomp_addr_2spk.to_hex()
        '''
        '''
        comp_addr_2spk = compressed_addr.to_script_pub_key()
        comp_p2sh_addr = P2shAddress.from_script(comp_addr_2spk).to_address()
        comp_addr_2spk_hex = comp_addr_2spk.to_hex()
        '''
        
        seg_addr_2spk = segwit_addr.to_script_pub_key()
        segwit_p2sh_addr = P2shAddress.from_script(seg_addr_2spk).to_address()
        uncompress_addr_2spk = uncompressed_btc1_segwit_addr.to_script_pub_key()
        uncompress_p2sh_addr = P2shAddress.from_script(uncompress_addr_2spk).to_address()
        seg_addr_2spk_hex = seg_addr_2spk.to_hex()
    
        # display P2WSH
        '''
        p2wpkh_key = PrivateKey.from_wif(uncompressed_priv_key)
        pswpkh_pub_hex = p2wpkh_key.get_public_key().to_hex()
        script = Script(['OP_1', p2wpkh_key.get_public_key().to_hex(), 'OP_1', 'OP_CHECKMULTISIG'])
        p2wsh_addr = P2wshAddress.from_script(script)
        p2wsh_address = p2wsh_addr.to_address()
        '''
        # display P2SH-P2WSH
        '''
        p2sh_pub = p2wsh_addr.to_script_pub_key()
        p2sh_pub_hex = p2sh_pub.to_hex()
        p2sh_p2wsh_addr = P2shAddress.from_script(p2sh_pub)
        p2sh_p2wsh_address = p2sh_p2wsh_addr.to_address()
        '''
        
        # logger format
        # priv_hex|compressed_priv_key|normal_priv_key
        logger.info('{}|{}|{}|{}|{}|{}|{}|{}|{}'.
                    format(str(priv_hex_param),
                           str(compressed_priv_key), str(normal_priv_key),
                           str(compressed_address), str(uncompressed_address),
                           str(segwit_p2sh_addr), str(uncompress_p2sh_addr),
                           str(segwit_address), str(uncompressed_btc1_addr)))
        # return uncompressed_priv_key, uncompressed_address, compressed_priv_key, compressed_address, private_key, uncompressed_pub, compressed_pub, decoded_private_key, segwit_address, segwit_hash, uncomp_p2sh_addr, uncomp_addr_2spk_hex, comp_p2sh_addr, comp_addr_2spk_hex, segwit_p2sh_addr, seg_addr_2spk_hex, p2wsh_address, pswpkh_pub_hex, p2sh_p2wsh_address, p2sh_pub_hex


def saveSimpleAddrInfo():
    logger.info("saveSimpleAddrInfo start")
    # the last number
    # i = 115792089237316195423570985008687907852837564279074904382605163141518161494331
    i = 57896044618658097711785492504343953926634992332820282019728792003956564819968
    # i = 115792089237316195423570985008687907852837564279074904382605163141518161494330
    #page = 1
    while(i >= 1):
        s_hex = "%064x" % i
        '''
        tmp1 = int(i % RECORD_NUM)
        tmp2 = i / RECORD_NUM
        if (tmp1 > 0 and tmp1 < RECORD_NUM):
            page = int(tmp2) + 1
        else:
            page = int(tmp2)
        '''
        gen_address_by_hex(i)
        i = i - 1


if __name__ == '__main__':
    config_logger()

    saveSimpleAddrInfo()
#     i = 115792089237316195423570985008687907852837564279074904382605163141518161494336
#     print(int(i/2))
#     s_hex = "%064x" % (int(i/2))
#     print (s_hex)
    
