# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日

@author: user
'''
import os, sys
from bs4 import BeautifulSoup
import logging
import requests
import pymysql
import traceback
from com.scott.dev.util.mysqlpool import MySQLConnPool
from importlib import reload

reload(sys)  
#sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/".replace('/', os.sep)
logger = logging.getLogger('mztcraw')
LOG_FILE = 'mzt_crawl.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

s = requests.Session()
MZT_AUTHORITY = "www.mzitu.com"
MZT_HOMEPAGE = "https://www.mzitu.com"
MZT_DOWNLOAD_PATH = PY_GEN_PATH + "/mzt/"


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


def post_url(url):
    try:
        HEADER_UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        HEADER_METHOD = "GET"
        HEADER_ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        HEADER_ACCEPT_ENCODING = "gzip, deflate, br"
        HEADER_AUTHORITY = MZT_AUTHORITY
        header = {"User-Agent":HEADER_UA, "authority":HEADER_AUTHORITY, "method":HEADER_METHOD, "Accept":HEADER_ACCEPT, "Accept-Encoding":HEADER_ACCEPT_ENCODING}
        r = s.post(url, headers=header)
        txt = r.text
        # logger.info("response:" + txt)
        return txt
    except Exception, e:
        return ""
        logger.error(e)


def post_img_url(model_url, url):
    try:
        HEADER_UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        HEADER_REFER = model_url
        header = {"User-Agent":HEADER_UA, "Referer":HEADER_REFER}
        r = s.get(url, headers=header)
        # logger.info("response:" + txt)
        return r
    except Exception, e:
        return ""
        logger.error(e)


def getTotalAlbumPageNum(url):
    html = post_url(url)
    soup = BeautifulSoup(html, "lxml")
    post_list = soup.find('body').find('div', attrs={"class":"main"}).find(name='div', attrs={"class":"main-content"}).find(name="div", attrs={"class":"postlist"})
    nav_links = post_list.find("nav", attrs={"class":"navigation pagination"}).find("div", attrs={"class":"nav-links"})
    biggest_page = nav_links.find("span", attrs={"class":"page-numbers dots"}).next_sibling.next_sibling
    return biggest_page.text


# 解析页面: url= https://www.mzitu.com/page/2/ 
def parseAlbumPageAndSave(url):
    param = []
    cur = conn.cursor()
    html = post_url(url)
    if html == "":
        pass
    soup = BeautifulSoup(html, "lxml")
    li = soup.find('body').find('div', attrs={"class":"main"}).find(name='div', attrs={"class":"main-content"}).find(name="div", attrs={"class":"postlist"}).find(name="ul", attrs={"id":"pins"}).findAll(name="li")
    for item in li:
        a = item.find("a")
        href = a.get('href')
        name = a.find("img").get("alt")
        id = href.split("/")[-1]
        param.append([id, name, href])
        logger.info("page_url:" + url + " | " + id + " | " + name + " | " + href)
    sql = "insert into album_info(id,name,url) values(%s,%s,%s)"
    insert_count = cur.executemany(sql, param)
    conn.commit()
    logger.info("save insert_count:" + str(insert_count))
    cur.close()


def saveAlbumInfo():
    total_page = getTotalAlbumPageNum(MZT_HOMEPAGE)
    logger.info("homepage:" + MZT_HOMEPAGE)
    parseAlbumPageAndSave(MZT_HOMEPAGE)
    for i in range(2, int(total_page) + 1):
        url = MZT_HOMEPAGE + "/page/" + str(i)
        logger.info("page url:" + url)
        parseAlbumPageAndSave(url)


def getTotalModelPhotoNum(url):
    html = post_url(url)
    # logger.info("resp:\n" + html)
    soup = BeautifulSoup(html, "lxml")
    div_cont = soup.find('body').find(name='div', attrs={"class":"main"}).find(name='div', attrs={"class":"content"})
    img_url = div_cont.find(name="div", attrs={"class":"main-image"}).find("p").find("a").find("img").get("src")
    dots = div_cont.find("div", attrs={"class":"pagenavi"}).find("span", attrs={"class":"dots"}).next_sibling
    logger.info("Url:" + url + " | img_Url:" + img_url + " | totalPage:" + dots.text)
    return dots.text


def getModelUrl():
    sql = "select id,name,url from album_info t "
    rs = conn.queryall(sql)
    for r in rs:
        id = r[0]
        name = r[1]
        url = r[2]
        sql = "select model_id from model_photo t where model_id =  " + str(id)
        row = conn.queryone(sql)
        if row:
            logger.info(str(id) + " 已经存在于数据库中，忽略")
            continue
        model_total_photo = int(getTotalModelPhotoNum(url))
        saveModelPhoto(id, name, 1, url, url)
        logger.info("id:" + str(id) + " | name:" + name + " | " + url + " | total:" + str(model_total_photo))
        for x in range(2, model_total_photo + 1):
            # logger.info("index:" + str(x))
            model_photo_url = url + "/" + str(x)
            saveModelPhoto(id, name, x, url, model_photo_url)


def saveModelPhoto(id, name, img_no , model_url, photo_url):
    param = []
    logger.info("photo url:" + photo_url)
    html = post_url(photo_url)
    # logger.info("resp:\n" + html)
    soup = BeautifulSoup(html, "lxml")
    try:
        cur = conn.cursor()
        div_cont = soup.find('body').find(name='div', attrs={"class":"main"}).find(name='div', attrs={"class":"content"})
        img_url = div_cont.find(name="div", attrs={"class":"main-image"}).find("p").find("a").find("img").get("src")
        logger.info("image url:" + img_url)
        img_cont = post_img_url(model_url, img_url)
        img_name = img_url.split('/')[-1]
        if (name.find(":") > -1 or name.find("?") > -1):
            name = name.replace(":", "-")
            name = name.replace("?", "-")
        dir_name = MZT_DOWNLOAD_PATH + "\\" + name
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
        img_str = pymysql.escape_string(img_b)
        param.append([id, img_no, img_url, img_path])
        logger.info(str(id) + " | " + str(img_no) + " | " + photo_url)
        sql = "insert into model_photo(model_id,img_id,img_url,img_path) values(%s,%s,%s,%s)"
        insert_count = conn.insertmany(sql, param)
        # logger.info("save photo count:" + str(insert_count))
    except Exception as e:
        logger.error(traceback.format_exc())
        pass
    finally:
        img_f.close()
        fin.close()


if __name__ == '__main__':
    config_logger()
    conn = MySQLConnPool('mzt')
#     saveAlbumInfo() #save personal photo url
    getModelUrl()
    # test()
    conn.dispose(1)

