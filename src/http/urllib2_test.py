#! /usr/bin/python
# -*- coding: UTF-8 -*-
# coding: utf-8
'''
urllib2测试
'''

import urllib2


def urllib2_main():
    py_url = 'http://python.org/'
    resp_content = urllib2.urlopen(py_url)
    html = resp_content.read()
    print (html)
    print ("\n============================\n")
    print("使用Request:\n")
    print ("\n============================\n")
    request = urllib2.Request(py_url)
    resp = urllib2.urlopen(request)
    print(resp.read())

if __name__ == '__main__':
    urllib2_main()
