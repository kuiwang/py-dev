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
from bitcoinutils.setup import setup
from bitcoinutils.script import Script
from bitcoinutils.keys import P2wpkhAddress, P2wshAddress, P2shAddress, PrivateKey, PublicKey
from _operator import add
import datetime

reload(sys)
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
TABLE_NUM = 1000
logger = logging.getLogger('dev_walt_gen_btcutils')
LOG_FILE = 'dev_walt_gen_btcutil.log'
# LOG_FORMATTER = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'
LOG_FORMATTER = '%(asctime)s - %(filename)s - %(lineno)d - %(message)s'
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


def get_url(url, refer=None):
    try:
        UA_LST = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
              'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
              'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
              'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
              'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
              'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
              'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
              'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
              'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
              'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']
        ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        ACCEPT_ENCODING = "gzip, deflate, br"
        ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9"
        CONNECTION = "keep-alive"
        HOST = 'chain.api.btc.com'
        header = {"User-Agent":UA_LST[random.randrange(0, len(UA_LST))], 'HOST':HOST, 'Cache-Control':'no-cache', "Accept":ACCEPT, "Accept-Encoding":ACCEPT_ENCODING, "Accept-Language":ACCEPT_LANGUAGE, "Connection":CONNECTION}
        r = s.get(url, headers=header)
        r.encoding = "utf-8"
        # logger.info("response:\n" + r.text)
    except Exception as e:
        logger.error(e)
    return r.text


def dev_gen_address():
    setup('mainnet')
    # 生成随机私钥
    valid_private_key = False
    while not valid_private_key:
        private_key = bitcoin.random_key()
        private_key = '41a4fefeff8dbe1cc45aa1625f0017afd83f2099116edef58ebc4acc8666e2b0'
        decoded_private_key = bitcoin.decode_privkey(private_key, 'hex')
        valid_private_key = 0 < decoded_private_key < bitcoin.N

        # normal private key
        uncompressed_priv_key = bitcoin.encode_privkey(decoded_private_key, 'wif')
        uncompressed_priv_key='KyA3iE1wRvTcEH3KmGyhy71fwSZjzPY19DgkbLq8a8G9dxNccBbw'
        logger.info("uncompressed_priv_key:{}".format(uncompressed_priv_key))
        priv = PrivateKey.from_wif(uncompressed_priv_key)
        
        normal_priv_key = priv.to_wif(compressed=False)
        compressed_priv_key = priv.to_wif(compressed=True)
        logger.info("uncompress priv key:{}".format(uncompressed_priv_key))
        logger.info("compressed_priv_key:{}".format(compressed_priv_key))
        
        pub = priv.get_public_key()
        uncompressed_pub = pub.to_hex(compressed=False)
        compressed_pub = pub.to_hex(compressed=True)
        logger.info("uncompressed_pub:{}".format(uncompressed_pub))
        logger.info("compress pub:{}".format(compressed_pub))
        
        uncompressed_addr = pub.get_address(compressed=False)
        uncompressed_address = uncompressed_addr.to_address()  # wif_normal address
        compressed_addr = pub.get_address(compressed=True)
        compressed_address = compressed_addr.to_address()  # wif_compressed address
        logger.info("uncompressed_addr:{}".format(uncompressed_address))
        logger.info("compressed_addr:{}".format(compressed_address))
        logger.info("uncompressed_addr_hash:{}".format(uncompressed_addr.to_hash160()))
        logger.info("compressed_addr_hash:{}".format(compressed_addr.to_hash160()))
        
        segwit_addr = pub.get_segwit_address()
        segwit_address = segwit_addr.to_address()
        logger.info("P2WPKH:{}".format(segwit_address))
        segwit_hash = segwit_addr.to_hash()
        logger.info("segwit_hash:{}".format(segwit_hash))
        '''
        addr2 = P2wpkhAddress.from_hash(segwit_hash)
        p2wpkh_addr2 = addr2.to_address()
        logger.info("Created P2wpkhAddress from Segwit Hash and calculate address:{}".format(p2wpkh_addr2))
        
        addr3 = PrivateKey.from_wif(uncompressed_priv_key).get_public_key().get_segwit_address()
        logger.info('addr3:{}'.format(addr3.to_address()))
        '''
        # wrap in P2SH address
        uncomp_addr_2spk = uncompressed_addr.to_script_pub_key()
        uncomp_p2sh_addr = P2shAddress.from_script(uncomp_addr_2spk).to_address()
        uncomp_addr_2spk_hex = uncomp_addr_2spk.to_hex()
        logger.info('uncomp_addr_2spk:{}'.format(uncomp_addr_2spk_hex))
        logger.info("uncomp_p2sh_addr:{}".format(uncomp_p2sh_addr))
        comp_addr_2spk = compressed_addr.to_script_pub_key()
        comp_p2sh_addr = P2shAddress.from_script(comp_addr_2spk).to_address()
        comp_addr_2spk_hex = comp_addr_2spk.to_hex()
        logger.info('comp_addr_2spk:{}'.format(comp_addr_2spk_hex))
        logger.info("comp_p2sh_addr:{}".format(comp_p2sh_addr))
        
        seg_addr_2spk = segwit_addr.to_script_pub_key()
        segwit_p2sh_addr = P2shAddress.from_script(seg_addr_2spk).to_address()
        seg_addr_2spk_hex = seg_addr_2spk.to_hex()
        logger.info('seg_addr_2spk_hex:{}'.format(seg_addr_2spk_hex))
        logger.info("addr4 P2SH(P2WPKH):{}".format(segwit_p2sh_addr))
    
        # display P2WSH
        p2wpkh_key = PrivateKey.from_wif(uncompressed_priv_key)
        pswpkh_pub_hex = p2wpkh_key.get_public_key().to_hex()
        logger.info("pswpkh_pub_hex:{}".format(pswpkh_pub_hex))
        script = Script(['OP_1', p2wpkh_key.get_public_key().to_hex(), 'OP_1', 'OP_CHECKMULTISIG'])
        p2wsh_addr = P2wshAddress.from_script(script)
        p2wsh_address = p2wsh_addr.to_address()
        logger.info("P2WSH of P2PK:{}".format(p2wsh_address))
    
        # display P2SH-P2WSH
        p2sh_pub = p2wsh_addr.to_script_pub_key()
        p2sh_pub_hex = p2sh_pub.to_hex()
        logger.info("p2sh_pub_hex:{}".format(p2sh_pub_hex))
        p2sh_p2wsh_addr = P2shAddress.from_script(p2sh_pub)
        p2sh_p2wsh_address = p2sh_p2wsh_addr.to_address()
        logger.info("P2SH(P2WSH of P2PK):{}".format(p2sh_p2wsh_address))
        
        return uncompressed_priv_key, uncompressed_address, compressed_priv_key, compressed_address, private_key, uncompressed_pub, compressed_pub, decoded_private_key, segwit_address, segwit_hash, uncomp_p2sh_addr, uncomp_addr_2spk_hex, comp_p2sh_addr, comp_addr_2spk_hex, segwit_p2sh_addr, seg_addr_2spk_hex, p2wsh_address, pswpkh_pub_hex, p2sh_p2wsh_address, p2sh_pub_hex


if __name__ == '__main__':
    setup('mainnet')
    config_logger()
    #dev_gen_address()
    print(time.time())
