# -*- coding:utf-8 -*-

'''
Rquests的基本用法
Created on 2018年11月5日

@author: user
'''
import requests

proxy_config = {
    "socks5":"https://127.0.0.1:58506"
}


def import_reqeusts():
    print ('requests的基础用法示例')
    import requests as req
    BD_HOME_PAGE = 'https://www.baidu.com'
    resp = req.get(BD_HOME_PAGE)
    txt = resp.text
    print ('response text:\n' + txt)
    print ('status_code: %s' % resp.status_code)
    print ('response txt type:' + type(txt))


def req_via_pro_global():
    import socks
    import socket
    
    socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 58506)
    socket.socket = socks.socksocket
    response = requests.get('http://httpbin.org/get')
    print(response.text)


def req_via_pro_local():
    proxy = '127.0.0.1:58506'
    proxies = {
        'http': 'socks5://' + proxy,
        'https': 'socks5://' + proxy
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36'
    }
    url = 'https://www.google.com/search?q=python'
    response = requests.get(url, headers=headers, proxies=proxies)
    print(response.text)


if __name__ == '__main__':
    # import_reqeusts()
    req_via_pro_local()
