# -*- coding:utf-8 -*-
# mysql简单封装工具
'''
Created on 2018年11月30日

@author: user
'''
"""
Python Mysql 工具包
"""
import os, sys
import json, logging
import traceback
import pymysql

reload(sys)  
sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/".replace('/', os.sep)
logger = logging.getLogger('mysqlutils')
LOG_FILE = 'mysqlutils.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

SRC_NAME = "src"
CONF_DIR = os.path.join(os.getcwd().split(SRC_NAME)[0], SRC_NAME, 'conf')
MYSQL_JSON_CFG = "mysql_json_all.cfg"


def config_logger():
    logger.setLevel(logging.DEBUG)
    dest_dir = os.path.join(CONF_DIR)
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


def find(name, path):
    """ 查找文件路径 """
    for root, dirs, files in os.walk(path):
        if name in files:
            # logger.info("filepath:" + os.path.join(root, name))
            return os.path.join(root, name)


def connect_mysql(cfg_db=None):
    """ 创建链接 """
    if cfg_db is None:
        cfg_db = 'test'
    try:
        config = find(MYSQL_JSON_CFG, CONF_DIR)
        with open(config, "r") as file:
            load_dict = json.load(file)
            h = load_dict['database'][cfg_db]['host']
            u = load_dict['database'][cfg_db]['user']
            p = load_dict['database'][cfg_db]['password']
            port = load_dict['database'][cfg_db]['port']
            cs = load_dict['database'][cfg_db]['charset']
            db = load_dict['database'][cfg_db]['db']
            logger.info("connect_mysql | host:" + h + " | user:" + u + " | port:" + str(port) + " | charset:" + cs + " | database:" + db)
            conn = pymysql.connect(database=db, host=h, user=u, password=p, charset=cs, port=port)
        return conn
        # return pymysql.connect(cursorclass=pymysql.cursors.DictCursor, **load_dict)
    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error("connect_mysql | cannot create mysql connect")


def queryall(sql, param=None):
    """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
    """
    con = connect_mysql()
    cur = con.cursor()

    rows = None
    try:
        # cur.execute(sql, param)
        # rows = cur.fetchall()
        if param is None:
            rows = cur.execute(sql)
        else:
            rows = cur.execute(sql, param)
        if rows > 0:
            result = cur.fetchall()
        else:
            result = False
        logger.info("queryall | sql:" + sql + " | rows:" + str(rows) + " | result:" + result)
    except Exception as e:
        con.rollback()
        logger.error(traceback.format_exc())
        logger.error("queryall | [sql]:{} [param]:{}".format(sql, param))

    cur.close()
    con.close()
    return result


def queryone(sql, param=None):
    """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
    """
    con = connect_mysql()
    cur = con.cursor()

    row = None
    try:
        # cur.execute(sql, param)
        # row = cur.fetchone()
        if param is None:
            row = cur.execute(sql)
        else:
            row = cur.execute(sql, param)
        if row > 0:
            result = cur.fetchone()
        else:
            result = False
        logger.info("queryone | sql:" + sql + " | rows:" + str(row) + " | result:" + result)
    except Exception as e:
        con.rollback()
        logger.error(traceback.format_exc())
        logger.error("queryone | [sql]:{} [param]:{}".format(sql, param))

    cur.close()
    con.close()
    # return simple_value(row)
    return result


def querymany(sql, num, param=None):
    """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
    """
    con = connect_mysql()
    cur = con.cursor()

    rows = None
    try:
        # cur.execute(sql, param)
        # rows = cur.fetchall()
        if param is None:
            rows = cur.execute(sql)
        else:
            rows = cur.execute(sql, param)
        if rows > 0:
            result = cur.fetchmany(num)
        else:
            result = False
        logger.info("querymany | sql:" + sql + " | num:" + str(num) + " | rows:" + str(rows) + " | result:" + result)
    except Exception as e:
        con.rollback()
        logger.error(traceback.format_exc())
        logger.error("querymany | [sql]:{} [param]:{}".format(sql, param))

    cur.close()
    con.close()
    return result


def insertone(sql, value):
    """
        @summary: 向数据表插入一条记录
        @param sql:要插入的ＳＱＬ格式
        @param value:要插入的记录数据tuple/list
        @return: insertId 受影响的行数
    """
    con = connect_mysql()
    cur = con.cursor()

    lastrowid = 0
    try:
        cur.execute(sql, value)
        con.commit()
        lastrowid = cur.lastrowid
        logger.info("insertone | rowid:" + str(lastrowid))
    except Exception as e:
        con.rollback()
        logger.error(traceback.format_exc())
        logger.error("insertone | [sql]:{} [param]:{}".format(sql, value))

    cur.close()
    con.close()
    return lastrowid


def insertmany(sql, values=None):
    """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
    """
    con = connect_mysql()
    cur = con.cursor()

    cnt = 0
    try:
        cnt = cur.executemany(sql, values)
        logger.info("insertmany count:" + str(cnt))
        con.commit()
    except Exception as e:
        con.rollback()
        logger.error(traceback.format_exc())
        logger.error("insertmany | [sql]:{} [param]:{}".format(sql, values))

    cur.close()
    con.close()
    return cnt


def execute(sql, param=None):
    """
                执行sql语句:修改或删除
        @param sql: sql语句
        @param param: string|list
        @return: 影响数量
    """
    con = connect_mysql()
    cur = con.cursor()

    cnt = 0
    try:
        cnt = cur.execute(sql, param)
        con.commit()
        logger.info("execute | count:" + str(cnt))
    except Exception as e:
        con.rollback()
        logger.error(traceback.format_exc())
        logger.error("execute | [sql]:{} [param]:{}".format(sql, param))

    cur.close()
    con.close()
    return cnt


def update(sql, param=None):
    """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
    """
    con = connect_mysql()
    cur = con.cursor()

    cnt = 0
    try:
        cnt = cur.execute(sql, param)
        con.commit()
        logger.info("update | count:" + str(cnt))
    except Exception as e:
        con.rollback()
        logger.error(traceback.format_exc())
        logger.error("update | [sql]:{} [param]:{}".format(sql, param))

    cur.close()
    con.close()
    return cnt


def delete(sql, param=None):
    """
        @summary: 删除数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要删除的条件 值 tuple/list
        @return: count 受影响的行数
    """
    con = connect_mysql()
    cur = con.cursor()

    cnt = 0
    try:
        cnt = cur.execute(sql, param)
        con.commit()
        logger.info("delete | count:" + str(cnt))
    except Exception as e:
        con.rollback()
        logger.error(traceback.format_exc())
        logger.error("delete | [sql]:{} [param]:{}".format(sql, param))

    cur.close()
    con.close()
    return cnt


if __name__ == '__main__':
    config_logger()
    logger.info("hello everyone!!!")
    logger.info("删表:" + str(execute('drop table test_users')))

    sql = '''
            CREATE TABLE `test_users` (
              `id` int(11) NOT NULL AUTO_INCREMENT,
              `email` varchar(255) NOT NULL,
              `password` varchar(255) NOT NULL,
              PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='测试用的, 可以直接删除';
            '''
    logger.info("建表:" + str(execute(sql)))

    # 批量插入
    sql_str = "insert into test_users(email, password) values (%s, %s)"
    arrays = [
        ("aaa@126.com", "111111"),
        ("bbb@126.com", "222222"),
        ("ccc@126.com", "333333"),
        ("ddd@126.com", "444444")
    ]
    logger.info("插入数据:" + str(insertmany(sql_str, arrays)))

    # 查询
    # 尽量使用limit
    logger.info("只取一行:" + queryone("select * from test_users limit %s,%s", (0, 1)))
    # logger.info("只取一行:" + queryall("select * from test_users limit %s,%s", (0, 2)))
    logger.info("查询全表:" + (queryall("select * from test_users")))

    # 条件查询
    logger.info("一列:" + str(queryall("select email from test_users where id <= %s", 2)))
    logger.info("多列:" + str(queryall("select * from test_users where email = %s and password = %s", ("bbb@126.com", "222222"))))

    # 更新|删除
    logger.info("更新:" + str(update("update test_users set email = %s where id = %s", ('new@126.com', 1))))
    logger.info("删除:" + str(delete("delete from test_users where id = %s", 4)))

    # 查询
    logger.info("再次查询全表:" + str(queryall("select * from test_users")))
    logger.info("数据总数:" + str(queryone("select count(*) from test_users")))
