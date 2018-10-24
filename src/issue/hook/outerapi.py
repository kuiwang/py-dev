#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 'scott@zamplus.com'
__version__ = '1.0'

'''
Api:
    inner_url = 'http://mc.zampda.net/v1/api/merchants/2764703/?offline=t&advertiser_id=194'
    outer_url = 'http://mc.zampda.net/v1/api/merchants/?offline=f&advertiser_id=639&outerID=132126&feed_id=1242'

Why:
    批量读读取文件中的商品ID,根据商品ID和FeedId调取mc接口,从而得知未出钩子是何原因导致的

Input:
    zid文件名(将文件放在src目录下)
    Account ID
    FeedId

Output:


'''
import sys
import os
import time
import urllib
import urllib2
import re  # 正则表达式

mc_url_pre = 'http://mc.zampda.net/v1/api/merchants/'
get_pid_pre = 'http://soraka.zamplus.com:8888/uc/GetTraits?hc_server=TS+Traits+HC+172.22.57.81'
src_dir_name = 'src'
dest_dir_name = 'dest'


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


# 使用客户ID查询MC
def query_by_outerid(company_id, feed_id, outerId):
    mc_outer_api_url = mc_url_pre + "?offline=t&advertiser_id=" + company_id + "&feed_id=" + feed_id + "&outerID=" + outerId
    outer_api_response = handle_get_request(mc_outer_api_url)
    return outer_api_response


# 使用晶赞内部ID查询MC
def query_by_innerid(company_id, innerId):
    mc_inner_api_url = mc_url_pre + "/" + innerId + "/?offline=t&advertiser_id=" + company_id
    inner_api_response = handle_get_request(mc_inner_api_url)
    return inner_api_response


def parse_json_to_dict(content):
    json_str = content.replace('true', '"true"')
    json_str = json_str.replace('false', '"false"')
    json_str = eval(json_str)
    return json_str


# 根据zid去查询Traits接口,然后爬取固定标签的值(非空值)
def get_pid_by_zid(company_id , zid):
    get_pid_url = get_pid_pre + '&advertiser_id=' + company_id + '&zid=' + zid
    get_pid_response = handle_get_request(get_pid_url)
    return get_pid_response


# 根据Traits接口查询结果,获取要得到的pid
def get_pid_from_traits(traits_resp):
    pid_list = []
    re_table = r'<table class="table table-striped table-bordered">(.*?)</table>'
    cont_table = re.findall(re_table, traits_resp, re.S | re.M)
    
    re_tbody = r'<tbody>(.*?)</tbody>'
    cont_tbody = re.findall(re_tbody, cont_table[0], re.S | re.M)

    re_tr = r'<tr>(.*?)</tr>'
    cont_tr = re.findall(re_tr, cont_tbody[0], re.S | re.M)
    # print cont_tr[1:]
    for tr in cont_tr[1:]:
        # print tr
        re_td = r'<td>(.*?)</td>'
        cont_tr = re.findall(re_td, tr, re.S | re.M)
        pid = cont_tr[1].strip()  # 只取第二列pid
        if pid != '':
            pid_list.append(pid)
        # print pid
    return pid_list


def hook_issue():
    cur_time = time.strftime(r"%Y-%m-%d_%H-%M-%S", time.localtime())
    
    py_script_name = sys.argv[0]  # 脚本名称
    src_file_name = sys.argv[1]  # zid csv源文件
    company_id = sys.argv[2]  # 广告主ID
    feed_id = sys.argv[3]  # 广告主feedID

    py_script_dir = os.path.dirname(py_script_name)
    src_dir = os.path.join(py_script_dir, src_dir_name)
    if not os.path.exists(src_dir):
        os.makedirs(r'%s/%s', (os.getcwd, src_dir_name))

    dest_dir = os.path.join(py_script_dir, dest_dir_name)
    if not os.path.exists(dest_dir):
        os.makedirs(r'%s/%s', (os.getcwd, dest_dir_name))

    abs_src_file_path = os.path.join(src_dir, src_file_name)
    abs_dest_file_path = os.path.join(dest_dir, company_id + '-' + str(cur_time) + ".csv")
    
    # 将处理结果写入目标文件
    dest_file_writer = open(abs_dest_file_path, "w+")
    
    # 打开源文件
    src_file_reader = open(abs_src_file_path, "r+")
    zid_with_return = src_file_reader.readline()
    real_zid = zid_with_return.replace('\n', '')
    dest_file_writer.writelines('num,zid,pid,stock\n')
    n = 0
    while real_zid:
        n = n + 1
        soraka_traits_resonse = get_pid_by_zid(company_id, real_zid)
        if (soraka_traits_resonse == ''):
            print 'zid:%s is null' % real_zid
            return
        pid_list = get_pid_from_traits(soraka_traits_resonse)  ############未完成
        # print pid_list
        for pid in pid_list:
            outerid_response = query_by_outerid(company_id, feed_id, pid)
            json_resp = parse_json_to_dict(outerid_response)
            if str(json_resp['response'] == ''):
                dest_file_writer.writelines(str(n) + ',' + real_zid + ',' + pid + ',NotExists' + '\n')
            else:
                stock = json_resp['response'][0]['stock']
                dest_file_writer.writelines(str(n) + ',' + real_zid + ',' + pid + ',' + stock + '\n')
            # print ('pid:%s,\n json_resp:\n%s') % (pid, stock)
        # 进入下一个循环,继续读取下一个zid
        zid_with_return = src_file_reader.readline()  # 包含有回车的zid
        real_zid = zid_with_return.replace('\n', '')  # 将zid后面的回车去掉
    # 记得关闭文件
    src_file_reader.close()
    dest_file_writer.close()


def test():
    # os.makedirs(r'%s/%s'%(os.getcwd(),"src1"))
    str = '{"status": 0, "errors": [], "response": [{"prdStatus": "5", "shopType": "\u81ea\u8425", "image": "https://gfs17.gomein.net.cn/T1C7KvBbAT1RCvBVdK", "clickUrl": "https://item.gome.com.cn/A0006010854-pop8009072534.html?cmpid=dsp_jingzan_dqc", "sync": true, "feed_id": 1352, "64strid": "1303511450378152313", "prdSkuNo": "8009072534", "category": "\u7535\u8111 \u529e\u516c\u6253\u5370 \u6587\u4eea", "loc": "https://item.gome.com.cn/A0006010854-pop8009072534.html?cmpid=dsp_jingzan_dqc", "subCategory": "cat10000015", "isSensitive": false, "mloc": "https://item.m.gome.com.cn/product-A0006010854-pop8009072534.html?cmpid=dsp_jingzan_dqc", "version": 66341137, "customerType": 638, "stock": 0, "status": 0, "update_time": 1514755894, "hash": "654496298", "price": 76388.0, "prdId": "A0006010854", "mClickUrl": "https://item.m.gome.com.cn/product-A0006010854-pop8009072534.html?cmpid=dsp_jingzan_dqc", "thirdCategory": "cat10000092", "imageSize": "800x800", "name": "\u8054\u60f3Thinkpad P70 20ERA01KCD 17.3\u82f1\u5bf8\u56fe\u5f62\u5de5\u4f5c\u7ad9 \u81f3\u5f3aE3/32G/\u53cc512G\u56fa\u6001/8G\u72ec\u663e", "prdStockRegion2": "5399,5305,5307,5303,5310,5314,5312,5306,5301,5308,5309,5304,5302,5311,5313,4305,4318,4316,4307,4399,4308,4314,4303,4301,4310,4312,4317,4304,4309,4306,4315,4302,4313,4311,1507,1505,1599,1502,1509,1511,1501,1506,1508,1503,1504,1512,1510,2599,2502,2507,2501,2508,2506,2503,2504,2505,2509,3106,3101,3119,3120,3108,3109,3104,3117,3102,3111,3115,3113,3118,3105,3121,3199,3107,3110,3116,3103,3112,3114,7116,7111,7103,7105,7108,7120,7113,7106,7119,7117,7102,7115,7104,7110,7121,7199,7109,7101,7107,7118,7112,7114,4106,4108,4111,4117,4104,4115,4113,4107,4102,4199,4109,4116,4105,4110,4103,4112,4101,4114,5103,5106,5108,5111,5104,5113,5102,5199,5110,5107,5109,5105,5112,5101,6103,6104,6199,6105,6102,6101,8101,2101,7401,2202,2299,2201,2203,2210,2211,2205,2204,2206,2209,2208,2207,1201,6403,6408,6409,6402,6410,6401,6407,6404,6405,6406,6499,2413,2411,2403,2414,2409,2416,2407,2405,2412,2417,2401,2410,2408,2402,2415,2404,2406,2499,7205,7216,7211,7213,7215,7210,7202,7204,7299,7208,7212,7206,7201,7214,7203,7207,7209,1410,1411,1402,1499", "prdStockRegion1": "53,43,15,25,31,71,41,51,61,81,21,74,22,12,64,24,72,14,52,44,62,42,32,26,11,65,13,63,33,23,73", "dfs_path": {"1303511450378152313_d_800_800_654496298|jpg": "group4/M00/B9/E2/rBYwC1nNuSCAX3lFAAE_RodeA7c079.jpg"}, "value": 0.0, "create_time": 1514755429, "validate_msg": "{}", "_id": 7448953, "outerID": "pop8009072534"}]}'
    str = str.replace('true', '"true"')
    str = str.replace('false', '"false"')
    v = ''
    dict_str = eval(str)
    for key, value in dict_str.items():
        if (type(value) == 'tuple'):
            v = value.__str__()
        elif (type(value) == 'list'):
            v = str(value)
        elif (type(value) == 'dict'):
            v = str(value)
        else:
            v = value
        print 'key=%s\n,value=%s' % (key, v)


if __name__ == '__main__':
    hook_issue()
    # test()
