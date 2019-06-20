# -*- coding:utf-8 -*-
# mongo
'''
Created on 2018年11月30日

@author: user
'''
from pymongo import MongoClient as mc 
import os, sys, datetime, time

SRC_NAME = "src"
CONF_DIR = os.path.join(os.getcwd().split(SRC_NAME)[0], SRC_NAME, 'conf')
MONGO_CONN_URL = "mongodb://test:test@localhost:27017/local"


def mongo_test():
    conn = mc(MONGO_CONN_URL)
    dict = conn.__dict__
    for (k, v) in dict.items():
        print (('{}={}').format(str(k), str(v)))
#         print ("dict[%s]=%s" % (k, v))
    # 字典keys()方法
    # print (dict.keys())
    # 字典values()方法
    # print (dict.values())
    
    db = conn._MongoClient__default_database_name
    print ('dataname:{}'.format(db))
    conn.close()


if __name__ == '__main__':
    mongo_test()
