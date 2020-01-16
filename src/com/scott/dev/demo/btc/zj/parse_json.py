# -*- coding:utf-8 -*-

'''
Created on 2019年8月26日

@author: user
'''
import os, sys, logging
from importlib import reload
import json

reload(sys)
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "E:/data/priv".replace('/', os.sep)
logger = logging.getLogger('parse_json')
LOG_FILE = 'parse_json.csv'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(message)s'
JSON_NAME = 'raw_json.json'


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


def parseJson(file_path):
    with open(file_path, 'r', encoding='UTF-8') as f:
        content1 = f.readline().strip()
        i = 0
        logger.info("index,data_size,date,hour,adv_id,adv_name,camp_id,camp_name,adgrp_id,adgrp_name,ad_id,ad_name,allianceid,sid,ouid,imp,click,ctr,cpc,cpm,cost")
        while content1:
            i = i + 1
            content = json.loads(content1)
            data = content['response']['data']
            data_size = len(data)
            for d in data:
                date = d['report_date']
                hour = d['report_hour']
                adv_id = d['advertiser_id']
                adv_name = d['advertiser_name']
                camp_id = d['campaign_id']
                camp_name = d['campaign_name']
                adgrp_id = d['adgroup_id']
                adgrp_name = d['adgroup_name']
                ad_id = d['ad_id']
                ad_name = d['ad_name']
                allianceid = d['allianceid']
                sid = d['sid']
                ouid = d['ouid']
                imp = d['imp']
                click = d['click']
                ctr = d['ctr']
                cpc = d['cpc']
                cpm = d['cpm']
                cost = d['cost']
                # format: 
                # 第几个response,data个数,date,hour,adv_id,adv_name,camp_id,camp_name,
                # adgrp,adgrp_name,ad_id,ad_name,allianceid,sid,ouid,imp,clk,ctr,cpc,cpm,cost
                logger.info('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(
                    str(i), str(data_size), str(date), str(hour), str(adv_id), str(adv_name), str(camp_id), str(camp_name),
                    str(adgrp_id), str(adgrp_name), str(ad_id), str(ad_name), str(allianceid), str(sid), str(ouid), str(imp),
                    str(click), str(ctr), str(cpc), str(cpm), str(cost)
                    ))
            content1 = f.readline().strip()

    
if __name__ == '__main__':
    config_logger()
    cwd = os.getcwd().replace('\\', '/')
    file_path = os.path.join(cwd, JSON_NAME)
    parseJson(file_path)
