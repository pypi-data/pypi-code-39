#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: mysql.py
Desc: mysql操作类
"""

from dp import utils, constants
from dp.db.mysqlgenerator import MySqlGenerator
import os
import sys
import platform
import time
import logging
if platform.python_version().split('.')[0] == '3':  # python3 use PyMySQL
    import pymysql
    from pymysql import cursors
else:  # python2 use MySQL-Python
    import MySQLdb as pymysql
    from MySQLdb import cursors


class Mysql(object):
    """
        Mysql操作类
    """

    def __init__(self, host, port, user, password, db,
                 charset="utf8", debug=0):
        """
        初始化配置

        :param host: hostname
        :param port: 端口
        :param user: 用户名
        :param password: 密码
        :param db: 库名
        :param charset: 字符集（默认utf8）
        :param debug: 是否打印sql
        :returns: 
        """
        self.host = host
        self.port = int(port)
        self.user = user
        self.password = password
        self.db = db
        self.debug_level = debug
        self.conn = None
        self.charset = charset
        self.sqlGen = MySqlGenerator()

    def debug(self, sql):
        """debug"""
        logging.info('SQL: {};'.format(sql))
        if self.debug_level:
            print('SQL: {};'.format(sql))

    def connect(self):
        """connect"""
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                    password=self.password, db=self.db, charset=self.charset,
                                    cursorclass=cursors.DictCursor)

    def disconnect(self):
        """disconnect"""
        if self.conn:
            self.conn.close()

    def insert(self, table, values):
        """
        插入数据

        :param table: 表名
        :param values: dict键值对
        :returns: 数据id
        """
        sql = self.sqlGen.insert(table=table, values=values)
        try:
            self.connect()
            cursor = self.conn.cursor()
            self.debug(sql)
            ret = cursor.execute(sql)
            # print(ret)
            lastrowid = cursor.lastrowid
            self.conn.commit()
            cursor.close()
            self.conn.close()
            return lastrowid
        except:
            logging.error("{}\t{}".format(sql, utils.get_trace()))
            return 0

    def update(self, table, where, values):
        """
        更新数据

        :param table: 表名
        :param where: where条件键值对
        :param values: 要更新的键值对
        :returns: 
        """
        if not isinstance(where, dict):
            logging.error("where must be dict")
        self.connect()
        cursor = self.conn.cursor()
        sql = self.sqlGen.update(table=table, where=where, values=values)
        self.debug(sql)
        ret = cursor.execute(sql)
        # print(ret)
        self.conn.commit()
        cursor.close()
        self.conn.close()
        return ret

    def query(self, table, where=None, select='*', groupby='', orderby='', limit=1000):
        """
        查询数据

        :param table: 表名
        :param where: where条件键值对
        :param select: 查询字段
        :param groupby: 分组
        :param orderby: 排序
        :param limit: 限定返回条数(默认1000)
        :returns: 结果集list
        """
        res = []
        self.connect()
        cursor = self.conn.cursor()
        where = where if where is not None else {}
        sql = self.sqlGen.query(table=table, select=select, where=where, groupby=groupby, orderby=orderby, limit=limit)
        self.debug(sql)
        cursor.execute(sql)
        for data in cursor.fetchall():
            res.append(data)
        cursor.close()
        self.conn.close()
        return res

    def count(self, table, where=None):
        """
        查询记录条数

        :param table: 表名
        :param where: where条件键值对
        :returns: 记录条数
        """
        res = []
        self.connect()
        cursor = self.conn.cursor()
        where = where if where is not None else {}
        sql = self.sqlGen.query(table=table, select='count(*) as count', where=where)
        self.debug(sql)
        cursor.execute(sql)
        for data in cursor.fetchall():
            res.append(data)
        cursor.close()
        self.conn.close()
        if len(res) > 0:
            return int(res[0]['count'])
        return 0

    def delete(self, table, where):
        """
        删除数据

        :param table: 表名
        :param where: where条件键值对
        :returns: 
        """
        self.connect()
        cursor = self.conn.cursor()
        sql = self.sqlGen.delete(table=table, where=where)
        self.debug(sql)
        ret = cursor.execute(sql)
        # print(ret)
        self.conn.commit()
        cursor.close()
        self.conn.close()
        return ret

    def execute(self, sql):
        """
        复杂sql执行（慎用-注意性能）

        :param sql: 特殊sql语句
        :returns: 
        """
        sql = sql.strip()
        qtype = sql.split()[0].upper()

        res = []
        self.connect()
        cursor = self.conn.cursor()
        self.debug(sql)
        ret = cursor.execute(sql)
        # print(ret)
        if qtype == 'SELECT':
            for data in cursor.fetchall():
                res.append(data)
        else:
            res = ret
            self.conn.commit()
        cursor.close()
        self.conn.close()
        return res


if __name__ == '__main__':
    """测试"""
    # log
    utils.init_logging(log_file='mysql', log_path=constants.APP_PATH)

    # mysql
    #from dp.db.mysql import Mysql
    db = Mysql(host='127.0.0.1', port='3306', user='root', password='Qazwsx!2#4%6&8(0', db='test', debug=1)
    table = 'test'
    # insert
    ret = db.insert(table, {'val': str(time.time())+'"; delete * from test'})
    print(ret)
    ret = db.insert(table, {'id': 1, 'val': str(time.time())+'"; delete * from test'})
    print(ret)
    # delete
    ret = db.delete(table, {'id': '< 2'})
    print(ret)
    # update
    ret = db.update(table, {'id': 2}, {'val': '6663' + str(time.time())})
    print(ret)
    # query
    res = db.query(table, where={'id': 'between 2 and 100', 'val': "like '66%'"})
    print(res)
    res = db.query(table, select='distinct id,val', orderby='id desc', limit=10)  # , {'val': '6663 or 1=2'})
    print(res)
    res = db.query(table, select='val', where={'id': 'in (2,3)'}, groupby='val')
    print(res)
    res = db.query(table, select='val', where={'id': 'in (2,3)'}, groupby='val')
    print(res)
    # count
    ret = db.count(table, where={'id': '> 2'})
    print(ret)
    # sql
    res = db.execute('select a.id,a.val from (select id,val from test) as a where a.id<3')
    print(res)
    res = db.execute("update test set val='6663' where id<3")
    print(res)
