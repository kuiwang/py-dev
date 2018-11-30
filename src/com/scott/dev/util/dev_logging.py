# -*- coding:utf-8 -*-
# logging模块使用
'''
Created on 2018年11月28日

@author: user
'''
import logging, os
PY_GEN_PATH = "D:/download/pygen/".replace('/', os.sep)
LOG_PATH = os.path.join(PY_GEN_PATH, 'log')
LOG_FILE = 'test.log'
LOG_FORMATTER = '%(asctime)s-文件名称:【%(filename)s】-函数名:【%(funcName)s】-行号:【%(lineno)d】-线程名:【%(threadName)s】-线程ID:【%(process)d】-模块名称:【%(name)s】-日志级别:【%(levelname)s】-%(message)s'


def logging_basic():
    logging.basicConfig(level=logging.NOTSET, format=LOG_FORMATTER)
    logger = logging.getLogger(__name__)
    logger.info('INFO level log')
    logger.debug('DEBUG level log')
    logger.warning('WARNING level log')
    logger.error('ERROR level log')


# 只将日志信息写入文件
def logtofile():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH, 777)
        print '日志路径不存在,已自动创建'
    handler = logging.FileHandler(os.path.join(LOG_PATH, LOG_FILE))
    handler.setLevel(logging.DEBUG)
    fmter = logging.Formatter(LOG_FORMATTER)
    handler.setFormatter(fmter)
    logger.addHandler(handler)
    
    logger.info('INFO level log into logfile')
    logger.debug('DEBUG level log into logfile')
    logger.warning('WARNING level log into logfile')
    logger.error('ERROR level log into logfile')


# 日志信息既写入文件同时控制台打印出来
def logToConsoleAndFile():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH, 777)
        print '日志路径不存在,已自动创建'
    handler = logging.FileHandler(os.path.join(LOG_PATH, LOG_FILE))
    handler.setLevel(logging.DEBUG)
    fmter = logging.Formatter(LOG_FORMATTER)
    handler.setFormatter(fmter)
    logger.addHandler(handler)
    
    # 控制台打印
    console = logging.StreamHandler()
    console.setLevel(level=logging.INFO)  # 设置为INFO级别
    console.setFormatter(fmter)
    logger.addHandler(console)
    logger.info('INFO level log into logfile')
    logger.debug('DEBUG level log into logfile')
    logger.warning('WARNING level log into logfile')
    logger.error('ERROR level log into logfile')


if __name__ == '__main__':
    # logging_basic()
    # logtofile()
    logToConsoleAndFile()
