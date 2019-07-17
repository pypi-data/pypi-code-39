# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@version: 0.1
@author: gabriel
@file: sqlservers.py
@time: 2018/11/20 15:12
"""
import pymssql


class SqlserverClient:
    def __init__(self, config, section):
        host = config[section]['Host']
        port = int(config[section]['Port'])
        user = config[section]['User']
        password = config[section]['Password']
        db_name = config[section]['Db_name']
        # 打开sqlserver数据库连接
        self.db = pymssql.connect(host=host, user=user, password=password, database=db_name, port=port, charset="utf8")

    def query_mssql(self, sql):
        """
        query
        """
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def close_mssql(self):
        """
        close connection
        """
        self.db.close()
