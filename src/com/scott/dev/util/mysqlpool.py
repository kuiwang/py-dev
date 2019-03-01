# -*- coding:utf-8 -*-
# mysql连接池
'''
Created on 2018年11月30日

@author: user
'''
"""
Python Mysql Connection Pool

"""
import os, sys
import json, logging
import traceback
import pymysql
from DBUtils.PooledDB import PooledDB

# reload(sys)  
# sys.setdefaultencoding('utf8')

PY_GEN_PATH = "D:/download/pygen/".replace('/', os.sep)
logger = logging.getLogger('mysql_conn_pool_utils')
LOG_FILE = 'mysql_conn_pool.log'
LOG_FORMATTER = '%(asctime)s-%(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s'

SRC_NAME = "src"
CONF_DIR = os.path.join(os.getcwd().split(SRC_NAME)[0], SRC_NAME, 'conf')
MYSQL_JSON_CFG = "mysql_json_all.cfg"


class MySQLConnPool(object):
    """
        MYSQL数据库对象，负责产生数据库连接 ,
                采用连接池实现获取连接对象:conn = Mysql.getConn()
               释放连接对象:conn.close()或del conn
    """

    @staticmethod
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
        console.setLevel(level=logging.DEBUG)
        console.setFormatter(fmter)
        logger.addHandler(console)

    # 连接池对象
    __pool = None

    def __init__(self, db):
        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        self._conn = MySQLConnPool.__getConn(db)
        self._cur = self._conn.cursor()
    
    @staticmethod
    def __getConn(dbname=None):
        MySQLConnPool.config_logger()
        if dbname is None:
            dbname = 'test'
            logger.info("config database name is null ,use default:[" + dbname + "] instead!")
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        if MySQLConnPool.__pool is None:
            try:
                config = find(MYSQL_JSON_CFG, CONF_DIR)
                with open(config, "r") as cfg_file:
                    load_dict = json.load(cfg_file)
                    h = load_dict['database'][dbname]['host']
                    u = load_dict['database'][dbname]['user']
                    p = load_dict['database'][dbname]['password']
                    prt = load_dict['database'][dbname]['port']
                    cs = load_dict['database'][dbname]['charset']
                    database = load_dict['database'][dbname]['db']
                    logger.info("getConn | host:" + h + " | user:" + u + " | port:" + str(prt) + " | charset:" + cs + " | database:" + database)
                    __pool = PooledDB(creator=pymysql, mincached=1 , maxcached=20 , host=h , port=prt , user=u, passwd=p , db=database, use_unicode=True, charset=cs)
            except Exception as e:
                logger.error(traceback.format_exc())
                logger.error("getConn | cannot create mysql connect")
        conn = __pool.connection()
        return conn
    
    def queryall(self, sql, param=None):
        """
            @summary: 执行查询，并取出所有结果集
            @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
            @param param: 可选参数，条件列表值（元组/列表）
            @return: result list(字典对象)/boolean 查询到的结果集
        """
        rows = None
        try:
            if param is None:
                rows = self._cur.execute(sql)
            else:
                rows = self._cur.execute(sql, param)
            if rows > 0:
                result = self._cur.fetchall()
            else:
                result = False
            logger.info("queryall | sql:" + sql + " | rows:" + str(rows))
            return result
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error("queryall | sql:{} | param:{}".format(sql, param))

    def queryone(self, sql, param=None):
        """
            @summary: 执行查询，并取出第一条
            @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
            @param param: 可选参数，条件列表值（元组/列表）
            @return: result list/boolean 查询到的结果集
        """
    
        row = None
        try:
            if param is None:
                row = self._cur.execute(sql)
            else:
                row = self._cur.execute(sql, param)
            if row > 0:
                result = self._cur.fetchone()
            else:
                result = False
            logger.info("queryone | sql:" + sql + " | row:" + str(row))
            return result
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error("queryone | sql:{} | param:{}".format(sql, param))
    
    def querymany(self, sql, num, param=None):
        """
            @summary: 执行查询，并取出num条结果
            @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
            @param num:取得的结果条数
            @param param: 可选参数，条件列表值（元组/列表）
            @return: result list/boolean 查询到的结果集
        """
        rows = None
        try:
            if param is None:
                rows = self._cur.execute(sql)
            else:
                rows = self._cur.execute(sql, param)
            if rows > 0:
                result = self._cur.fetchmany(num)
            else:
                result = False
            logger.info("querymany | sql:" + sql + " | num:" + str(num) + " | rows:" + str(rows))
            return result
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error("querymany | sql:{} | param:{}".format(sql, param))
    
    def insertone(self, sql, value):
        """
            @summary: 向数据表插入一条记录
            @param sql:要插入的ＳＱＬ格式
            @param value:要插入的记录数据tuple/list
            @return: insertId 受影响的行数
        """
    
        lastrowid = 0
        try:
            self._cur.execute(sql, value)
            lastrowid = self._cur.lastrowid
            logger.error("insertone | sql:{} | param:{} | rowid:{}".format(sql, value, str(lastrowid)))
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error("insertone | sql:{} | param:{}".format(sql, value))
    
        return lastrowid
    
    def insertmany(self, sql, values=None):
        """
            @summary: 向数据表插入多条记录
            @param sql:要插入的ＳＱＬ格式
            @param values:要插入的记录数据tuple(tuple)/list[list]
            @return: cnt 受影响的行数
        """
        cnt = 0
        try:
            cnt = self._cur.executemany(sql, values)
            logger.info("insertmany | sql:{} | param:{} | cnt:{}".format(sql, values, str(cnt)))
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error("insertmany | sql:{} param:{}".format(sql, values))
    
        return cnt
    
    def execute(self, sql, param=None):
        """
                    执行sql语句:修改或删除
            @param sql: sql语句
            @param param: string|list
            @return: 影响数量
        """
        cnt = 0
        try:
            if param is None:
                cnt = self._cur.execute(sql)
            else:
                cnt = self._cur.execute(sql, param)
            logger.info("execute | sql:{} | param:{} | cnt:{}".format(sql, param, str(cnt)))
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error("execute | sql:{} | param:{}".format(sql, param))
    
        return cnt
    
    def update(self, sql, param=None):
        """
            @summary: 更新数据表记录
            @param sql: ＳＱＬ格式及条件，使用(%s,%s)
            @param param: 要更新的  值 tuple/list
            @return: cnt 受影响的行数
        """
        return self.execute(sql, param)
    
    def delete(self, sql, param=None):
        """
            @summary: 删除数据表记录
            @param sql: ＳＱＬ格式及条件，使用(%s,%s)
            @param param: 要删除的条件 值 tuple/list
            @return: cnt 受影响的行数
        """
        return self.execute(sql, param)
    
    def __getInsertId(self):
        """获取当前连接最后一次插入操作生成的id,如果没有则为０
        """
        self._cur.execute("SELECT @@IDENTITY AS id")
        result = self._cur.fetchall()
        return result[0]['id']
    
    def begin(self):
        """
        @summary: 开启事务
        """
        self._conn.autocommit(0)
 
    def end(self, option='commit'):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()
 
    def dispose(self, isEnd=1):
        """
        @summary: 释放连接池资源
        """
        if isEnd == 1:
            self.end('commit')
        else:
            self.end('rollback');
        self._cur.close()
        self._conn.close()


def find(name, path):
    """ 查找文件路径 """
    for root, dirs, files in os.walk(path):
        if name in files:
            # logger.info("filepath:" + os.path.join(root, name))
            return os.path.join(root, name)


if __name__ == '__main__':
    conn = MySQLConnPool('test')
    
    # 批量插入
    """
    sql_str = "insert into test_users(email, password) values (%s, %s)"
    arrays = [
        ("aaa@126.com", "111111"),
        ("bbb@126.com", "222222"),
        ("ccc@126.com", "333333"),
        ("ddd@126.com", "444444")
    ]
    logger.info("插入数据:" + str(conn.insertmany(sql_str, arrays)))
    """
    '''
    # 查询
    logger.info("查询全表:")
    sql_all = 'select * from test_users'
    result = conn.queryall(sql_all)
    if result:
        for row in result:
            logger.info("{} | {} | {}".format(str(row[0]), row[1], str(row[2])))
    
    # 条件查询
    single_cond_sql = "select * from test_users where 1 = 1 and id <= %s"
    param = (3,)
    result = conn.queryall(single_cond_sql, param)
    if result:
        for row in result:
            logger.info("{} | {} | {}".format(str(row[0]), row[1], str(row[2])))
    # 多提交查询
    multi_cond_sql = "select * from test_users where email = %s and password = %s"
    param = ("bbb@126.com", "222222")
    result = conn.queryall(multi_cond_sql, param)
    if result:
        for row in result:
            logger.info("{} | {} | {}".format(str(row[0]), row[1], str(row[2])))
    
    # 更新
    update_sql = "update test_users set email = %s where id = %s "
    param = ('new_11@126.com', 1)
    update_count = conn.update(update_sql, param)
    logger.info("update_count:" + str(update_count))
    
    update_sql = "update test_users set email = %s where id = %s "
    param = ['2_new_new@126.com', 2]
    update_count = conn.update(update_sql, param)
    logger.info("update_count:" + str(update_count))
    
    # 删除
    delete_sql = "delete from test_users where id = %s"
    param = [3]
    delete_count = conn.delete(delete_sql, param)
    logger.info("delete_count:" + str(delete_count))
    
    # 全部查询
    sql_all = 'select * from test_users'
    result = conn.queryall(sql_all)
    if result:
        for row in result:
            logger.info("{} | {} | {}".format(str(row[0]), row[1], str(row[2])))
    '''
    # 总条数
    qryone_sql = "select count(*) from test_users"
    result = conn.queryone(qryone_sql)
    logger.info("table size:" + str(result[0]))
    '''
    logger.info("一列:" + str(conn.queryall("select email from test_users where id <= %s", 2)))
    logger.info("多列:" + str(conn.queryall("select * from test_users where email = %s and password = %s", ("bbb@126.com", "222222"))))
    
    # 更新|删除
    logger.info("更新:" + str(conn.update("update test_users set email = %s where id = %s", ('new@126.com', 1))))
    logger.info("删除:" + str(conn.delete("delete from test_users where id = %s", 4)))

    # 查询
    logger.info("再次查询全表:" + str(conn.queryall("select * from test_users")))
    logger.info("数据总数:" + str(conn.queryone("select count(*) from test_users")))
    '''
    # 释放资源
    conn.dispose()
