# -*- coding:utf-8 -*-
# 程序生成配置文件
'''
Created on 2018年11月30日

@author: user
'''

from ConfigParser import SafeConfigParser
import os, sys
import logging
from logger import config_file

reload(sys)  
sys.setdefaultencoding('utf8')
# import configparser
INI_CONFIG_FILE_NAME = "dev_config.ini"
JSON_CONFIG_FILE_NAME = "dev_config.json"
SRC_NAME = "src"
CONF_DIR = os.path.join(os.getcwd().split(SRC_NAME)[0], SRC_NAME, 'conf')
PY_GEN_PATH = "D:/download/pygen/".replace('/', os.sep)
logger = logging.getLogger('write_config')
LOG_FILE = 'write_config.log'
LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'


def config_logger():
    logger.setLevel(logging.DEBUG)
    dest_dir = os.path.join(PY_GEN_PATH)
    if not os.path.exists(dest_dir):
        logger.info('文件夹:' + dest_dir + '不存在')
        os.makedirs(dest_dir, 777)
        logger.info('创建文件夹 ' + dest_dir + '成功')
    handler = logging.FileHandler(os.path.join(PY_GEN_PATH, LOG_FILE))
    handler.setLevel(logging.DEBUG)
    fmter = logging.Formatter(LOG_FORMATTER)
    handler.setFormatter(fmter)
    logger.addHandler(handler)
    # 控制台打印
    console = logging.StreamHandler()
    console.setLevel(level=logging.DEBUG)  # 设置为INFO级别
    console.setFormatter(fmter)
    logger.addHandler(console)


def gen_config_ini():
    config = SafeConfigParser()
    if not os.path.exists(CONF_DIR):
        os.makedirs(CONF_DIR, 777)
    config_file = os.path.join(CONF_DIR, INI_CONFIG_FILE_NAME)
    logger.info("read config file:" + config_file)
    config.read(config_file)
    sections = config.sections()
    print 
    if (sections.index("main") < 0):
        config.add_section('main')
        config.set('main', 'key1', 'value1')
        config.set('main', 'key2', 'value2')
        config.set('main', 'key3', 'value3')
        logger.info("add section main into config file")
        with open(config_file, 'w') as f:
            config.write(f)
            logger.info("write new section into config file successful!")
    else:
        logger.info("section main is existed!")


def gen_config_json():
    logger.info("generate json config file now!")
    import json
    config = {'key1': 'value1', 'key2': 'value2'}
    if not os.path.exists(CONF_DIR):
        os.makedirs(CONF_DIR, 777)
    config_file = os.path.join(CONF_DIR, JSON_CONFIG_FILE_NAME)
    logger.info("json config file name:" + config_file)
    with open(config_file, 'w') as f:
        json.dump(config, f)
        logger.info("json config file generated successful!")


if __name__ == '__main__':
    config_logger()
    # gen_config_ini()
    gen_config_json()
