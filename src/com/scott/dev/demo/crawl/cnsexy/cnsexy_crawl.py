# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日

@author: user
'''
import os, sys
from bs4 import BeautifulSoup
import logging
import requests
import mysqlutils
import pymysql
import traceback
import brotli

reload(sys)  
sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/".replace('/', os.sep)
logger = logging.getLogger('cnsxy')
LOG_FILE = 'cnsxy.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

s = requests.Session()
CNSXY_AUTHORITY = "cnsexy.net"
CNSXY_HOMEPAGE = "https://cnsexy.net/"
CNSXY_DOWNLOAD_PATH = PY_GEN_PATH + "/cnsxy/"
SOCKS5_PROXY_CONFIG = {"http":"http://127.0.0.1:58506", "https":"https://127.0.0.1:58506"}


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


def get_url(url, refer=None):
    try:
        HEADER_UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        HEADER_METHOD = "GET"
        HEADER_ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        HEADER_ACCEPT_ENCODING = "gzip, deflate, br"
        HEADER_ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9"
        HEADER_AUTHORITY = CNSXY_AUTHORITY
        header = {"User-Agent":HEADER_UA, "authority":HEADER_AUTHORITY,
                  "upgrade-insecure-requests":"1", "method":HEADER_METHOD,
                  "Accept":HEADER_ACCEPT, "Accept-Encoding":HEADER_ACCEPT_ENCODING,
                  "accept-language":HEADER_ACCEPT_LANGUAGE
        }
        if not refer:
            header['referer'] = 'https://cnsexy.net/'
        else:
            header['referer'] = refer
        # r = s.get(url, headers=header,verify=False)
        header['scheme']='https'
        header['cookie']='__cfduid=df1919a684c0ef2fe5908c392a9c1dca61547900851'
        r = s.get(url, headers=header, proxies={"socks5":"127.0.0.1:58506"})
        content = r.content
        data = brotli.decompress(content)
        data1 = data.decode('utf-8')
        # logger.info("response:\n" + data1)
        return data1
    except Exception, e:
        logger.error(e)


def post_img_url(model_url, url, refer=None):
    try:
        HEADER_UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        HEADER_REFER = model_url
        header = {"User-Agent":HEADER_UA, "Referer":HEADER_REFER}
        r = s.get(url, headers=header)
        # logger.info("response:" + txt)
        
        HEADER_UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        HEADER_METHOD = "GET"
        HEADER_ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        HEADER_ACCEPT_ENCODING = "gzip, deflate, br"
        HEADER_ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9"
        HEADER_AUTHORITY = CNSXY_AUTHORITY
        header = {"User-Agent":HEADER_UA, "authority":HEADER_AUTHORITY,
                  "upgrade-insecure-requests":"1", "method":HEADER_METHOD,
                  "Accept":HEADER_ACCEPT, "Accept-Encoding":HEADER_ACCEPT_ENCODING,
                  "accept-language":HEADER_ACCEPT_LANGUAGE
        }
        if not refer:
            header['referer'] = 'https://cnsexy.net/'
        else:
            header['referer'] = refer
        # r = s.get(url, headers=header,verify=False)
        r = s.get(url, headers=header, proxies={"socks5":"127.0.0.1:58506"})
        return r
    except Exception, e:
        return ""
        logger.error(e)


def getTotalAlbumPageNum(url):
    html = get_url(url)
    soup = BeautifulSoup(html, "lxml")
    main_div = soup.find('body').find('div', attrs={"id":"page"}).find(name='div', attrs={"id":"content"}).find(name="div", attrs={"id":"main"})
    post_masonry = main_div.find("section", attrs={"id":"post_masonry"})
    last_a = main_div.find("div", attrs={"class":"container"}).find("div", attrs={"class", "wp-pagenavi"}).find("a", attrs={"class":"last"})
    last_href = last_a.get("href")
    logger.info("last href:" + last_href)
    biggest_page = last_href.split("/")[-2]
    logger.info("biggest page:" + str(biggest_page))
    return biggest_page


def parseAlbumPageAndSave(url):
    html = get_url(url)
    param = []
    cur = conn.cursor()
    if html == "":
        pass
    soup = BeautifulSoup(html, "lxml")
    main_div = soup.find('body').find('div', attrs={"id":"page"}).find(name='div', attrs={"id":"content"}).find(name="div", attrs={"id":"main"})
    post_masonry = main_div.find("section", attrs={"id":"post_masonry"})
    # 获得所有的article列表
    article_list = post_masonry.findAll("article")
    for article in article_list:
        album_a = article.find(name="div").find(name="figure").find("a")
        id = article.get("id").split('-')[-1]
        name = album_a.get("title")
        href = album_a.get('href')
        print name + ' | ' + href
        param.append([id, name, href])
        logger.info("page_url:" + url + " | " + id + " | " + name + " | " + href)
    sql = "insert into album_info(id,name,url) values(%s,%s,%s)"
    insert_count = cur.executemany(sql, param)
    conn.commit()
    logger.info("save insert_count:" + str(insert_count))
    cur.close()


def saveAlbumInfo():
    total_page = getTotalAlbumPageNum(CNSXY_HOMEPAGE)
    logger.info("homepage:" + CNSXY_HOMEPAGE)
    parseAlbumPageAndSave(CNSXY_HOMEPAGE)
    for i in range(2, int(total_page) + 1):
        url = CNSXY_HOMEPAGE + "/page/" + str(i)
        logger.info("page url:" + url)
        parseAlbumPageAndSave(url)


def getModelUrl():
    cur = conn.cursor()
    # sql = "select id,name,model_url from album_info t "
    sql = "select id,name,url from album_info t "
    cur.execute(sql)
    rs = cur.fetchall()
    for r in rs:
        id = r[0]
        name = r[1]
        model_url = r[2]
        cur1 = conn.cursor()
        sql = "select model_id from model_photo t where model_id =  " + str(id)
        cur1.execute(sql)
        row = cur1.fetchone()
        if row:
            logger.info(str(id) + " 已经存在于数据库中，忽略")
            continue
        # saveModelPhoto(id, name, 1, model_url, model_url)
        logger.info("id:" + str(id) + " | name:" + name + " | " + model_url)
        saveModelPhoto(id, name, model_url)


def saveModelPhoto(id, name , model_url):
    param = []
    html = get_url(model_url, CNSXY_HOMEPAGE)
    logger.info("resp:\n" + html)
    soup = BeautifulSoup(html, "lxml")
    try:
        cur = conn.cursor()
        main_element = soup.find('body').find(name='div', attrs={"id":"page"}).find(name='div', attrs={"class":"content"}).find(name='div', attrs={"class":"container clearfix"}).find(name="div" , attrs={"id":"primary"}).find(name="main", attrs={"id":"main"})
        entry_content = main_element.find("article").find(name="div", attrs={"class":"entry-content clearfix"}).find(name="div").find(name="div", attrs={"class":"grid-gallery-photos"})
        a_list = entry_content.findAll("a", attrs={"class":"gg-link"})
        i = 0
        for a in a_list:
            i = i + 1
            img_id = i
            img_url = a.get("href")
            img_name = a.get("alt")
            logger.info("img url:" + img_url)
        
        img_cont = post_img_url(model_url, img_url, model_url)
        img_name = img_url.split('/')[-1]
        dir_name = CNSXY_DOWNLOAD_PATH + "\\" + name
        if not os.path.exists(dir_name):
            logger.info('文件夹:' + dir_name + '不存在')
            os.makedirs(dir_name, 777)
            logger.info('创建文件夹 ' + dir_name + '成功')
        img_path = dir_name + "\\" + img_name
        logger.info("image real path:" + img_path)
        img_f = open(img_path, 'wb')
        img_f.write(img_cont.content)
        img_f.flush()
        fin = open(img_path, 'rb')
        img_b = fin.read()
        param.append([id, img_id, img_url, img_path])
        logger.info(str(id) + " | " + str(img_no) + " | " + photo_url)
        sql = "insert into model_photo(model_id,img_id,img_url,img_path) values(%s,%s,%s,%s)"
        insert_count = cur.executemany(sql, param)
        # logger.info("save photo count:" + str(insert_count))
        conn.commit()
    except Exception as e:
        logger.error(traceback.format_exc())
        pass
    finally:
        img_f.close()
        fin.close()
        cur.close()


def test():
    url = "https://cnsexy.net/luoli181127/"
    html = get_url(url)
    logger.info("resp:\n" + html)


if __name__ == '__main__':
    config_logger()
    conn = mysqlutils.connect_mysql()
    # saveAlbumInfo()  # save personal photo url
    getModelUrl()
    # test()
    conn.close()

