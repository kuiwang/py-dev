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
import requests, json, secrets
from bitcoinutils.setup import setup
from bitcoinutils.script import Script
from bitcoinutils.keys import P2wpkhAddress, P2wshAddress, P2shAddress, PrivateKey, PublicKey

reload(sys)
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
TABLE_NUM = 10000
RECORD_LIMIT = 10000
logger = logging.getLogger('walt_gen_btcutil')
LOG_FILE = 'walt_gen_btcutil.log'
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


def gen_address():
    # setup('mainnet')
    # 生成随机私钥
    valid_private_key = False
    while not valid_private_key:
        # private_key = bitcoin.random_key()
        bits = secrets.randbits(256)
        # 46518555179467323509970270980993648640987722172281263586388328188640792550961
        bits_hex = hex(bits)
        # 0x66d891b5ed7f51e5044be6a7ebe4e2eae32b960f5aa0883f7cc0ce4fd6921e31
        private_key = bits_hex[2:]
        # 66d891b5ed7f51e5044be6a7ebe4e2eae32b960f5aa0883f7cc0ce4fd6921e31
        decoded_private_key = bitcoin.decode_privkey(private_key, 'hex')
        valid_private_key = 0 < decoded_private_key < bitcoin.N
        
        # normal private key
        uncompressed_priv_key = bitcoin.encode_privkey(decoded_private_key, 'wif')
        priv = PrivateKey.from_wif(uncompressed_priv_key)
        
        normal_priv_key = priv.to_wif(compressed=False)
        compressed_priv_key = priv.to_wif(compressed=True)
        
        pub = priv.get_public_key()
        uncompressed_pub = pub.to_hex(compressed=False)
        compressed_pub = pub.to_hex(compressed=True)
        
        uncompressed_addr = pub.get_address(compressed=False)
        uncompressed_address = uncompressed_addr.to_address()  # wif_normal address
        compressed_addr = pub.get_address(compressed=True)
        compressed_address = compressed_addr.to_address()  # wif_compressed address
        
        segwit_addr = pub.get_segwit_address()
        segwit_address = segwit_addr.to_address()
        segwit_hash = segwit_addr.to_hash()

        # wrap in P2SH address
        uncomp_addr_2spk = uncompressed_addr.to_script_pub_key()
        uncomp_p2sh_addr = P2shAddress.from_script(uncomp_addr_2spk).to_address()
        uncomp_addr_2spk_hex = uncomp_addr_2spk.to_hex()
        
        comp_addr_2spk = compressed_addr.to_script_pub_key()
        comp_p2sh_addr = P2shAddress.from_script(comp_addr_2spk).to_address()
        comp_addr_2spk_hex = comp_addr_2spk.to_hex()
        
        seg_addr_2spk = segwit_addr.to_script_pub_key()
        segwit_p2sh_addr = P2shAddress.from_script(seg_addr_2spk).to_address()
        seg_addr_2spk_hex = seg_addr_2spk.to_hex()
    
        # display P2WSH
        p2wpkh_key = PrivateKey.from_wif(uncompressed_priv_key)
        pswpkh_pub_hex = p2wpkh_key.get_public_key().to_hex()
        script = Script(['OP_1', p2wpkh_key.get_public_key().to_hex(), 'OP_1', 'OP_CHECKMULTISIG'])
        p2wsh_addr = P2wshAddress.from_script(script)
        p2wsh_address = p2wsh_addr.to_address()
    
        # display P2SH-P2WSH
        p2sh_pub = p2wsh_addr.to_script_pub_key()
        p2sh_pub_hex = p2sh_pub.to_hex()
        p2sh_p2wsh_addr = P2shAddress.from_script(p2sh_pub)
        p2sh_p2wsh_address = p2sh_p2wsh_addr.to_address()
        
        return uncompressed_priv_key, uncompressed_address, compressed_priv_key, compressed_address, private_key, uncompressed_pub, compressed_pub, decoded_private_key, segwit_address, segwit_hash, uncomp_p2sh_addr, uncomp_addr_2spk_hex, comp_p2sh_addr, comp_addr_2spk_hex, segwit_p2sh_addr, seg_addr_2spk_hex, p2wsh_address, pswpkh_pub_hex, p2sh_p2wsh_address, p2sh_pub_hex


def dev_gen_address():
    setup('mainnet')
    # 生成随机私钥
    valid_private_key = False
    while not valid_private_key:
        private_key = bitcoin.random_key()
        private_key = '41a4fefeff8dbe1cc45aa1625f0017afd83f2099116edef58ebc4acc8666e2b0'
        decoded_private_key = bitcoin.decode_privkey(private_key, 'hex')
        valid_private_key = 0 < decoded_private_key < bitcoin.N
        # logger.info("decoded_priv_key:{}".format(decoded_private_key))
        
        # normal private key
        uncompressed_priv_key = bitcoin.encode_privkey(decoded_private_key, 'wif')
        priv = PrivateKey.from_wif(uncompressed_priv_key)
        
        normal_priv_key = priv.to_wif(compressed=False)
        compressed_priv_key = priv.to_wif(compressed=True)
        # logger.info("uncompress priv key:{}".format(uncompressed_priv_key))
        # logger.info("compressed_priv_key:{}".format(compressed_priv_key))
        
        pub = priv.get_public_key()
        uncompressed_pub = pub.to_hex(compressed=False)
        compressed_pub = pub.to_hex(compressed=True)
        # logger.info("uncompressed_pub:{}".format(uncompressed_pub))
        # logger.info("compress pub:{}".format(compressed_pub))
        
        uncompressed_addr = pub.get_address(compressed=False)
        uncompressed_address = uncompressed_addr.to_address()  # wif_normal address
        compressed_addr = pub.get_address(compressed=True)
        compressed_address = compressed_addr.to_address()  # wif_compressed address
        # logger.info("uncompressed_addr:{}".format(uncompressed_address))
        # logger.info("compressed_addr:{}".format(compressed_address))
        # logger.info("uncompressed_addr_hash:{}".format(uncompressed_addr.to_hash160()))
        # logger.info("compressed_addr_hash:{}".format(compressed_addr.to_hash160()))
        
        segwit_addr = pub.get_segwit_address()
        segwit_address = segwit_addr.to_address()
        # logger.info("P2WPKH:{}".format(segwit_address))
        segwit_hash = segwit_addr.to_hash()
        # logger.info("segwit_hash:{}".format(segwit_hash))
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
        # logger.info('uncomp_addr_2spk:{}'.format(uncomp_addr_2spk_hex))
        # logger.info("uncomp_p2sh_addr:{}".format(uncomp_p2sh_addr))
        comp_addr_2spk = compressed_addr.to_script_pub_key()
        comp_p2sh_addr = P2shAddress.from_script(comp_addr_2spk).to_address()
        comp_addr_2spk_hex = comp_addr_2spk.to_hex()
        # logger.info('comp_addr_2spk:{}'.format(comp_addr_2spk_hex))
        # logger.info("comp_p2sh_addr:{}".format(comp_p2sh_addr))
        
        seg_addr_2spk = segwit_addr.to_script_pub_key()
        segwit_p2sh_addr = P2shAddress.from_script(seg_addr_2spk).to_address()
        seg_addr_2spk_hex = seg_addr_2spk.to_hex()
        # logger.info('seg_addr_2spk_hex:{}'.format(seg_addr_2spk_hex))
        # logger.info("addr4 P2SH(P2WPKH):{}".format(segwit_p2sh_addr))
    
        # display P2WSH
        p2wpkh_key = PrivateKey.from_wif(uncompressed_priv_key)
        pswpkh_pub_hex = p2wpkh_key.get_public_key().to_hex()
        # logger.info("pswpkh_pub_hex:{}".format(pswpkh_pub_hex))
        script = Script(['OP_1', p2wpkh_key.get_public_key().to_hex(), 'OP_1', 'OP_CHECKMULTISIG'])
        p2wsh_addr = P2wshAddress.from_script(script)
        p2wsh_address = p2wsh_addr.to_address()
        # logger.info("P2WSH of P2PK:{}".format(p2wsh_address))
    
        # display P2SH-P2WSH
        p2sh_pub = p2wsh_addr.to_script_pub_key()
        p2sh_pub_hex = p2sh_pub.to_hex()
        # logger.info("p2sh_pub_hex:{}".format(p2sh_pub_hex))
        p2sh_p2wsh_addr = P2shAddress.from_script(p2sh_pub)
        p2sh_p2wsh_address = p2sh_p2wsh_addr.to_address()
        # logger.info("P2SH(P2WSH of P2PK):{}".format(p2sh_p2wsh_address))
        
        return uncompressed_priv_key, uncompressed_address, compressed_priv_key, compressed_address, private_key, uncompressed_pub, compressed_pub, decoded_private_key, segwit_address, segwit_hash, uncomp_p2sh_addr, uncomp_addr_2spk_hex, comp_p2sh_addr, comp_addr_2spk_hex, segwit_p2sh_addr, seg_addr_2spk_hex, p2wsh_address, pswpkh_pub_hex, p2sh_p2wsh_address, p2sh_pub_hex

'''
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
'''


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
    for i in range(1, num + 1):
        # logger.info("i = {}".format(str(i)))
        address_give = gen_address()
        wif_encoded_private_key = address_give[0] 
        normal_addr = address_give[1]
        wif_compressed_private_key = address_give[2]
        compress_addr = address_give[3]
        rand_key = address_give[4]
        uncompress_pub = address_give[5]
        compress_pub = address_give[6]
        # priv_key_hex = bitcoin.decode_privkey(rand_key, 'hex')
        priv_key_hex = address_give[7]
        segwit_address = address_give[8]
        segwit_hash = address_give[9]
        uncomp_p2sh_addr = address_give[10]
        uncomp_addr_2spk_hex = address_give[11]
        comp_p2sh_addr = address_give[12]
        comp_addr_2spk_hex = address_give[13]
        segwit_p2sh_addr = address_give[14]
        seg_addr_2spk_hex = address_give[15]
        p2wsh_address = address_give[16]
        pswpkh_pub_hex = address_give[17]
        p2sh_p2wsh_address = address_give[18]
        p2sh_pub_hex = address_give[19]
        tbl_idx = priv_key_hex % TABLE_NUM
        insert_gen_sql = 'insert into gen_wallet_' + str(tbl_idx) + '(rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key) values(%s,%s,%s,%s,%s,%s)'
        insert_err_sql = 'insert into error_info(rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key,tbl_idx,save_time) values(%s,%s,%s,%s,%s,%s,%s,now())'
        try:
            param.append([str(rand_key), str(wif_encoded_private_key), 'wif_normal', normal_addr, priv_key_hex, uncompress_pub])
            param.append([str(rand_key), str(wif_compressed_private_key), 'wif_compressed', compress_addr, priv_key_hex, compress_pub])
            param.append([str(rand_key), str(wif_compressed_private_key), 'segwit_addr', segwit_address, priv_key_hex, segwit_hash])
            param.append([str(rand_key), str(wif_compressed_private_key), 'uncompressed_p2sh_addr', uncomp_p2sh_addr, priv_key_hex, uncomp_addr_2spk_hex])
            param.append([str(rand_key), str(wif_compressed_private_key), 'compressed_p2sh_addr', comp_p2sh_addr, priv_key_hex, comp_addr_2spk_hex])
            param.append([str(rand_key), str(wif_compressed_private_key), 'segwit_p2sh_addr', segwit_p2sh_addr, priv_key_hex, seg_addr_2spk_hex])
            param.append([str(rand_key), str(wif_compressed_private_key), 'p2wsh_addr', p2wsh_address, priv_key_hex, pswpkh_pub_hex])
            param.append([str(rand_key), str(wif_compressed_private_key), 'p2sh_p2wsh_addr', p2sh_p2wsh_address, priv_key_hex, p2sh_pub_hex])
            insert_gen_count1 = conn.insertmany(insert_gen_sql, param)
            conn.end('commit')
            logger.info('i={} | count:{}'.format(str(i), str(insert_gen_count1)))
            # logger.info('i={}'.format(str(i)))
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


def saveWltIgnoreTbl(num):
    logger.info("saveWltIgnoreTbl start at: {}".format(time.ctime()))
    param = []
    error_param = []
    for i in range(1, num + 1):
        for j in range(1000, TABLE_NUM):
            insert_gen_sql = 'insert into gen_wallet_' + str(j) + '(rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key) values(%s,%s,%s,%s,%s,%s)'
            total = 0
            for k in range(1, RECORD_LIMIT + 1):
                address_give = gen_address()
                wif_encoded_private_key = address_give[0] 
                normal_addr = address_give[1]
                wif_compressed_private_key = address_give[2]
                compress_addr = address_give[3]
                rand_key = address_give[4]
                uncompress_pub = address_give[5]
                compress_pub = address_give[6]
                priv_key_hex = address_give[7]
                segwit_address = address_give[8]
                segwit_hash = address_give[9]
                uncomp_p2sh_addr = address_give[10]
                uncomp_addr_2spk_hex = address_give[11]
                comp_p2sh_addr = address_give[12]
                comp_addr_2spk_hex = address_give[13]
                segwit_p2sh_addr = address_give[14]
                seg_addr_2spk_hex = address_give[15]
                p2wsh_address = address_give[16]
                pswpkh_pub_hex = address_give[17]
                p2sh_p2wsh_address = address_give[18]
                p2sh_pub_hex = address_give[19]
                tbl_idx = priv_key_hex % TABLE_NUM
                insert_err_sql = 'insert into error_info(rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key,tbl_idx,save_time) values(%s,%s,%s,%s,%s,%s,%s,now())'
                try:
                    param.append([str(rand_key), str(wif_encoded_private_key), 'wif_normal', normal_addr, priv_key_hex, uncompress_pub])
                    param.append([str(rand_key), str(wif_compressed_private_key), 'wif_compressed', compress_addr, priv_key_hex, compress_pub])
                    param.append([str(rand_key), str(wif_compressed_private_key), 'segwit_addr', segwit_address, priv_key_hex, segwit_hash])
                    param.append([str(rand_key), str(wif_compressed_private_key), 'uncompressed_p2sh_addr', uncomp_p2sh_addr, priv_key_hex, uncomp_addr_2spk_hex])
                    param.append([str(rand_key), str(wif_compressed_private_key), 'compressed_p2sh_addr', comp_p2sh_addr, priv_key_hex, comp_addr_2spk_hex])
                    param.append([str(rand_key), str(wif_compressed_private_key), 'segwit_p2sh_addr', segwit_p2sh_addr, priv_key_hex, seg_addr_2spk_hex])
                    param.append([str(rand_key), str(wif_compressed_private_key), 'p2wsh_addr', p2wsh_address, priv_key_hex, pswpkh_pub_hex])
                    param.append([str(rand_key), str(wif_compressed_private_key), 'p2sh_p2wsh_addr', p2sh_p2wsh_address, priv_key_hex, p2sh_pub_hex])
                    len_p = len(param)
                    if ((len_p % RECORD_LIMIT) == 0):
                        insert_gen_count1 = conn.insertmany(insert_gen_sql, param)
                        total = total + insert_gen_count1
                        conn.end('commit')
                        logger.info('i={} | table:{} | k={} | count:{} | total:{}'.format(str(i), str(j), str(k), str(insert_gen_count1), str(total)))
                        param = []
                    # logger.info('i={}'.format(str(i)))
                except Exception as e:
                    error_param.append([str(rand_key), str(wif_encoded_private_key), 'wif_normal', normal_addr, priv_key_hex, uncompress_pub, str(tbl_idx)])
                    error_param.append([str(rand_key), str(wif_compressed_private_key), 'wif_compressed', compress_addr, priv_key_hex, compress_pub, str(tbl_idx)])
                    error_count = conn.insertmany(insert_err_sql, error_param)
                    logger.error(e)
                    # logger.error('error count:{} | rand_key:{} | table:{}'.format(str(error_count), str(rand_key), str(tbl_idx)))
                    logger.error('error count:{} | rand_key:{} | table:{}'.format(str(error_count), str(rand_key), str(j)))
                    conn.end('commit')
                    error_param = []
        if len(param) > 0:
            insert_gen_count = conn.insertmany(insert_gen_sql, param)
            total = total + insert_gen_count
            conn.end('commit')
            param = []
            logger.info('saveWltIgnoreTbl ,i={} | table:{} | count:{} | total_now:{}'.format(str(i), str(j), str(insert_gen_count), str(total)))
    logger.info("saveWlt end at: {} ".format(time.ctime()))



def saveWltIgnoreEverything(num):
    logger.info("saveWltIgnoreEverything start at: {}".format(time.ctime()))
    param = []
    error_param = []
    for i in range(1, num + 1):
        insert_gen_sql = 'insert into gen_wallet_dev(rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key) values(%s,%s,%s,%s,%s,%s)'
        total = 0
        address_give = gen_address()
        wif_encoded_private_key = address_give[0] 
        normal_addr = address_give[1]
        wif_compressed_private_key = address_give[2]
        compress_addr = address_give[3]
        rand_key = address_give[4]
        uncompress_pub = address_give[5]
        compress_pub = address_give[6]
        priv_key_hex = address_give[7]
        segwit_address = address_give[8]
        segwit_hash = address_give[9]
        uncomp_p2sh_addr = address_give[10]
        uncomp_addr_2spk_hex = address_give[11]
        comp_p2sh_addr = address_give[12]
        comp_addr_2spk_hex = address_give[13]
        segwit_p2sh_addr = address_give[14]
        seg_addr_2spk_hex = address_give[15]
        p2wsh_address = address_give[16]
        pswpkh_pub_hex = address_give[17]
        p2sh_p2wsh_address = address_give[18]
        p2sh_pub_hex = address_give[19]
        tbl_idx = priv_key_hex % TABLE_NUM
        insert_err_sql = 'insert into error_info(rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key,tbl_idx,save_time) values(%s,%s,%s,%s,%s,%s,%s,now())'
        try:
            param.append([str(rand_key), str(wif_encoded_private_key), 'wif_normal', normal_addr, priv_key_hex, uncompress_pub])
            param.append([str(rand_key), str(wif_compressed_private_key), 'wif_compressed', compress_addr, priv_key_hex, compress_pub])
            param.append([str(rand_key), str(wif_compressed_private_key), 'segwit_addr', segwit_address, priv_key_hex, segwit_hash])
            param.append([str(rand_key), str(wif_compressed_private_key), 'uncompressed_p2sh_addr', uncomp_p2sh_addr, priv_key_hex, uncomp_addr_2spk_hex])
            param.append([str(rand_key), str(wif_compressed_private_key), 'compressed_p2sh_addr', comp_p2sh_addr, priv_key_hex, comp_addr_2spk_hex])
            param.append([str(rand_key), str(wif_compressed_private_key), 'segwit_p2sh_addr', segwit_p2sh_addr, priv_key_hex, seg_addr_2spk_hex])
            param.append([str(rand_key), str(wif_compressed_private_key), 'p2wsh_addr', p2wsh_address, priv_key_hex, pswpkh_pub_hex])
            param.append([str(rand_key), str(wif_compressed_private_key), 'p2sh_p2wsh_addr', p2sh_p2wsh_address, priv_key_hex, p2sh_pub_hex])
            len_p = len(param)
            if ((len_p % RECORD_LIMIT) == 0):
                insert_gen_count1 = conn.insertmany(insert_gen_sql, param)
                total = total + insert_gen_count1
                conn.end('commit')
                logger.info('i={} | total:{}'.format(str(i), str(total)))
                param = []
            # logger.info('i={}'.format(str(i)))
        except Exception as e:
            error_param.append([str(rand_key), str(wif_encoded_private_key), 'wif_normal', normal_addr, priv_key_hex, uncompress_pub, str(tbl_idx)])
            error_param.append([str(rand_key), str(wif_compressed_private_key), 'wif_compressed', compress_addr, priv_key_hex, compress_pub, str(tbl_idx)])
            error_count = conn.insertmany(insert_err_sql, error_param)
            logger.error(e)
            # logger.error('error count:{} | rand_key:{} | table:{}'.format(str(error_count), str(rand_key), str(tbl_idx)))
            logger.error('error count:{} | rand_key:{} '.format(str(error_count), str(rand_key)))
            conn.end('commit')
            error_param = []
    if len(param) > 0:
        insert_gen_count = conn.insertmany(insert_gen_sql, param)
        total = total + insert_gen_count
        conn.end('commit')
        param = []
        logger.info('saveWltIgnoreTbl ,i={} | count:{} '.format(str(i), str(insert_gen_count)))
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
    setup('mainnet')
    config_logger()
    conn = MySQLConnPool('btc_new')
    
    #saveWlt(900000000)
    saveWltIgnoreTbl(100)
    #saveWltIgnoreEverything(90000000)
    
    # get_address()
    
    conn.dispose(1)
