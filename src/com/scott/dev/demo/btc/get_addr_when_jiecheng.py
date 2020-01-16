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
logger = logging.getLogger('get_addr_jiecheng')
LOG_FILE = 'get_addr_jiecheng.log'
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


# 阶乘
def saveSimpleAddrInfo_jiecheng():
    k = 2
    i2 = 4
    k = factorial(i2)
    while(k > 1 and k < MAX_N):
        gen_address_by_hex(k)
        i2 = i2 + 1
        k = factorial(i2)


# 阶幂
def saveSimpleAddrInfo_jiemi():
    i2 = 4
    k = jiemi(i2)
    while(k > 1 and k < MAX_N):
        gen_address_by_hex(k)
        i2 = i2 + 1
        k = jiemi(i2)


# 卡特兰数
def saveSimpleAddrInfo_katelan():
    i2 = 4
    k = int(factorial(i2 * 2) / (factorial(i2 + 1) * factorial(i2)))
    while(k > 1 and k < MAX_N):
        gen_address_by_hex(k)
        i2 = i2 + 1
        k = int(factorial(i2 * 2) / (factorial(i2 + 1) * factorial(i2)))


def jiemi(n):
    if (n == 1):
        return 1
    else:
        return pow(n, jiemi(n - 1))


# 阶乘
def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return (n * factorial(n - 1))


def kamanershu():
    # lst = [561, 41041, 825265, 321197185, 5394826801, 232250619601, 9746347772161, 1436697831295441, 60977817398996785, 7156857700403137441, 1791562810662585767521, 87674969936234821377601, 6553130926752006031481761, 1590231231043178376951698401]
    lst = [127, 323, 835, 2188, 5798, 15511, 41835, 113634, 310572, 853467, 2356779, 6536382, 18199284, 50852019, 142547559, 400763223, 1129760415, 3192727797, 9043402501, 25669818476, 73007772802, 208023278209, 593742784829, 1211, 111221, 312211, 13112221, 1113213211,
 31131211131221, 13211311123113112211,
 11131221133112132113212221,
 3113112221232112111312211312113211,
 1321132132111213122112311311222113111221131221,
 11131221131211131231121113112221121321132132211331, 11131221131211131231121113112221121321132132211331222113112211,
 31131122211311123113111213211231132132211211131221,
 311311222113111231131112132112311321322112111312211312111322212311322113212221, 288, 34560, 24883200, 125411328000,
 5056584744960000, 1834933472251084800000,
 6658606584104736522240000000,
 265790267296391946810949632000000000,
 127313963299399416749559771247411200000000000, 27648, 86400000, 4031078400000,
 3319766398771200000, 55696437941726556979200000,
 21577941222941856209168026828800000,
 215779412229418562091680268288000000000000000,
 61564384586635053951550731889313964883968000000000, 61564384586635053951550731889313964883968000000000000000, 135135, 645120, 2027025, 10321920, 34459425, 185794560,
 654729075, 3715891200, 13749310575, 81749606400,
 316234143225, 1961990553600, 7905853580625,
 51011754393600, 5040, 40320, 362880, 3628800,
 39916800, 479001600, 6227020800, 87178291200,
 1307674368000, 20922789888000, 355687428096000,
 6402373705728000, 121645100408832000,
 2432902008176640000, 51090942171709440000,
 1124000727777607680000, 2741256, 6017193, 1412774811, 11302198488, 137513849003496, 424910390480793000, 933528127886302221000, 1729, 87539319, 6963472309248, 48988659276962496, 24153319581254312065344, 153, 370, 371, 407, 165033, 221859, 336700, 336701, 340067, 341067, 407000, 407001, 444664, 487215, 982827, 983221, 166500333, 296584415, 333667000, 333667001, 334000667, 710656413, 828538472, 142051701000, 166650003333, 262662141664, 333366670000, 41616, 1413721, 48024900, 1631432881, 55420693056, 1882672131025, 63955431761796, 2172602007770041, 73804512832419600, 2507180834294496361, 85170343853180456676, 2893284510173841030625, 512, 1353, 3610, 9713, 26324, 71799, 196938, 542895, 1503312, 4179603, 11662902, 32652735, 91695540, 258215664, 728997192, 2062967382, 5850674704, 16626415975, 47337954326, 135015505407, 385719506620, 1103642686382, 3162376205180, 9073807670316, 26068895429376, 220, 1184, 2620, 5020, 6232, 10744, 12285, 17296, 63020, 66928, 67095, 69615, 79750, 100485, 122265, 122368, 141664, 142310, 171856, 176272, 185368, 196724, 280540, 308620, 319550, 356408, 437456, 469028, 503056, 522405, 600392, 609928, 32212254719, 2833419889721787128217599, 195845982777569926302400511, 4776913109852041418248056622882488319, 1307960347852357218937346147315859062783, 225251798594466661409915431774713195745814267044878909733007331390393510002687, 28, 496, 8128, 33550336, 8589869056, 137438691328,
 2305843008139952128,
 2658455991569831744654692615953842176,
 19156194260823610729479337808430363813099732154816, 191561942608236107294793378084303638130997321548169216, 39916801, 479001599,
 87178291199, 10888869450418352160768000001,
 265252859812191058636308479999999,
 263130836933693530167218012159999999,
 8683317618811886495518194401279999999, 131071, 524287, 2147483647,
 2305843009213693951, 618970019642690137449562111,
 162259276829213363391578010288127,
 170141183460469231731687303715884105727]
    for n in lst:
        if n < MAX_N:
            gen_address_by_hex(n)
            gen_address_by_hex(n + 1)
            gen_address_by_hex(n - 1)
            gen_address_by_hex(n + 2)
            gen_address_by_hex(n - 2)
            gen_address_by_hex(n + 4)
            gen_address_by_hex(n - 4)
            gen_address_by_hex(n + 8)
            gen_address_by_hex(n - 8)

def zoumadeng():
    lst = [142857]
    for n in lst:
        for i in range(1,10):
            gen_address_by_hex(n*i)

if __name__ == '__main__':
    config_logger()

    # saveSimpleAddrInfo_jiecheng()
    # saveSimpleAddrInfo_jiemi()
    # saveSimpleAddrInfo_katelan()
    #kamanershu()
    zoumadeng()
