# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
生成城市配置文件
@author: user
'''
import os, sys
import logging
import requests, json
from bs4 import BeautifulSoup 
from importlib import reload
import random, time
import brotli

reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "E:/data/priv".replace('/', os.sep)
PY_IMG_PATH = "E:/data/priv/qunar/flight".replace('/', os.sep)
logger = logging.getLogger('flight_city')
LOG_FILE = 'flight_city.log'
LOG_FORMATTER = '%(message)s'
# IMG_URL='https://cdn.zampdsp.com/vip/760/flight/dalian/1.jpg'
IMG_PREFIX = "https://cdn.zampdsp.com/vip/760/flight/{}/{}.jpg"
JSON_CONF_FILE = PY_GEN_PATH + "/flight.json"

CITY_DICT = {
'北海':'beihai',
'北京':'beijing',
'长春':'changchun',
'长沙':'changsha',
'成都':'chengdu',
'重庆':'chongqing',
'大理':'dali',
'大连':'dalian',
'福州':'fuzhou',
'广州':'guangzhou',
'桂林':'guilin',
'贵阳':'guiyang',
'哈尔滨':'haerbin',
'海口':'haikou',
'杭州':'hangzhou',
'合肥':'hefei',
'呼和浩特':'huhehaote',
'揭阳':'jieyang',
'济南':'jinan',
'昆明':'kunming',
'兰州':'lanzhou',
'拉萨':'lasa',
'丽江':'lijiang',
'绵阳':'mianyang',
'南昌':'nanchang',
'南京':'nanjing',
'南宁':'nanning',
'宁波':'ningbo',
'青岛':'qingdao',
'泉州':'quanzhou',
'三亚':'sanya',
'上海':'shanghai',
'沈阳':'shenyang',
'深圳':'shenzhen',
'石家庄':'shijiazhuang',
'太原':'taiyuan',
'天津':'tianjin',
'温州':'wenzhou',
'乌鲁木齐':'wlmq',
'武汉':'wuhan',
'无锡':'wuxi',
'厦门':'xiamen',
'西安':'xian',
'西宁':'xining',
'西双版纳':'xishuangbanna',
'烟台':'yantai',
'银川':'yinchuan',
'张家界':'zhangjiajie',
'郑州':'zhengzhou',
'珠海':'zhuhai',
'默认':'default'
}

s = requests.Session()


def get_url(url, refer, proxy=None):
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
        HOST = "zampdsp.com"
        header = {"HOST":HOST, "METHOD":"GET", "User-Agent":UA_LST[random.randrange(0, len(UA_LST))], 'Cache-Control':'no-cache', 'Referer':refer, "Accept":ACCEPT, "Accept-Encoding":ACCEPT_ENCODING, "Accept-Language":ACCEPT_LANGUAGE, "Connection":CONNECTION}
        r = s.get(url, headers=header)
        sc = r.status_code
        if sc == 200:
            r.encoding = 'utf-8'
            
            key = 'Content-Encoding'
            # print(response.headers[key])
            if(key in r.headers and r.headers['Content-Encoding'] == 'br'):
                data = brotli.decompress(r.content)
                data1 = data.decode('utf-8')
                return data1
            return r.text
        else:
            return None
    except Exception as e:
        logger.error(e)
        return None


def post_img_url(refer_url, url):
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
        
        HEADER_REFER = refer_url
        header = {"User-Agent":UA_LST[random.randrange(0, len(UA_LST))], "Referer":HEADER_REFER}
        r = s.get(url, headers=header)
        return r
    except Exception as e:
        return ""


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
    
    console = logging.StreamHandler()
    console.setLevel(level=logging.DEBUG)  # 设置为INFO级别
    console.setFormatter(fmter)
    logger.addHandler(console)


def gen_conf():
    json_f = open(JSON_CONF_FILE, 'a')
    json_f.writelines('['+'\n')
    log_content = {}
    for (k, v) in CITY_DICT.items():
        img_arr = []
        city_name = k
        city_short = v
        log_content['city'] = city_name
        dir_name = PY_IMG_PATH + "\\" + city_short
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, 777)
        for i in range(1, 4):
            img_url = IMG_PREFIX.format(str(city_short), str(i))
            img_arr.append(img_url)
            
            img_cont = post_img_url(img_url, img_url)
            img_name = img_url.split('/')[-1]
            img_path = dir_name + "\\" + img_name
            img_f = open(img_path, 'wb')
            img_f.write(img_cont.content)
            img_f.flush()
            img_f.close()
            
        log_content['img'] = img_arr
        cont = json.dumps(log_content, indent=2,ensure_ascii=False)
        cont1 = cont + ',' + '\n'
        json_f.writelines(cont1)
    json_f.writelines(']'+'\n')


if __name__ == '__main__':
    config_logger()
    gen_conf()
