# -*- coding: utf-8 -*-

# from download_info import download_info
# from download_pictures import get_info, get_info_imgs, download
from importlib import reload
import os, sys
import logging, json, demjson, time
import requests, random

from multiprocessing import Process, Queue, Pool

reload(sys)

PY_GEN_PATH = "D:/download/pygen/as".replace('/', os.sep)
logger = logging.getLogger('as')
LOG_FILE = 'as.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

s = requests.Session()


def get_url(url, data):
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
        ACCEPT = "text/html,text/json,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        ACCEPT_ENCODING = "gzip, deflate, br"
        ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9"
        CONNECTION = "keep-alive"
        header = {"User-Agent":UA_LST[random.randrange(0, len(UA_LST))], "method":'POST', 'Cache-Control':'no-cache', "Accept":ACCEPT, "Accept-Encoding":ACCEPT_ENCODING, "Accept-Language":ACCEPT_LANGUAGE, "Connection":CONNECTION}
        r = s.post(url, headers=header, data=data)
        r.encoding = "utf-8"
        # logger.info("response:\n" + r.text)
    except Exception as e:
        logger.error(e)
    return r.text


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

# ##download_info


def download_page(page):
    """ 下载某页面的信息 """
    url = 'http://api.pmkoo.cn/aiss/suite/suiteList.do'
    usrId = 153044
    params = {
        'page': page,
        'userId': usrId
    }
    logger.info("url:{},page:{},userId:{}".format(url, str(page), str(usrId)))
    # rsp = requests.post(url, data=params)
    rsp = get_url(url, params)
    # return rsp.json()
    return rsp


def download_info():
    """ 下载列表页（包含所有对图片的描述信息），并存储到data/info.txt文件中 """
    page = 1
    while True:
        page_json = demjson.decode(download_page(page), 'utf8')
        if not page_json['data']['list']:
            break
        save_page(page_json)
        page += 1


def save_page(page_json):
    """ 保存某页面的信息 """
    txt = json.dumps(page_json)
    with open(os.path.join(PY_GEN_PATH, 'data/info.txt'), 'a') as f:
        f.write(txt)
        f.write('\n')

# ##download_pictures


def get_info():
    """ 获取所有图片组的信息 """
    res = []
    with open(os.path.join(PY_GEN_PATH, 'data/info.txt'), 'r') as f:
        for line in f:
            data = json.loads(line)
            res.extend(data['data']['list'])
    return res


def get_info_imgs(info):
    """ 获取要下载的所有图片url、目录名、要存储的名字 """
    res = []
    for item in info:
        nickname = item["author"]["nickname"]
        catalog = item["source"]["catalog"]
        name = item["source"]["name"]
        issue = item["issue"]
        pictureCount = item["pictureCount"]
        for pic_idx in range(pictureCount):
            # url = "http://aiss-1254233499.costj.myqcloud.com/picture/%s/%s/%s.jpg" % (catalog, issue, pic_idx)
            url = "http://tuigirl-1254818389.cosbj.myqcloud.com/picture/%s/%s/%s.jpg" % (catalog, issue, pic_idx)
            directory = os.path.join(PY_GEN_PATH + "/data/", name, "%s-%s" % (issue, nickname))
            filepath = os.path.join(directory, "%s.jpg" % pic_idx)
            # 每张图片一组，包含 图片url，所在目录，存储路径
            logger.info("url:{} | dir:{} | filepath:{}".format(url, directory, filepath))
            res.append((
                url, directory, filepath
            ))
    return res


def setup_download_dir(directory):
    """ 设置文件夹，文件夹名为传入的 directory 参数，若不存在会自动创建 """
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            pass
    return True


def download_one(img):
    """ 下载一张图片 """
    url, directory, filepath = img
    logger.info("download_one | url:{},dir:{},filepath:{}".format(url, directory, filepath))
    # 如果文件已经存在，放弃下载
    if os.path.exists(filepath):
        logger.error("filepath:{} exists".format(filepath))
        # print('exists:', filepath)
        return

    setup_download_dir(directory)
    rsp = requests.get(url)
    # print('start download', url)
    logger.info("download_one | start download , url:{}".format(url))
    with open(filepath, 'wb') as f:
        f.write(rsp.content)
        logger.info('end download | url:' + url)


def download(imgs, processes=10):
    """ 并发下载所有图片 """
    logger.info("download start now")
    start_time = time.time()
    pool = Pool(processes)
    for img in imgs:
        pool.apply_async(download_one, (img,))

    pool.close()
    pool.join()
    end_time = time.time()
    logger.info("download | 下载完毕,用时:%s秒" % (end_time - start_time))
    # print('下载完毕,用时:%s秒' % (end_time - start_time))


if __name__ == '__main__':
    config_logger()
    
    # 下载图片描述信息
    #download_info()
    # 获取图片组信息
    info = get_info()
    # 获取每张图片的url，存储文件夹，本地文件名
    imgs = get_info_imgs(info)
    # 以10个进程并发下载图片
    download(imgs, processes=10)
