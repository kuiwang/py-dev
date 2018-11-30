# -*- coding:utf-8 -*-

'''
Rquests的基本用法
Created on 2018年11月5日

@author: user
'''


def import_reqeusts():
    print 'requests的基础用法示例'
    import requests as req
    BD_HOME_PAGE = 'https://www.baidu.com'
    resp = req.get(BD_HOME_PAGE)
    txt = resp.text
    print 'response text:\n', txt
    print 'status_code: %s' % resp.status_code
    print 'response txt type:', type(txt)
    print 'cookies:', resp.cookies


if __name__ == '__main__':
    import_reqeusts()
