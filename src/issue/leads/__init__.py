#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 'scott@zamplus.com'
__version__ = '1.0'

import sys
import os
import time
import datetime
import urllib
import urllib2
import re  # 正则表达式


def handle_post_request(url, req_params, req_header):
    data = urllib.urlencode(req_params)
    req = urllib2.Request(url, data, req_header)
    res = urllib2.urlopen(req)
    res_content = res.read()
    return res_content


def handle_get_request(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    content = response.read()
    return content


def handle_get_request_pc(url):
    header_ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4620.400 QQBrowser/9.7.13014.400'
    header_refer = 'http://dealer.bitauto.com/zuidijia/nb2593/?T=1&leads_source=p002001'
    headers = { 'User-Agent' : header_ua, 'Referer':header_refer }
    request = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(request)
    content = response.read()
    return content


def handle_get_request_h5(url):
    header_ua = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36' 
    header_refer = 'http://dealer.h5.yiche.com/MultiOrder/2593/126282/?leads_source=H001005'
    headers = { 'User-Agent' : header_ua, 'Referer':header_refer }
    request = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(request)
    content = response.read()
    return content


def parse_json_to_dict(content):
    json_str = content.replace('true', '"true"')
    json_str = json_str.replace('false', '"false"')
    json_str = eval(json_str)
    return json_str


def leads():
    # leads_url = 'http://dealer.h5.yiche.com/MultiOrder/3600/127132/?leads_source=H001005&WT.mc_id=mjinzanh5'
    leads_url = 'http://dealer.h5.yiche.com/MultiOrder/3600/127132/?leads_source=H001005'
    t = int(round(time.time() * 1000))
    smt_url_h5 = 'https://sec.bitauto.com/ordermobile/ashx/submitOrders.ashx?callback=aa&c=201&car=126282&ds=50000004%2C100058871&t=13625440067&n=%E6%9E%97%E7%90%B3&u=5ed327efa8614d1bbdca62b68e1b4761&ikey=&icode=&iid=43&_=' + str(t)
    smt_url_pc = 'https://sec.bitauto.com/multiplepc/ashx/submitOrders.ashx?leads_source=p002001&callback=orderCallback&n=%25u6797&s=1&t=15000767608&c=201&car=126283&ds=100059801&ot=1&tid=5ed327efa8614d1bbdca62b68e1b4761&sid=&code=0&icode=&ikey=&iid=40&iscall=0&ct=2018-02-27+11%3A01%3A05&isczk=0&_=' + str(t)
    # get_car_json = 'http://api.car.bitauto.com/CarInfo/GetCarDataJson.ashx?action=car&pid=3600&datatype=0&callback=a'
    
    # get_dealer = 'http://price.m.yiche.com/Ajax/getDealers.ashx?type=json&callback=aa&car=127133&city=201'
    # get_content = handle_get_request(smt_url_h5)
    # print 'response:\n%s' % get_content
    get_content = handle_get_request_h5(smt_url_h5)
    print 'response:\n%s' % get_content 


if __name__ == '__main__':
    leads()
