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
# from bitcoinutils.script import Script
# from bitcoinutils.keys import P2wpkhAddress, P2wshAddress, P2shAddress, PrivateKey, PublicKey
from bitcoinutils.keys import  P2shAddress, PrivateKey

reload(sys) 
# sys.setdefaultencoding('utf8')
MAX_N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364140
PY_GEN_PATH = "E:/data/priv".replace('/', os.sep)
# PY_GEN_PATH = "/vagrant/priv".replace('/', os.sep)
ADDR_URL_PREFIX = "https://privatekeys.pw/bitcoin/keys/{}"
logger = logging.getLogger('get_addr_2num')
LOG_FILE = 'get_addr_2num.log1'
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
        logger.info('{}|{}|{}|{}|{}|{}|{}|{}|{}|'.
                    format(str(priv_hex_param),
                           str(compressed_priv_key), str(normal_priv_key),
                           str(compressed_address), str(uncompressed_address),
                           str(segwit_p2sh_addr), str(uncompress_p2sh_addr),
                           str(segwit_address), str(uncompressed_btc1_addr)))
        # return uncompressed_priv_key, uncompressed_address, compressed_priv_key, compressed_address, private_key, uncompressed_pub, compressed_pub, decoded_private_key, segwit_address, segwit_hash, uncomp_p2sh_addr, uncomp_addr_2spk_hex, comp_p2sh_addr, comp_addr_2spk_hex, segwit_p2sh_addr, seg_addr_2spk_hex, p2wsh_address, pswpkh_pub_hex, p2sh_p2wsh_address, p2sh_pub_hex


def gen_address_by_hex_simple(i):
    setup('mainnet')
    # 生成随机私钥
    valid_private_key = False
    while not valid_private_key:
        priv_hex_param = "%064x" % i
        #priv_hex_param = i
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
    i = 1
    while(i >= 1):
        gen_address_by_hex(i)
        i = i * 2
        j = i - 1
        gen_address_by_hex(j)
        gen_address_by_hex(j * 2)
        gen_address_by_hex(j * 3)
        gen_address_by_hex(j * 5)
        gen_address_by_hex(j * 7)
        gen_address_by_hex(j * 11)
        gen_address_by_hex(j * 13)
        gen_address_by_hex(j * 17)
        gen_address_by_hex(j * 19)
        gen_address_by_hex(j * 23)
        gen_address_by_hex(j * 29)
        gen_address_by_hex(j * 31)
        gen_address_by_hex(j * 37)
        gen_address_by_hex(j * 41)
        gen_address_by_hex(j * 43)
        gen_address_by_hex(j * 47)
        k = i + 1
        gen_address_by_hex(k)
        gen_address_by_hex(k * 2)
        gen_address_by_hex(k * 3)
        gen_address_by_hex(k * 5)
        gen_address_by_hex(k * 7)
        gen_address_by_hex(k * 11)
        gen_address_by_hex(k * 13)
        gen_address_by_hex(k * 17)
        gen_address_by_hex(k * 19)
        gen_address_by_hex(k * 23)
        gen_address_by_hex(j * 29)
        gen_address_by_hex(j * 31)
        gen_address_by_hex(j * 37)
        gen_address_by_hex(j * 41)
        gen_address_by_hex(j * 43)
        gen_address_by_hex(j * 47)


def saveSimpleAddrInfo_3():
    i = 1
    while(i >= 1 and i <= MAX_N):
        gen_address_by_hex(i)
        i = i * 3
        j = i - 1
        gen_address_by_hex(j)
        k = i + 1
        gen_address_by_hex(k)


def saveSimpleAddrInfo_5():
    i = 1
    while(i >= 1 and i <= MAX_N):
        gen_address_by_hex(i)
        i = i * 5
        j = i - 1
        gen_address_by_hex(j)
        k = i + 1
        gen_address_by_hex(k)


def saveSimpleAddrInfo_7():
    i = 1
    while(i >= 1 and i <= MAX_N):
        gen_address_by_hex(i)
        i = i * 7
        j = i - 1
        gen_address_by_hex(j)
        k = i + 1
        gen_address_by_hex(k)


def saveSimpleAddrInfo_11():
    i = 1
    while(i >= 1 and i <= MAX_N):
        gen_address_by_hex(i)
        i = i * 11
        j = i - 1
        gen_address_by_hex(j)
        k = i + 1
        gen_address_by_hex(k)


def saveSimpleAddrInfo_13():
    i = 1
    while(i >= 1 and i <= MAX_N):
        gen_address_by_hex(i)
        i = i * 13
        j = i - 1
        gen_address_by_hex(j)
        k = i + 1
        gen_address_by_hex(k)


def saveSimpleAddrInfo_17():
    i = 1
    while(i >= 1 and i <= MAX_N):
        gen_address_by_hex(i)
        i = i * 17
        j = i - 1
        gen_address_by_hex(j)
        k = i + 1
        gen_address_by_hex(k)


def saveSimpleAddrInfo_19():
    i = 1
    while(i >= 1 and i <= MAX_N):
        gen_address_by_hex(i)
        i = i * 19
        j = i - 1
        gen_address_by_hex(j)
        k = i + 1
        gen_address_by_hex(k)


def saveSimpleAddrInfo_0618():
    i = MAX_N
    # 黄金分割点数
    '''
    while(i >= 1):
        gen_address_by_hex(i)
        gen_address_by_hex(int(i * 0.6))
        gen_address_by_hex(int(i * 0.61))
        gen_address_by_hex(int(i * 0.618))
        i = int(i * 0.618)
    '''
    '''
    # 七角锥数
    j = 1
    i1 = 1
    while(j >= 1 and j < MAX_N):
        gen_address_by_hex(j)
        i1 = i1 + 1 
        j = (int)(i1 * (i1 + 1) * (5 * i1 - 2) / 6)
    
    # 五角锥数
    m = 1
    i3 = 1
    while(m >= 1 and m < MAX_N):
        gen_address_by_hex(m)
        i3 = i3 + 1
        m = (int)((i3 * i3 * (i3 + 1)) / 2)
    # 平方数
    n = 1
    i4 = 1 
    while(n >= 1 and n < MAX_N):
        gen_address_by_hex(n)
        i4 = i4 + 1
        n = (int)(i4 * i4)
    
    # 立方数
    p = 1
    i5 = 1 
    while(p >= 1 and p < MAX_N):
        gen_address_by_hex(p)
        i5 = i5 + 1
        p = (i5 * (i5 + 1)) * (i5 * (i5 + 1))
    '''
    # 五次方数
    '''
    k = 2
    i2 = 1
    while(k > 1 and k < MAX_N):
        gen_address_by_hex(k)
        i2 = i2 + 1
        k = (int)(i2 * i2 * i2 * i2 * i2)
    '''
    i1 = 0x4442e3d2c2342fcd609a490144a978814cbe864d1d36cb5bf8ab479e27909007
    i2 = 0x35fc22e2976f206a1805716dc53d29d4f61e34f30f57337e0972e99db2aec21d
    i3 = 0x76e9b8c79dee21a88912202c02f1759e622460debf2d7b05b793247efa1b68a2
    i4 = 0b0111011011101001101110001100011110011101111011100010000110101000100010010001001000100000001011000000001011110001011101011001111001100010001001000110000011011110101111110010110101111011000001011011011110010011001001000111111011111010000110110110100010100010
    gen_address_by_hex_simple(i1)
    gen_address_by_hex_simple(i2)
    gen_address_by_hex_simple(i3)
    gen_address_by_hex_simple(i4)


def test():
    i = MAX_N
    i = i * 0.618
    j = i - 1
    print(i)


if __name__ == '__main__':
    config_logger()

    # saveSimpleAddrInfo()
    # saveSimpleAddrInfo_19()
    saveSimpleAddrInfo_0618()
    # test()
