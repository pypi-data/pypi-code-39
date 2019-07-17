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

    def commit(self):
        self.db_info.commit()

    def rollback(self):
        self.db_info.rollback()

    def update_table_data(self, data, table, field, times=1000):
        import math
        if len(data) < 1:
            return

        try:
            n = times
            m = int(math.ceil(len(data) / n))
            for l in [data[i:i + m] for i in range(0, len(data), m)]:
                if len(set([x[0] for x in l])) != len(([x[0] for x in l])):
                    raise NameError('update_table_data error,field:', field)

                sql = """
                INSERT INTO 
                {t} (uid,{f}) 
                VALUES {d} on DUPLICATE key 
                update {f}=values({f});
                """.format(t=table,
                           d=','.join(["({},'{}')".format(x[0], x[1]) for x in l if int(x[0]) > 0]),
                           f=field)
                with self.db_info.cursor() as cursor:
                    cursor.execute(sql)
                    self.db_info.commit()
        except Exception as e:
            self.db_info.rollback()
            raise e
