'''
Created on 2018年11月15日

@author: user
'''

import os
import argparse
import random
import hashlib
from datetime import datetime


class PackageTool:

    def __init__(self, sql, account, pack_name):
        self.sql = sql
        self.account = account
        self.csv_name = '{account}_5_{pack_name}.csv'.format(account=account, pack_name=pack_name)
        self.tmp = "{}.tar.gz".format(hashlib.md5(
            '{p1}_{p2}_{p3}'.format(p1=self.csv_name, p2=datetime.now(), p3=random.randint(2, 10e5)).encode(
                'utf-8')).hexdigest())
        self.tar_name = self.tmp[2:]
        self.today = datetime.now().strftime("%Y%m%d")
        self.cmds = []

    def get_cmds(self, sql, csv_name, tar_name):
        self.cmds.append(
            '''clickhouse-client -h 172.22.16.46 --query="{sql}" >> "{csv_name}"'''.format(sql=sql, csv_name=csv_name))
        self.cmds.append("tar czvf {tar_name}  {csv_name}".format(tar_name=tar_name, csv_name=csv_name))

    def get_ip(self):
        out = os.popen(
            "ifconfig | grep 'inet addr:' | grep -v '127.0.0.1' | cut -d: -f2 | awk '{print $1}' | head -1").read()
        return out.strip()

    def escute(self):
        self.get_cmds(self.sql, self.csv_name, self.tar_name)
        for cmd in self.cmds:
            print(cmd)
            os.system(cmd)
        res = "cp\t{ip}:{path}/{tar_name}\t40.2:/home/zampread/chexiang01/{ts}/ \n".format(ip=self.get_ip(), 
                                                                                           path=os.path.abspath('.'), 
                                                                                           tar_name=self.tar_name, 
                                                                                           ts=self.today)
        print("please send this massage to Roger!")
        print(res)
        fo = open("log.txt", "a+")
        fo.write(res)
        fo.close()


def init_parser():
    print('begin pack ...')
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "-sql",
                        type=str,
                        dest='sql',
                        required=True,
                        help="please input clickhouse sql type(str)"
                        )
    parser.add_argument("-a", "-account",
                        type=int,
                        dest='account',
                        help="please input account type(int)"
                        )
    parser.add_argument("-f", "-name",
                        type=str,
                        dest='name',
                        help="please input pack name type(str)"
                        )
    return parser


if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args()

    my_sql = args.sql
    my_account = args.account
    my_name = args.name

    pt = PackageTool(my_sql, my_account, my_name)
    pt.escute()

