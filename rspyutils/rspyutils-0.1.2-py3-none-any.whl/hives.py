# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created on MAY 21, 2018
@author: zhanglanhui
hive
"""
from pyhive import hive


class HiveClient:
    def __init__(self, config, section, authMechanism="KERBEROS"):
        """
        create connection to hive server2
        """
        host = config[section]['Host']
        port = int(config[section]['Port'])
        user = config[section]['User']
        password = config[section]['Password']
        db_name = config[section]['Db_name']
        self.conn = hive.connect(host=host,
                                 port=port,
                                 auth=authMechanism,
                                 kerberos_service_name="hive",
                                 database=db_name)

    def query_hive(self, sql):
        """
        query
        """
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()

    def close_hive(self):
        """
        close connection
        """
        self.conn.close()
