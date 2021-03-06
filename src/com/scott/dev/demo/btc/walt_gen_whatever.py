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
import bitcoin, random, secrets
import requests, json
from bitcoinutils.setup import setup
from bitcoinutils.script import Script
from bitcoinutils.keys import P2wpkhAddress, P2wshAddress, P2shAddress, PrivateKey, PublicKey

reload(sys)
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
TABLE_NUM = 1000
logger = logging.getLogger('walt_whatever_gen')
LOG_FILE = 'walt_whatever_gen.log'
# LOG_FORMATTER = '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'
LOG_FORMATTER = '%(lineno)d - %(message)s'
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


def gen_address_new():
    setup('mainnet')
    # 生成随机私钥
    valid_private_key = False
    while not valid_private_key:
        # private_key = bitcoin.random_key()
        bits = secrets.randbits(256)
        # 46518555179467323509970270980993648640987722172281263586388328188640792550961
        bits_hex = hex(bits)
        # 0x66d891b5ed7f51e5044be6a7ebe4e2eae32b960f5aa0883f7cc0ce4fd6921e31
        private_key = bits_hex[2:]
        private_key = '0000000000000000000000000000000000000000000000000000000000000001'
        # 66d891b5ed7f51e5044be6a7ebe4e2eae32b960f5aa0883f7cc0ce4fd6921e31
        decoded_private_key = bitcoin.decode_privkey(private_key, 'hex')
        valid_private_key = 0 < decoded_private_key < bitcoin.N
        
        # normal private key
        uncompressed_priv_key = bitcoin.encode_privkey(decoded_private_key, 'wif')
        priv = PrivateKey.from_wif(uncompressed_priv_key)
        
        
        normal_priv_key = priv.to_wif(compressed=False)
        logger.info("normal_priv_key:{}".format(normal_priv_key))
        compressed_priv_key = priv.to_wif(compressed=True)
        logger.info("compressed_priv_key:{}".format(compressed_priv_key))
        
        pub = priv.get_public_key()
        uncompressed_pub = pub.to_hex(compressed=False)
        compressed_pub = pub.to_hex(compressed=True)
        
        uncompressed_addr = pub.get_address(compressed=False)
        uncompressed_address = uncompressed_addr.to_address()  # wif_normal address
        logger.info('uncompressed_address:{}'.format(uncompressed_address))
        compressed_addr = pub.get_address(compressed=True)
        compressed_address = compressed_addr.to_address()  # wif_compressed address
        logger.info('compressed_address:{}'.format(compressed_address))
        
        segwit_addr = pub.get_segwit_address()
        segwit_address = segwit_addr.to_address()
        logger.info('compressed_btc1_addr:{}'.format(segwit_address))
        segwit_hash = segwit_addr.to_hash()
        
        uncompressed_btc1_segwit_addr = pub.get_segwit_address_uncompressed()
        uncompressed_btc1_addr = uncompressed_btc1_segwit_addr.to_address()
        logger.info('uncompressed_btc1_addr:{}'.format(uncompressed_btc1_addr))

        # wrap in P2SH address
        uncomp_addr_2spk = uncompressed_addr.to_script_pub_key()
        uncomp_p2sh_addr = P2shAddress.from_script(uncomp_addr_2spk).to_address()
        logger.info('uncomp_p2sh_addr:{}'.format(uncomp_p2sh_addr))
        uncomp_addr_2spk_hex = uncomp_addr_2spk.to_hex()
        
        comp_addr_2spk = compressed_addr.to_script_pub_key()
        comp_p2sh_addr = P2shAddress.from_script(comp_addr_2spk).to_address()
        logger.info('comp_p2sh_addr:{}'.format(comp_p2sh_addr))
        comp_addr_2spk_hex = comp_addr_2spk.to_hex()
        
        seg_addr_2spk = segwit_addr.to_script_pub_key()
        segwit_p2sh_addr = P2shAddress.from_script(seg_addr_2spk).to_address()
        logger.info('compressed_3_prefix_addr:{}'.format(segwit_p2sh_addr))
        uncompress_addr_2spk = uncompressed_btc1_segwit_addr.to_script_pub_key()
        uncompress_p2sh_addr =P2shAddress.from_script(uncompress_addr_2spk).to_address()
        logger.info('uncompressed_3_prefix_addr:{}'.format(uncompress_p2sh_addr))
        seg_addr_2spk_hex = seg_addr_2spk.to_hex()
    
        # display P2WSH
        p2wpkh_key = PrivateKey.from_wif(uncompressed_priv_key)
        pswpkh_pub_hex = p2wpkh_key.get_public_key().to_hex()
        script = Script(['OP_1', p2wpkh_key.get_public_key().to_hex(), 'OP_1', 'OP_CHECKMULTISIG'])
        p2wsh_addr = P2wshAddress.from_script(script)
        p2wsh_address = p2wsh_addr.to_address()
        logger.info('p2wsh_address:{}'.format(p2wsh_address))
    
        # display P2SH-P2WSH
        p2sh_pub = p2wsh_addr.to_script_pub_key()
        p2sh_pub_hex = p2sh_pub.to_hex()
        p2sh_p2wsh_addr = P2shAddress.from_script(p2sh_pub)
        p2sh_p2wsh_address = p2sh_p2wsh_addr.to_address()
        logger.info('p2sh_p2wsh_address:{}'.format(p2sh_p2wsh_address))
        
        return uncompressed_priv_key, uncompressed_address, compressed_priv_key, compressed_address, private_key, uncompressed_pub, compressed_pub, decoded_private_key, segwit_address, segwit_hash, uncomp_p2sh_addr, uncomp_addr_2spk_hex, comp_p2sh_addr, comp_addr_2spk_hex, segwit_p2sh_addr, seg_addr_2spk_hex, p2wsh_address, pswpkh_pub_hex, p2sh_p2wsh_address, p2sh_pub_hex


def get_address():
    # 生成随机私钥
    valid_private_key = False
    while not valid_private_key:
        private_key = bitcoin.random_key()
        # private_key = '0000000000000000000000000000000000000000000000000000000000000001'
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
        
        logger.info('decimal_encoded_public_key:{} | len:{}'.format(decimal_enc_pub, str(len(decimal_enc_pub))))
        logger.info('bin_encoded_public_key:{} | len:{}'.format(bin_enc_public_key, str(len(bin_enc_public_key))))
        logger.info('bin_compressed_encoded_public_key:{} | len:{}'.format(bin_compress_encoded_pub, str(len(bin_compress_encoded_pub))))
        # logger.info('hex_compressed_encoded_public_key:{}'.format(hex_compress_encoded_pub))
        logger.info('bin_electrum_encoded_public_key:{} | len:{}'.format(bin_electrum_enc_pub, str(len(bin_electrum_enc_pub))))
        logger.info('hex_electrum_encoded_public_key:{} | len:{}'.format(hex_electrum_enc_pub, str(len(hex_electrum_enc_pub))))
        
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
        logger.info('hex_compressed_public_key:{}'.format(hex_compress_pub))

        # 从公钥生成比特币地址
        # time.sleep(1 / 5)
        normal_addr = bitcoin.pubkey_to_address(public_key)
        
        logger.info("decimal addr:".format(bitcoin.pubkey_to_address(decimal_enc_pub)))
        logger.info("bin addr:".format(bitcoin.pubkey_to_address(str(bin_enc_public_key).encode('utf-8'))))
        logger.info("bin_compressed addr:".format(bitcoin.pubkey_to_address(bin_compress_encoded_pub)))
        logger.info("bin_electrum addr:".format(bitcoin.pubkey_to_address(str(bin_electrum_enc_pub).encode('utf_8'))))
        logger.info("hex_electrum addr:".format(bitcoin.pubkey_to_address(hex_electrum_enc_pub.encode('utf_8'))))
        logger.info('uncompressed_address:{}'.format(normal_addr))
        
        # 从压缩公钥生成压缩比特币地址
        # time.sleep(1 / 5)
        compress_addr = bitcoin.pubkey_to_address(hex_compress_pub.encode('utf-8'))
        logger.info('compress_addr:{}'.format(compress_addr))
        
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
    select_sql = 'select rand_key from gen_wallet t where t.rand_key= "{}" and priv_key="{}" and addr="{}"'.format(str(rand_key), str(priv_key), str(addr))
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
    # num = int(num)
    times = 0
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
        insert_gen_sql = 'insert into gen_wallet(rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key) values(%s,%s,%s,%s,%s,%s)'
        insert_err_sql = 'insert into error_info(rand_key,priv_key,priv_key_type,addr,priv_key_hex,pub_key,save_time) values(%s,%s,%s,%s,%s,%s,now())'
        try:
            param.append([str(rand_key), str(wif_encoded_private_key), 'wif_normal', normal_addr, priv_key_hex, uncompress_pub])
            param.append([str(rand_key), str(wif_compressed_private_key), 'wif_compressed', compress_addr, priv_key_hex, compress_pub])
            size = len(param)
            if ((size % 10000) == 0):
                insert_gen_count1 = conn.insertmany(insert_gen_sql, param)
                conn.end('commit')
                times = times + 1
                logger.info('times:{} | count:{}'.format(str(times), str(insert_gen_count1)))
                param = []
        except Exception as e:
            error_param.append([str(rand_key), str(wif_encoded_private_key), 'wif_normal', normal_addr, priv_key_hex, uncompress_pub])
            error_param.append([str(rand_key), str(wif_compressed_private_key), 'wif_compressed', compress_addr, priv_key_hex, compress_pub])
            error_count = conn.insertmany(insert_err_sql, error_param)
            logger.error(e)
            logger.error('error count:{} | rand_key:{} '.format(str(error_count), str(rand_key)))
            conn.end('commit')
            error_param = []
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
    processlist = []
    # conn = MySQLConnPool('btc_new')
    config_logger()
    
    # saveWlt(1)
    res = gen_address_new()
    
    # conn.dispose(1)
