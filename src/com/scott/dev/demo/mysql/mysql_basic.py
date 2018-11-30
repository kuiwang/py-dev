# -*- coding:utf-8 -*-
# 使用配置文件来连接mysql
'''
Created on 2018年11月30日

@author: user
'''
import pymysql
import os, sys, datetime, time
import json

SRC_NAME = "src"
CONF_DIR = os.path.join(os.getcwd().split(SRC_NAME)[0], SRC_NAME, 'conf')
MYSQL_JSON_CFG = "mysql_json.cfg"


def json_conf_test():
    json_path = os.path.join(CONF_DIR, MYSQL_JSON_CFG)
    with open(json_path, 'r') as cfgFile:
        confStr = cfgFile.read()
    conf = json.loads(confStr)


if __name__ == '__main__':
    json_conf_test()
