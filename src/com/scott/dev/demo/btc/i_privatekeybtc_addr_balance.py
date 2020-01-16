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

PY_GEN_PATH = "E:/data/priv".replace('/', os.sep)
# PY_GEN_PATH = "/vagrant/priv".replace('/', os.sep)
ADDR_URL_PREFIX = "https://privatekeys.pw/bitcoin/keys/{}"
logger = logging.getLogger('privk_btc_addr')
LOG_FILE = 'i-privk_btc_addr.log'
RECORD_NUM = 45
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
# LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'
LOG_FORMATTER = '%(lineno)d-%(message)s'
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
    
    console = logging.StreamHandler()
    console.setLevel(level=logging.DEBUG)  # 设置为INFO级别
    console.setFormatter(fmter)
    logger.addHandler(console)
    


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


def saveSimpleAddrInfo():
    priv_pre = '5HwcyzKDae5kpek'
    priv_last = 'WaZCBavso3BvGaB'
    
    a = []
    digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    for i in digits58:
        a.append(i)
    b = 21
    for x in itertools.product(*[a] * b):
        p = ''.join(x)
        priv = priv_pre + str(p) + priv_last
        try:
            pvk = PrivateKey.from_wif(priv)
            # logger.info('pvk')
            gen_address_by_hex(priv)
        except Exception as e:
            # logger.error(p+"=er")
            continue
        # print(priv)
        
        # logger.info(priv)


def gen_address_by_priv_key(priv_param):
    # logger.info('priv_param:{}'.format(priv_param))
    setup('mainnet')
    # 生成随机私钥
    uncompressed_priv_key = priv_param
    priv = PrivateKey.from_wif(uncompressed_priv_key)
    
    normal_priv_key = priv.to_wif(compressed=False)
    compressed_priv_key = priv.to_wif(compressed=True)
    logger.info("privparam:{}_normalpriv:{}_comppriv:{}".format(priv_param, str(normal_priv_key), str(compressed_priv_key)))
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
    logger.info('{}|{}|{}|{}|{}|{}|{}|{}|{}|'.format(str(priv_param), str(compressed_priv_key), str(normal_priv_key), str(compressed_address), str(uncompressed_address), str(segwit_p2sh_addr), str(uncompress_p2sh_addr), str(segwit_address), str(uncompressed_btc1_addr)))
        # return uncompressed_priv_key, uncompressed_address, compressed_priv_key, compressed_address, private_key, uncompressed_pub, compressed_pub, decoded_private_key, segwit_address, segwit_hash, uncomp_p2sh_addr, uncomp_addr_2spk_hex, comp_p2sh_addr, comp_addr_2spk_hex, segwit_p2sh_addr, seg_addr_2spk_hex, p2wsh_address, pswpkh_pub_hex, p2sh_p2wsh_address, p2sh_pub_hex


def check_priv(pk):
    try:
        pvk = PrivateKey.from_wif(pk)
        return True
    except Exception as e:
        return False


def dev():
    addr = '3Nxwenay9Z8Lc9JBiywExpnEFiLp6Afp8v'
    priv_orig = '5vUsuFj43b4HL6t5dyXnRAEKLbEv8nD55fDFNRZLj7t7Nurvh'
    size = len(priv_orig)
    digits = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    
    a = []
    for i in digits:
        a.append(i)
    b = 2
    for x in itertools.product(*[a] * b):
        p = ''.join(x)
        for i in range(1, size + 1):
            pre = priv_orig[:i]
            post = priv_orig[i:size + 1]
            pk = pre + p + post
            # logger.info(pk)
            try:
                # pvk = PrivateKey.from_wif(pk)
                gen_address_by_priv_key(pk)
            except Exception as e:
                continue
    logger.info('lower-upper-convert')
    res = ''
    for c in priv_orig:
        if(c.islower()):
            c1 = c.upper()
        elif(c.isupper()):
            c1 = c.lower()
        else:
            c1 = c
        res = res + c1
    priv_orig1 = res
    logger.info("priv_orig1:{}".format(str(priv_orig1)))
    size1 = len(priv_orig1)
    for x in itertools.product(*[a] * b):
        p = ''.join(x)
        for i in range(1, size1 + 1):
            pre = priv_orig1[:i]
            post = priv_orig1[i:size1 + 1]
            pk = pre + p + post
            # logger.info(pk)
            try:
                # pvk = PrivateKey.from_wif(pk)
                gen_address_by_priv_key(pk)
            except Exception as e:
                continue
    
    ######b=3
    b = 3
    for x in itertools.product(*[a] * b):
        p = ''.join(x)
        for i in range(1, size + 1):
            pre = priv_orig[:i]
            post = priv_orig[i:size + 1]
            pk = pre + p + post
            try:
                gen_address_by_priv_key(pk)
            except Exception as e:
                continue
    
    res = ''
    for c in priv_orig:
        if(c.islower()):
            c1 = c.upper()
        elif(c.isupper()):
            c1 = c.lower()
        else:
            c1 = c
        res = res + c1
    priv_orig1 = res
    size = len(priv_orig1)
    for x in itertools.product(*[a] * b):
        p = ''.join(x)
        for i in range(1, size + 1):
            pre = priv_orig1[1:i]
            post = priv_orig1[i:size + 1]
            pk = pre + p + post
            
            try:
                gen_address_by_priv_key(pk)
            except Exception as e:
                continue


def test(i):
    setup('mainnet')
    # 生成随机私钥
    valid_private_key = False
    while not valid_private_key:
        priv_hex_param = "%064x" % i
        private_key = priv_hex_param
        # 66d891b5ed7f51e5044be6a7ebe4e2eae32b960f5aa0883f7cc0ce4fd6921e31
        decoded_private_key = bitcoin.decode_privkey(private_key, 'hex')
        valid_private_key = 0 <= decoded_private_key < bitcoin.N
        # normal private key
        uncompressed_priv_key = bitcoin.encode_privkey(decoded_private_key, 'wif')
        priv = PrivateKey.from_wif(uncompressed_priv_key)
        
        normal_priv_key = priv.to_wif(compressed=False)
        compressed_priv_key = priv.to_wif(compressed=True)
        
        pub = priv.get_public_key()
        
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


if __name__ == '__main__':
    setup('mainnet')
    config_logger()

    # saveSimpleAddrInfo()
#     pk1 = '5vUsuFj43b4HL6t5dyXnRAEKLbEv8nD55fDFNRZLj7t7zzNurvh'
#     logger.info(check_priv(pk1))
#     pk2 = '5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf'
#     logger.info(check_priv(pk2))
    test(1)
    '''
    test(1)
    dev_k= '5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf'
    dev_k1='5VuSUfJ43B4hl6T5DYxNraeklBeV8Nd55FdfnrzlJ7T7nURVHzz'
    logger.info('342 line')
    gen_address_by_priv_key(dev_k1)
    '''
