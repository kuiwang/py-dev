# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
解析blk.dat文件
@author: user
'''
import os, sys, time
import logging
from importlib import reload
from com.scott.dev.util.mysqlpool import MySQLConnPool
from blockchain_parser.block import Block
import hashlib
from ecdsa import SECP256k1, SigningKey
import binascii
  
# 58 character alphabet used
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
KEY_ALPHA = '0123456789abcdefghijklmnopqrstuvwxyzabcdefghijkmnopqrstuvwxyz'

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

# generate walt


def from_bytes (data, big_endian=False):
    if isinstance(data, str):
        data = bytearray(data)
    if big_endian:
        data = reversed(data)
    num = 0
    for offset, byte in enumerate(data):
        num += byte << (offset * 8)
    return num

    
def base58_encode(version, public_address):
    """
    Gets a Base58Check string
    See https://en.bitcoin.it/wiki/Base58Check_encoding
    """
    if sys.version_info.major > 2:
        version = bytes.fromhex(version)
    else:
        version = bytearray.fromhex(version)
    firstSHA256 = hashlib.sha256(version + public_address)
    logger.info("first sha256: %s" % firstSHA256.hexdigest().upper())
    secondSHA256 = hashlib.sha256(firstSHA256.digest())
    logger.info("second sha256: %s" % secondSHA256.hexdigest().upper())
    checksum = secondSHA256.digest()[:4]
    payload = version + public_address + checksum
    logger.info("Hex address: %s" % binascii.hexlify(payload).decode().upper())
    if sys.version_info.major > 2:
        result = int.from_bytes(payload, byteorder="big")
    else:
        result = from_bytes(payload, True)
    # count the leading 0s
    padding = len(payload) - len(payload.lstrip(b'\0'))
    encoded = []

    while result != 0:
        result, remainder = divmod(result, 58)
        encoded.append(BASE58_ALPHABET[remainder])

    return padding * "1" + "".join(encoded)[::-1]


def get_private_key(hex_string):
    if sys.version_info.major > 2:
        return bytes.fromhex(hex_string.zfill(64))
    else:
        return bytearray.fromhex(hex_string.zfill(64))


def get_public_key(private_key):
    # this returns the concatenated x and y coordinates for the supplied private address
    # the prepended 04 is used to signify that it's uncompressed
    if sys.version_info.major > 2:
        return (bytes.fromhex("04") + SigningKey.from_string(private_key, curve=SECP256k1).verifying_key.to_string())
    else:
        return (bytearray.fromhex("04") + SigningKey.from_string(private_key, curve=SECP256k1).verifying_key.to_string())


def get_public_address(public_key):
    address = hashlib.sha256(public_key).digest()
    logger.info("public key hash256: %s" % hashlib.sha256(public_key).hexdigest().upper())
    h = hashlib.new('ripemd160')
    h.update(address)
    address = h.digest()
    logger.info("RIPEMD-160: %s" % h.hexdigest().upper())
    return address


def gen_noraml_list():
    lst = [chr(i) for i in range(97, 123)]
    for i in range(0, 10):
        lst.append(str(i))
    
    logger.info(lst)


# 排列数
def Permutation(ss):
    res = []
    if len(ss) <= 1:
        return ss
    size = len(ss)
    for i in range(size):
        for n in map(lambda x:ss[i] + x, Permutation(ss[:i] + ss[i + 1:])):
            res.append(n)
    return res


def checkRandKeyExists(rand_key):
    '''
    select_sql = 'select rand_key from gen_addr t where t.rand_key= "{}"'.format(str(rand_key))
    try:
        res = conn.queryone(select_sql)
        if res:
            return True
        else:
            return False
    except Exception as e:
        logger.error('checkRandKeyExists exception' + e)
        return False
    '''
    return False


def perm(s=''):
    # logger.info("perm | s:{}".format(s))
    if len(s) <= 1:
        return [s]
    sl = []
    # logger.info('length:{}'.format(str(len(s))))
    for i in range(len(s)):
        for j in perm(s[0:i] + s[i + 1:]):
            sl.append(s[i] + j)
            size = len(sl)
            if(size % 1000000 == 0):
                savePermutation(sl)
                sl = []
    return sl


def savePermutation(lst):
    size = len(lst)
    logger.info('savePermutation | size:{}'.format(str(size)))
    param = []
    insert_gen_sql = 'insert into gen_addr(rand_key) values(%s)'
    for n in lst:
        isRandExist = checkRandKeyExists(n)
        num = 0
        len_n = len(n)
        if ((not isRandExist) and (len_n >= 35)):
            num = num + 1 
            param.append([str(n)])
            if (num % 1000000 == 0):
                times = num / 1000000
                insert_gen_count = conn.insertmany(insert_gen_sql, param)
                conn.end('commit')
                logger.info('times:{} savePermutation successful! count:{}'.format(str(times), str(insert_gen_count)))
                param = []
    if len(param) > 0:
        insert_gen_count = conn.insertmany(insert_gen_sql, param)
        conn.end('commit')
        logger.info('savePermutation successful at last! count:{}'.format(str(insert_gen_count)))


def gen_random():
    BASE_LIST = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # logger.info('size:{}'.format(str(len(BASE_LIST))))
    k1 = ''
    k2 = ''
    k3 = ''
    k4 = ''
    k5 = ''
    k6 = ''
    k7 = ''
    k8 = ''
    sum1 = 0
    sum2 = 0
    sum3 = 0
    sum4 = 0
    sum5 = 0
    sum6 = 0
    sum7 = 0
    sum8 = 0
    for i1 in BASE_LIST:
        for i2 in BASE_LIST:
            for i3 in BASE_LIST:
                for i4 in BASE_LIST:
                    sum1 = sum1 + 1
                    k1 = str(i1) + str(i2) + str(i3) + str(i4)
    logger.info('sum1 = {}'.format(str(sum1)))
                    
    for i5 in BASE_LIST:
        for i6 in BASE_LIST:
            for i7 in BASE_LIST:
                for i8 in BASE_LIST:
                    sum2 = sum2 + 1
                    k2 = str(i5) + str(i6) + str(i7) + str(i8)
    logger.info('sum2 = {}'.format(str(sum2)))
    for i9 in BASE_LIST:
        for i10 in BASE_LIST:
            for i11 in BASE_LIST:
                for i12 in BASE_LIST:
                    sum3 = sum3 + 1
                    k3 = str(i9) + str(i10) + str(i11) + str(i12)
    logger.info('sum3 = {}'.format(str(sum3)))
    for i13 in BASE_LIST:
        for i14 in BASE_LIST:
            for i15 in BASE_LIST:
                for i16 in BASE_LIST:
                    sum4 = sum4 + 1
                    k4 = str(i13) + str(i14) + str(i15) + str(i16)
    logger.info('sum4 = {}'.format(str(sum4)))
    for i17 in BASE_LIST:
        for i18 in BASE_LIST:
            for i19 in BASE_LIST:
                for i20 in BASE_LIST:
                    sum5 = sum5 + 1
                    k5 = str(i17) + str(i18) + str(i19) + str(i20)
    logger.info('sum5 = {}'.format(str(sum5)))
    for i21 in BASE_LIST:
        for i22 in BASE_LIST:
            for i23 in BASE_LIST:
                for i24 in BASE_LIST:
                    sum6 = sum6 + 1
                    k6 = str(i21) + str(i22) + str(i23) + str(i24)
    logger.info('sum6 = {}'.format(str(sum6)))
    for i25 in BASE_LIST:
        for i26 in BASE_LIST:
            for i27 in BASE_LIST:
                for i28 in BASE_LIST:
                    sum7 = sum7 + 1
                    k7 = str(i25) + str(i26) + str(i27) + str(i28)
    logger.info('sum7 = {}'.format(str(sum7)))
    for i29 in BASE_LIST:
        for i30 in BASE_LIST:
            for i31 in BASE_LIST:
                for i32 in BASE_LIST:
                    sum8 = sum8 + 1
                    k8 = str(i29) + str(i30) + str(i31) + str(i32)
    logger.info('sum8 = {}'.format(str(sum8)))
    
    rand_key = i1 + i2 + i3 + i4 + i5 + i6 + i7 + i8 

    logger.info('sum = ' + str(sum))


def gen_wallet1():
    random_key = 'ccea9c5a20e2b78c2e0fbdd8ae2d2b67e6b1894ccb7a55fc1de08bd53994ea64'
    private_key = get_private_key(random_key)
    logger.info('private_key:{}'.format(str(private_key)))
    priv_key_len = len(private_key)
    logger.info('private_key len:{}'.format(priv_key_len))
    logger.info("private key: %s" % binascii.hexlify(private_key).decode().upper())
    public_key = get_public_key(private_key)
    logger.info('public_key:{}'.format(str(public_key)))
    logger.info("public key:{}".format(binascii.hexlify(public_key).decode().upper()))
    public_address = get_public_address(public_key)
    bitcoin_address = base58_encode("00", public_address)
    logger.info("Final address %s" % bitcoin_address)


def gen_wallet():
    random_key = 'ccea9c5a20e2b78c2e0fbdd8ae2d2b67e6b1894ccb7a55fc1de08bd53994ea64'
    private_key_hex = get_private_key(random_key)
    logger.info('private key hex:{}'.format(str(private_key_hex)))
    priv_key_len = len(private_key_hex)
    logger.info('private key hex len:{}'.format(priv_key_len))
    logger.info("private key: %s" % binascii.hexlify(private_key_hex).decode().upper())
    public_key_hex = get_public_key(private_key_hex)
    logger.info('public key hex:{}'.format(str(public_key_hex)))
    logger.info("public key:{}".format(binascii.hexlify(public_key_hex).decode().upper()))
    public_address = get_public_address(public_key_hex)
    bitcoin_address = base58_encode("00", public_address)
    logger.info("Final address %s" % bitcoin_address)


def pcurve_dev():
    Pcurve = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1  # 有限域
    x = 0xd061e9c5891f579fd548cfd22ff29f5c642714cc7e7a9215f0071ef5a5723f69
    y = 0x1757b28e31be71f09f24673eed52348e58d53bcfd26f4d96ec6bf1489eab429d
    
    x_res = x ** 3 + 7
    y_res = y ** 2
    
    logger.info('equal ?{}'.format((x_res % Pcurve) == (y_res % Pcurve)))


if __name__ == '__main__':
    conn = MySQLConnPool('btc')
    config_logger()
    # gen_wallet1()
    lst = perm(KEY_ALPHA)
    savePermutation(lst)
#     # gen_noraml_list()
    # gen_random()
    # pcurve_dev()
    conn.dispose(1)
