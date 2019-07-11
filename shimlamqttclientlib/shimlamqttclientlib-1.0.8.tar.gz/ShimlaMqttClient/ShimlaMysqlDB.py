#!/usr/bin/env python3.5
import MySQLdb

class Database(object):
   def __init__(self, db, host, user, passwd):
      self.db = db
      self.host = host
      self.user = user
      self.passwd = passwd
      self.conn = MySQLdb.connect(host=self.host, db=self.db, user=self.user, passwd=self.passwd)
      assert self.conn
      self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)

   def query(self, queryStr):
      self.cursor.execute(queryStr)
      return self.cursor.fetchall()

   def commit(self):
      self.conn.commit()

   def close(self):
      self.conn.close()
