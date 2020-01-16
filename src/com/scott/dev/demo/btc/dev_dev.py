# -*- coding:utf-8 -*-

'''
Created on 2019年8月26日

@author: user
'''
import os, sys, logging
from importlib import reload
from hashlib import sha256
import bitcoin
# random, secrets
from bitcoinutils.setup import setup
from bitcoinutils.keys import  P2shAddress, PrivateKey
import itertools

reload(sys)
# sys.setdefaultencoding('utf8')

# digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
digits58 = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
PY_GEN_PATH = "E:/data/priv".replace('/', os.sep)
logger = logging.getLogger('dev_dev')
LOG_FILE = 'dev.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(message)s'


def decode_base58(bc, length):
    n = 0
    for char in bc:
        n = n * 58 + digits58.index(char)
    return n.to_bytes(length, 'big')


def check_bc(bc):
    try:
        bcbytes = decode_base58(bc, 25)
        return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]
    except Exception:
        return False


def print_pkq(i):
    i_hex = hex(i)
    s = "%064x" % i
    print(s)
    i = i + 1


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

    
def pinjie():
    prefix = '5vUsuFj43b4HL6t5dyXnRAEKLbEv8nD55fDFNRZLj7t7Nurvh'
    # prefix = '5JvUsuFj43b4HL6t5dyXnRAEKLbEv8nD55fDFNRZLj7t7Nurvh'
    length = len(prefix)
    '''
    for i in range(1,length+1):
        pre = prefix[0:i]
        post = prefix[i:length+1]
        logger.info("{}|{}".format(pre,post))
    '''
    for a in digits58:
        for i in range(1, length + 1):
            pre = prefix[0:i]
            post = prefix[i:length + 1]
            logger.info("{}{}{}".format(pre, str(a), post))


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

 
def gen_pwd():
    string = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&)_+-=[]'\,./{}:\"|<>?"
    a = []
    for i in string:
        a.append(i)
    size = len(a)
    b = 1
    for b in range(1, 3):
        for x in itertools.product(*[a] * b):
            p = ''.join(x)
            logger.info(p)


def dev():
    i =1
    priv_hex_param = "%064x" % i
    gen_address_by_hex(priv_hex_param)

    
if __name__ == '__main__':
    config_logger()
    '''
    priv='5Kdzbp7myy98kM7MywwZC5sEwri5kmQe3PpZ5vnmRKp3PfvYPKx'
    gen_address_by_hex(priv)
    '''
    # gen_pwd()
    dev()
