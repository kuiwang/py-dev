# -*- coding:utf-8 -*-
'''
Created on 2018年11月27日

@author: user

'''
import urllib2
import json

REQ_HEADER_UA = "user-agent"
DEFAULT_UA = "user-agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
DEFAULT_HEADERS = {
    REQ_HEADER_UA:DEFAULT_UA
}
SAMPLE_URL = "http://partner.bitauto.com/api/jingzan/FileMap.xml"


def get_req(url):
    req = urllib2.Request(url, headers=DEFAULT_HEADERS)
    #print type(req)
    # resp = urllib2.urlopen(url, data, timeout, cafile, capath, cadefault, context)
    resp = urllib2.urlopen(req)
    #print type(resp)
    cont = resp.read()
    return cont


if __name__ == '__main__':
    get_req(SAMPLE_URL)
