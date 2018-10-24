#! /usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import os
import sys


def datetime_test():
    now = datetime.datetime.now()
    print 'now is:',now
    return now

def func_test():
    datetime_test()

if __name__ == '__main__':
    func_test();
