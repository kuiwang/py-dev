# -*- coding:utf-8 -*-
# redis
'''
Created on 2018年11月30日

@author: user
'''
import redis
import os, sys, datetime, time
import json

SRC_NAME = "src"
CONF_DIR = os.path.join(os.getcwd().split(SRC_NAME)[0], SRC_NAME, 'conf')
MYSQL_JSON_CFG = "mysql_json.cfg"


def redis_test():
    pool = redis.ConnectionPool(host='localhost', port=6379)
    r = redis.Redis(connection_pool=pool)
    r.set('name1', 'zhangsan')   #添加
    print (r.get('name1'))   #获取


if __name__ == '__main__':
    redis_test()
