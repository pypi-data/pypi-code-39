#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xytool.config import Config
# from xytool.commom.xylog import faillog
import pymysql

host = Config().get_config("Database-config","host")
user = Config().get_config("Database-config","user")
password = Config().get_config("Database-config","password")
db = Config().get_config("Database-config","db")
charset = Config().get_config("Database-config","charset")

print(host)
print(user)
print(password)
print(db)

def main():
    try:
        conn = pymysql.connect(host='172.18.16.21', user=user, passwd='', db='mysql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM nike_ippool")
        for r in cur:
            print(r)
        cur.close()
        conn.close()
    except pymysql.err.InternalError as error:
        print(format(error))

if __name__ == '__main__':
    main()
    