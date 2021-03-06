# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
查询转化信息中手机的归属地
@author: user
'''
import os, sys, json
import logging
import requests
import argparse
from importlib import reload
import brotli, random, time

reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/amap".replace('/', os.sep)

logger = logging.getLogger('poi_search')
LOG_FILE = 'poi_search.log'
# LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'
LOG_FORMATTER = '%(message)s'
AMAP_POI_SEARCH_API = 'https://restapi.amap.com/v3/place/text?key={}&keywords={}&city=010&page={}'
# AMAP_POI_SEARCH_API = 'https://restapi.amap.com/v3/place/text?key={}&keywords={}'
s = requests.Session()


def get_url(url, proxy=None):
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
        ACCEPT = "application/json"
        ACCEPT_ENCODING = "gzip, deflate, br"
        ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9"
        CONNECTION = "keep-alive"
        HOST = "restapi.amap.com"
        header = {"HOST":HOST, "METHOD":"GET", "User-Agent":UA_LST[random.randrange(0, len(UA_LST))], 'Cache-Control':'no-cache', "Accept":ACCEPT, "Accept-Encoding":ACCEPT_ENCODING, "Accept-Language":ACCEPT_LANGUAGE, "Connection":CONNECTION}
        r = s.get(url, headers=header)
        sc = r.status_code
        if sc == 200:
            r.encoding = 'utf-8'
            '''
            logger.info('headers in below:\n')
            header_lst = r.headers
            for k, v in header_lst.items():
                logger.info(k + "=" + v)
            logger.info('encoding:\n' + r.encoding)
            '''
            key = 'Content-Encoding'
            # print(response.headers[key])
            if(key in r.headers and r.headers['Content-Encoding'] == 'br'):
                data = brotli.decompress(r.content)
                data1 = data.decode('utf-8')
                # logger.info('data1：' + data1)
                return data1
            # logger.info('r.text:\n' + r.text)
            return r.text
        else:
            return None
    except Exception as e:
        logger.error(e)
        return None


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


def getPoiLocation(key, kw, page=1):
    
    real_api = AMAP_POI_SEARCH_API.format(key, kw, str(page))
    resp_json = get_url(real_api)
    respObj = json.loads(resp_json)
    
    return respObj


def savePoiInfo(key, kw):
    poi_info = getPoiLocation(key, kw)
    total_num = poi_info['count']
    
    total_page = int(int(total_num) / 20 + 1)
    for p in range(1, total_page + 1):
        poiinfo = getPoiLocation(key, kw, p)
        pois = poiinfo['pois']
        for poi in pois:
            name = poi['name']
            location = poi['location']
            logger.info('{}|{}'.format(str(name),str(location)))


def init_parser():
    # logger.info('start parse arguments')
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key",
                        type=str,
                        dest='apikey',
                        required=True,
                        help="api_key"
                        )
    parser.add_argument("-kw", "--keyword",
                        type=str,
                        dest='keyword',
                        required=True,
                        help="kw"
                        )
    return parser


if __name__ == '__main__':
    config_logger()
    
    parser = init_parser()
    args = parser.parse_args()
    key = args.apikey
    kw = args.keyword
    # kw = kw.encode('utf-8')
    
    savePoiInfo(key, kw)
    
