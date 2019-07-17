# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@version: 0.1
@author: gabriel
@file: mysqls.py
@time: 2018/11/20 15:12
"""
import pymysql.cursors


class MysqlClient:
    def __init__(self, config, section):
        host = config[section]['Host']
        port = int(config[section]['Port'])
        user = config[section]['User']
        password = config[section]['Password']
        db_name = config[section]['Db_name']
        # 打开sqlserver数据库连接
        self.db_info = pymysql.connect(host=host, user=user, passwd=password, db=db_name, port=port, charset="utf8")

    def query_mysql(self, sql):
        """
        query
        """
        with self.db_info.cursor() as cursor:
            cursor.execute(sql)
            self.db_info.commit()
            return cursor.fetchall()

    def cursor_mysql(self):
        return self.db_info.cursor()

    def ping_mysql(self):
        self.db_info.ping(True)

    def close_mysql(self):
        """
        close connection
        """
        self.db_info.close()
