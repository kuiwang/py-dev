# -*- coding:utf-8 -*-
'''
Created on 2018年10月14日

@author: root
'''
import os,sys
import pymysql
def operateMysql():
    try:
        conn = pymysql.Connect(host='localhost',user='root',passwd='admin',db='test')
        print 'connect successful!'
    except Exception ,e:
        print "exception in below:\n",e
        sys.exit()
    stmt = conn.cursor()
    sql = "select * from student t "
    stmt.execute(sql)
    rs = stmt.fetchall()
    if rs:
        for x in rs:
            print "id:%s,name:%s,age:%s" %(x[0],x[1],x[2])
    stmt.close()
    conn.close()

if __name__ == '__main__':
    operateMysql()

