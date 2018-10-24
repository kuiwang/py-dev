# -*- coding:utf-8 -*-
'''
Created on 2018年10月15日

@author: user
'''
import os, sys
import pymysql


def operate_mysql():
    try:
        conn = pymysql.connect(host='localhost', user='root', password='admin', db='test')
        print 'connect successful!'
    except Exception, e:
        print 'exception in below:\n', e
        sys.exit()
    statement = conn.cursor()
    sql = "select pid,name,loc,brand from czzj_info t "
    statement.execute(sql)
    rs = statement.fetchall()
    if rs:
        for x in rs:
            print 'pid:%s , name:%s , loc:%s , brand:%s' % (x[0], x[1], x[2], x[3])
    statement.close()
    conn.close()


if __name__ == '__main__':
    operate_mysql()
