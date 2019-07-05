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

reload(sys)
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
TABLE_NUM = 1000
logger = logging.getLogger('walt_gen')
LOG_FILE = 'walt_gen.log'
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


def get_address():
    # 生成随机私钥
    valid_private_key = False
    while not valid_private_key:
        private_key = bitcoin.random_key()
        # logger.info('random_info:{} | length:{}'.format(private_key, str(len(private_key))))
        decoded_private_key = bitcoin.decode_privkey(private_key, 'hex')
        # logger.info("decoded_private_key:{}".format(decoded_private_key))
        valid_private_key = 0 < decoded_private_key < bitcoin.N
        
        # 将私钥转换为WIF格式
        wif_enc_priv = bitcoin.encode_privkey(decoded_private_key, 'wif')
        # logger.info('wif_encoded_private_key:{}'.format(wif_enc_priv))
        # time.sleep(1 / 5)
        
        dec_enc_priv = bitcoin.encode_privkey(decoded_private_key, 'decimal')
        bin_enc_priv = bitcoin.encode_privkey(decoded_private_key, 'bin')
        bin_compress_enc_priv = bitcoin.encode_privkey(decoded_private_key, 'bin_compressed')
        
        # hex_encoded_priv == private_key
        # hex_encoded_priv = bitcoin.encode_privkey(decoded_private_key, 'hex')
        hex_compress_enc_priv = bitcoin.encode_privkey(decoded_private_key, 'hex_compressed')
        wif_compress_enc_priv = bitcoin.encode_privkey(decoded_private_key, 'wif_compressed')
        '''
        logger.info('decimal_encoded_priv_key:{}'.format(dec_enc_priv))
        logger.info('bin_encoded_priv_key:{}'.format(bin_enc_priv))
        logger.info('bin_compressed_encoded_priv_key:{}'.format(bin_compress_enc_priv))
        # logger.info('hex_encoded_priv_key:{}'.format(hex_encoded_priv))
        logger.info('hex_compressed_encoded_priv_key:{}'.format(hex_compress_enc_priv))
        logger.info('wif_compressed_encoded_priv_key:{}'.format(wif_compress_enc_priv))
        '''
        # 添加后缀'01'以指示压缩的私钥
        compressed_priv = private_key + '01'

        # 从压缩私钥生成WIF格式（WIF压缩）
        wif_compressed_priv = bitcoin.encode_privkey(bitcoin.decode_privkey(compressed_priv, 'hex'), 'wif')
        wif_compressed_private_key_direct = bitcoin.encode_privkey(compressed_priv, 'wif')
        # logger.info('wif_compressed_private_key:{}'.format(wif_compressed_priv))
        # logger.info('wif_compressed_private_key_direct:{}'.format(wif_compressed_private_key_direct))
        # time.sleep(1 / 5)

        # 将EC生成器G与私钥相乘以获得公钥点
        public_key = bitcoin.fast_multiply(bitcoin.G, decoded_private_key)
        # logger.info('public_key:{}'.format(public_key))

        # 编码为十六进制，前缀为04
        hex_encoded_public_key = bitcoin.encode_pubkey(public_key, 'hex')  # uncompressed public key
        # logger.info('hex_encoded_public_key:{}'.format(hex_encoded_public_key))
        
        decimal_enc_pub = bitcoin.encode_pubkey(public_key, 'decimal')
        bin_enc_public_key = bitcoin.encode_pubkey(public_key, 'bin')
        bin_compress_encoded_pub = bitcoin.encode_pubkey(public_key, 'bin_compressed')
        # hex_compress_encoded_pub = bitcoin.encode_pubkey(public_key, 'hex_compressed')
        bin_electrum_enc_pub = bitcoin.encode_pubkey(public_key, 'bin_electrum')
        hex_electrum_enc_pub = bitcoin.encode_pubkey(public_key, 'hex_electrum')
        '''
        logger.info('decimal_encoded_public_key:{} | len:{}'.format(decimal_enc_pub, str(len(decimal_enc_pub))))
        logger.info('bin_encoded_public_key:{} | len:{}'.format(bin_enc_public_key, str(len(bin_enc_public_key))))
        logger.info('bin_compressed_encoded_public_key:{} | len:{}'.format(bin_compress_encoded_pub, str(len(bin_compress_encoded_pub))))
        # logger.info('hex_compressed_encoded_public_key:{}'.format(hex_compress_encoded_pub))
        logger.info('bin_electrum_encoded_public_key:{} | len:{}'.format(bin_electrum_enc_pub, str(len(bin_electrum_enc_pub))))
        logger.info('hex_electrum_encoded_public_key:{} | len:{}'.format(hex_electrum_enc_pub, str(len(hex_electrum_enc_pub))))
        '''
        
        # 压缩公钥，根据y是偶数还是奇数调整前缀
        (public_key_x, public_key_y) = public_key
        # logger.info('public_key:{}'.format(str(public_key)))
        # logger.info('public_key_x:{}'.format(public_key_x))
        # logger.info('public_key_y:{}'.format(public_key_y))
        if (public_key_y % 2) == 0:
            compressed_prefix = '02'
            # time.sleep(1 / 5)
        else:
            compressed_prefix = '03'
            # time.sleep(1 / 5)
        
        # 压缩后的公钥  compressed_public_key
        # hex_compress_pub == hex_compress_encoded_pub 
        hex_compress_pub = compressed_prefix + bitcoin.encode(public_key_x, 16)
        # logger.info('hex_compressed_public_key:{}'.format(hex_compress_pub))

        # 从公钥生成比特币地址
        # time.sleep(1 / 5)
        normal_addr = bitcoin.pubkey_to_address(public_key)
        '''
        logger.info("decimal addr:".format(bitcoin.pubkey_to_address(decimal_enc_pub)))
        logger.info("bin addr:".format(bitcoin.pubkey_to_address(str(bin_enc_public_key).encode('utf-8'))))
        logger.info("bin_compressed addr:".format(bitcoin.pubkey_to_address(bin_compress_encoded_pub)))
        logger.info("bin_electrum addr:".format(bitcoin.pubkey_to_address(str(bin_electrum_enc_pub).encode('utf_8'))))
        logger.info("hex_electrum addr:".format(bitcoin.pubkey_to_address(hex_electrum_enc_pub.encode('utf_8'))))
        logger.info('uncompressed_address:{}'.format(normal_addr))
        '''
        # 从压缩公钥生成压缩比特币地址
        # time.sleep(1 / 5)
        compress_addr = bitcoin.pubkey_to_address(hex_compress_pub.encode('utf-8'))
        # logger.info('compress_addr:{}'.format(compress_addr))
        
        return wif_enc_priv, normal_addr, wif_compressed_priv, compress_addr, private_key, hex_encoded_public_key, hex_compress_pub


def web_get_accountinfo(bitcoin_address):
    # 通过btc.com查询帐户信息
    while(1):
        try:
            url_str = ('https://chain.api.btc.com/v3/address/' + bitcoin_address)
            # r = requests.get(url_str)
            r = get_url(url_str)
            break
        except Exception as e:
            logger.info('connect error,retry...', e)
            time.sleep(5)
    r_json = json.loads(r)
    
    return r_json


def checkRandAndPrivExists(rand_key, priv_key, addr, tbl):
    select_sql = 'select rand_key from gen_wallet_{} t where t.rand_key= "{}" and priv_key="{}" and addr="{}"'.format(str(tbl), str(rand_key), str(priv_key), str(addr))
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
    # insert_gen_sql = 'insert into gen_wallet_(rand_key,priv_key,priv_key_type,addr) values(%s,%s,%s,%s)'
    # m = 0
    for i in range(1, num + 1):
        # logger.info("i = {}".format(str(i)))
        address_give = get_address()
        wif_encoded_private_key = address_give[0] 
        normal_addr = address_give[1]
        wif_compressed_private_key = address_give[2]
        compress_addr = address_give[3]
        rand_key = address_give[4]
        uncompress_pub = address_give[5]
        compress_pub = address_give[6]
        priv_key_hex = bitcoin.decode_privkey(rand_key, 'hex')
        tbl_idx = priv_key_hex % TABLE_NUM
        insert_gen_sql = 'insert into gen_wallet_' + str(tbl_idx) + '(rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key) values(%s,%s,%s,%s,%s,%s)'
        insert_err_sql = 'insert into error_info(rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key,tbl_idx,save_time) values(%s,%s,%s,%s,%s,%s,%s,now())'
        try:
            param.append([str(rand_key), str(wif_encoded_private_key), 'wif_normal', normal_addr, priv_key_hex, uncompress_pub])
            param.append([str(rand_key), str(wif_compressed_private_key), 'wif_compressed', compress_addr, priv_key_hex, compress_pub])
            insert_gen_count1 = conn.insertmany(insert_gen_sql, param)
            conn.end('commit')
            # logger.info('count:{} | i = {}'.format(str(insert_gen_count1), str(i)))
            param = []
        except Exception as e:
            error_param.append([str(rand_key), str(wif_encoded_private_key), 'wif_normal', normal_addr, priv_key_hex, uncompress_pub, str(tbl_idx)])
            error_param.append([str(rand_key), str(wif_compressed_private_key), 'wif_compressed', compress_addr, priv_key_hex, compress_pub, str(tbl_idx)])
            error_count = conn.insertmany(insert_err_sql, error_param)
            logger.error(e)
            logger.error('error count:{} | rand_key:{} | table:{}'.format(str(error_count), str(rand_key), str(tbl_idx)))
            conn.end('commit')
            error_param = []
        '''
            isNoramlExist = checkRandAndPrivExists(rand_key, wif_encoded_private_key, normal_addr, tbl_idx)
            isCompressExist = checkRandAndPrivExists(rand_key, wif_compressed_private_key, compress_addr, tbl_idx)
            if not (isNoramlExist or isCompressExist):
                param.append([str(rand_key), str(wif_encoded_private_key), 'wif_normal', normal_addr, priv_key_hex, uncompress_pub])
                param.append([str(rand_key), str(wif_compressed_private_key), 'wif_compressed', compress_addr, priv_key_hex, compress_pub])
                insert_gen_count1 = conn.insertmany(insert_gen_sql, param)
                conn.end('commit')
                #logger.info('saveWlt count:{} | i = {}'.format(str(insert_gen_count1), str(i)))
                param = []
        '''
        
    if len(param) > 0:
        insert_gen_count = conn.insertmany(insert_gen_sql, param)
        conn.end('commit')
        logger.info('saveWlt successful at last! count:{}'.format(str(insert_gen_count)))
    logger.info("saveWlt end at: {} ".format(time.ctime()))

'''
def btc_ad_save():
    # 输入地址及私钥信息
    address_give = get_address()

    logger.info("WIF格式私钥:{}".format(address_give[2]))
    time.sleep(1 / 5)
    account1 = web_get_accountinfo(address_give[0])
    logger.info("对应地址:{} | 帐户信息{}".format(address_give[0] , account1))

    time.sleep(1 / 5)
    logger.info("WIF格式压缩私钥:", address_give[3])
    time.sleep(1 / 5)
    account2 = web_get_accountinfo(address_give[1])
    logger.info("对应地址：{} | 帐户信息:{}".format({address_give[1]}, account2))
    time.sleep(1 / 5)

    return address_give
'''

if __name__ == '__main__':
    conn = MySQLConnPool('btc_new')
    config_logger()
    
    saveWlt(1000000)
    # get_address()
    
    conn.dispose(1)
