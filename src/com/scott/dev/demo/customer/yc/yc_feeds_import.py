# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日

@author: user
'''
import os, sys, json
import logging
import requests
import mysqlutils
import argparse
from bs4 import BeautifulSoup 

reload(sys)  
sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/bitauto".replace('/', os.sep)
YC_INDEX_FILE = "bitauto_index.xml"
YC_FEED_LOC = "bitauto_loc.xml"
logger = logging.getLogger('bitauto_feed')
LOG_FILE = 'bitauto_feed_import.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

s = requests.Session()


def get_url(url):
    try:
        UA = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
        ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        ACCEPT_ENCODING = "gzip, deflate"
        ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9"
        CONNECTION = "keep-alive"
        header = {"User-Agent":UA, "Accept":ACCEPT, "Accept-Encoding":ACCEPT_ENCODING, "Accept-Language":ACCEPT_LANGUAGE, "Connection":CONNECTION}
        r = s.get(url, headers=header)
        r.encoding = "utf-8"
        # logger.info("response:\n" + r.text)
    except Exception, e:
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


def saveFeed(account_id, feed_url):
    # 读取feed url生成索引文件地址
    parseAndSaveIndex(feed_url)
    parseLocFile(os.path.join(PY_GEN_PATH, YC_FEED_LOC))


def parseLocFile(loc_file):
    with open(loc_file, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line:
                saveLoc(line)


def saveLoc(loc_url):
    logger.info("save file:" + loc_url)
    idx_txt = get_url(loc_url)
    param = []
    file_name = loc_url.split("/")[-1]
    cur = conn.cursor()
    file_abs_path = os.path.join(PY_GEN_PATH + os.path.sep, file_name)
    soup = BeautifulSoup(idx_txt, "lxml-xml")
    insert_sql = "insert into yc_info(pid,name,image,url,murl,img_width,img_height,brand,category,sub_cat,third_cat,related_ids,cut_price,model_url,m_model_url,quote_price,leads_url,status,emission,origin,country,price_lowest,price_highest,runk_num)"
    insert_sql = insert_sql + " values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    with open(file_abs_path, 'w') as f:
        f.write(idx_txt)
        products = soup.find("products")
        prds = products.findAll("product")
        for prd in prds:
            pid = prd.find("id").text
            name = prd.find("name").text
            image = prd.find("image").text
            landingPage = prd.find("landingPage").text
            m_landingPage = prd.find("m_landingPage").text
            imageWidth = prd.find("imageWidth").text
            imageHeight = prd.find("imageHeight").text
            brand = prd.find("brand").text
            c1 = prd.find("category").text
            c2 = prd.find("subCategory").text
            c3 = prd.find("thirdCategory").text
            competingModelsId = prd.find("competingModelsId").text
            cutPrice = prd.find("cutPrice").text if(prd.find("cutPrice").text != '') else 'No-cutPrice'
            cutPriceUrl = prd.find("cutPriceUrl").text
            m_cutPriceUrl = prd.find("m_cutPriceUrl").text
            quotedPrice = prd.find("quotedPrice").text
            tijiaodealerUrl = prd.find("tijiaodealerUrl").text
            saleStatus = prd.find("saleStatus").text
            emission = prd.find("emission").text
            origin = prd.find("origin").text
            country = prd.find("country").text
            priceLowest = prd.find("priceLowest").text
            priceHighest = prd.find("priceHighest").text
            runkNum = prd.find("runkNum").text
            param.append([str(pid), str(name), str(image), str(landingPage) ,
                          str(m_landingPage), str(imageWidth), str(imageHeight), str(brand),
                          str(c1), str(c2), str(c3), str(competingModelsId),
                          str(cutPrice), str(cutPriceUrl), str(m_cutPriceUrl), str(quotedPrice),
                          str(tijiaodealerUrl), str(saleStatus), str(emission), str(origin),
                          str(country), str(priceLowest), str(priceHighest), str(runkNum)]
            )
    insert_count = cur.executemany(insert_sql, param)
    conn.commit()
    logger.info("save insert_count:" + str(insert_count))
    cur.close()


def parseAndSaveIndex(feed_url):
    idx_txt = get_url(feed_url)
    idx_file_path = os.path.join(PY_GEN_PATH, YC_INDEX_FILE)
    with open(idx_file_path, 'w') as f:
        f.write(idx_txt)
        f.flush()
        f.close()
    soup = BeautifulSoup(idx_txt, "lxml")
    root = soup.find("root")
    dir = root.find("dir")
    feed_prefix = dir.text
    outer_id_lst = root.find("item_ids").findAll("outer_id")
    
    loc_file_path = os.path.join(PY_GEN_PATH, YC_FEED_LOC)
    loc_file = open(loc_file_path, 'w')
    
    for outer_id in outer_id_lst:
        outer_id_txt = outer_id.text
        if outer_id_txt.find(".xml") <= 0:
            outer_id_txt = outer_id_txt + ".xml"
            feed_url = feed_prefix + outer_id_txt
        loc_file.write(feed_url + "\n")
    loc_file.flush()
    loc_file.close()


def init_parser():
    logger.info('start parse arguments')
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url",
                        type=str,
                        dest='url',
                        required=True,
                        help="客户feeds url"
                        )
    parser.add_argument("-a", "--account",
                        type=int,
                        dest='account',
                        required=True,
                        help="客户账户ID"
                        )
    return parser


if __name__ == '__main__':
    conn = mysqlutils.connect_mysql()
    config_logger()
    
    parser = init_parser()
    args = parser.parse_args()
    account_id = args.account
    feed_url = args.url
    
    saveFeed(account_id, feed_url)
    
    conn.close()
