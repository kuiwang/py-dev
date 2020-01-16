# -*- coding:utf-8 -*-
'''
Created on 2018年12月14日
get wifi
@author: user
'''
import os, sys
import logging
import itertools
import requests, json
from bs4 import BeautifulSoup 
from importlib import reload
import random, time
import brotli
import pywifi
from pywifi.wifi import PyWiFi
reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "E:/data/priv".replace('/', os.sep)
logger = logging.getLogger('wifi_check')
LOG_FILE = 'wifi_pwd.log'
LOG_FORMATTER = '%(message)s'
AKMS = {
0:'AKM_TYPE_NONE',
1:'AKM_TYPE_WPA',
2:'AKM_TYPE_WPAPSK',
3:'AKM_TYPE_WPA2',
4:'AKM_TYPE_WPA2PSK',
5:'AKM_TYPE_UNKNOWN'
}


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
    '''
    console = logging.StreamHandler()
    console.setLevel(level=logging.DEBUG)  # 设置为INFO级别
    console.setFormatter(fmter)
    logger.addHandler(console)
    '''

# 获取是否连接网络
def check_state():
    # 创建一个无线对象wifi
    wifi = PyWiFi()
    # 取第一个无线网卡
    ifaces = wifi.interfaces()[0]
    stat = ifaces.status()
    logger.info('ifaces status:{}'.format(str(stat)))
    if stat == 4:
        logger.info('already connected to wifi')
    else:
        logger.info('not connected yet!')


def get_wireless_info():
    # 创建一个无线对象wifi
    wifi = PyWiFi()
    # 取第一个无线网卡
    ifaces = wifi.interfaces()[0]
    # 扫描附近的无线信号
    # ifaces.scan()
    wireless_lst = ifaces.scan_results()
    for d in wireless_lst:
        ssid = d.ssid
        encry_method = AKMS[d.akm[0]]
        logger.info('ssid:{}|method:{}'.format(str(ssid), str(encry_method)))

# 测试链接
# def test_connected(self,):


def gen_pwd_lst():
    a = []
    #digits58 = '1234567890qQwWeErRtTyYuUiIoOpPaAsSdDfFgGhHjJkKlLzZxXcCvVbBnNmM!@#$%^&*()_+-='
    digits58 = '1234567890abcefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*'
    for i in digits58:
        a.append(i)
    #file = PY_GEN_PATH + '/wifi_pwd.txt'
    #with open(file, 'a', encoding='utf-8') as f:
    for b in range(8, 11):
        for x in itertools.product(*[a] * b):
            p = str(''.join(x)).strip()
            logger.info(p)
            #f.writelines(''.join(x))
        

if __name__ == '__main__':
    config_logger()
    gen_pwd_lst()
