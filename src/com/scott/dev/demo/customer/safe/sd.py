# -*- coding:utf-8 -*-

import requests
import os, sys, logging
import argparse, json, hashlib
import datetime

reload(sys)  
sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/".replace('/', os.sep)
logger = logging.getLogger('safemodeLogger')
LOG_FILE = 'safemode.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

s = requests.Session()

API_KEY = "BYtwBBiCGJ0HAS86"


def config_logger():
    logger.setLevel(logging.DEBUG)
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


def post_url(url, send_data):
    try:
        HEADER_UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        HEADER_METHOD = "POST"
        HEADER_ACCEPT = "text/json"
        header = {"User-Agent":HEADER_UA, "method":HEADER_METHOD, "Accept":HEADER_ACCEPT}
        r = s.post(url, data=send_data, headers=header)
        status = r.status_code
        if status == 200:
            return r.content
        # logger.info("response:" + txt)
    except Exception, e:
        return ""
        logger.error(e)


def init_parser():
    logger.info('start parse arguments')
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url",
                        type=str,
                        dest='url',
                        required=True,
                        help="API提交地址"
                        )
    parser.add_argument("-a", "--account",
                        type=int,
                        dest='account',
                        required=True,
                        help="输入账户ID"
                        )
    parser.add_argument("-f", "--file",
                        type=str,
                        dest='file',
                        required=True,
                        help="输入文件完整路径"
                        )
    return parser


def smtData(url, account, filename):
    items = []
    i = 0
    usr_info = {}
    f = open(filename, 'r')
    cont = f.readline().strip()
    m2 = hashlib.md5()
    with open(filename, 'r') as f:
        for cont in f:
            cont = cont.strip()
            # logger.info("content:" + cont)
            if len(cont) != 32:
                continue
            i = i + 1
            usr_info = {"idtype":"txxwdevid", "uid":cont}
            items.append(usr_info)
            if(i % 100 == 0):
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                m2.update(str(account) + str(now) + str(API_KEY))
                sign = m2.hexdigest()
                post_body = {
                    "aid":account,
                    "time":now,
                    "sign":sign,
                    "items":items
                }
                json_post_body = json.dumps(post_body).encode("utf-8")
                items = []
                # post_url(url, json_post_body)
                logger.info("第" + str(i / 100) + "次: 已处理" + str(i) + "条 |" + str(account) + " | " + str(now) + " | " + sign + " |post data:" + str(json_post_body))
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        m2.update(str(account) + str(now) + str(API_KEY))
        sign = m2.hexdigest()
        post_body = {
            "aid":account,
            "time":now,
            "sign":sign,
            "items":items
        }
        json_post_body = json.dumps(post_body).encode("utf-8")
        logger.info("第" + str(i / 100) + "次: 已处理" + str(i) + "条 |" + str(account) + " | " + str(now) + " | " + sign + " |post data:" + str(json_post_body))
        # post_url(api, post_data)


if __name__ == '__main__':
    config_logger()
    parser = init_parser()
    args = parser.parse_args()
    api_url = args.url
    account_id = args.account
    file_name = args.file
    smtData(api_url, account_id, file_name)
