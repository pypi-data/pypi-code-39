#!/usr/bin/env python3
#coding: utf-8
"""
@author: sunway
@version v1
"""
import os
basedir=os.path.dirname(os.path.abspath(__file__))
logdir=os.path.join(basedir,'logs')
if not os.path.exists(logdir):
    os.mkdir(logdir)
import MySQLdb
import random,string
import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='%s/dbmgt.log' %(logdir),
                filemode='a')
class DBtool(object):
    def __init__(self, **kwargs):
        self.__dbhost = kwargs['dbhost']
        self.__dbport = kwargs['dbport']
        self.__dbuser = kwargs['dbuser']
        self.__dbpwd = kwargs['dbpwd']
        self.__dbname = kwargs['dbname']
        self.__charset = kwargs['charset']
        self.conn = None
    def getConn(self):
        try:
            self.conn = MySQLdb.connect(host=self.__dbhost, port=self.__dbport, user=self.__dbuser, password=self.__dbpwd,
                                    db=self.__dbname, charset=self.__charset)
            if self.conn:
                return self.conn
            else:
                return "连接数据库失败"
        except Exception as e:
            raise e
            print(e.args)
    def getColumns(self,sql):
        cursor = self.getConn().cursor()
        try:
            cursor.execute(sql)
            cols=[col[0] for col in cursor.description]
            return cols
        except Exception as e:
            raise Exception(e)
        finally:
            cursor.close()
            self.conn.close()
    def sqlDml(self, sql):
        cursor = self.getConn().cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
            if cursor.rowcount > 0:
                # return 0 表示修改成功
                return 0
            else:
                # return2 表示行数无影响
                return 2
        except Exception as e:
            self.conn.rollback()
            raise Exception('error')
        finally:
            cursor.close()
            self.conn.close()
    def sqlDmlp(self, sql,*args):
        cursor = self.getConn().cursor()
        try:
            cursor.execute(sql,args)
            self.conn.commit()
            if cursor.rowcount > 0:
                # return 0 表示修改成功
                return 0
            else:
                return 2
        except Exception as e:
            self.conn.rollback()
            raise Exception('error')
        finally:
            cursor.close()
            self.conn.close()
    def sqlDql(self, sql):
        cursor = self.getConn().cursor()
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            logging.exception(e)
        finally:
            cursor.close()
            self.conn.close()
    def sqlDqlp(self, sql,*args):
        cursor = self.getConn().cursor()
        try:
            cursor.execute(sql,args)
            return cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            self.conn.close()
    def sqlDdl(self,sql):
        cursor = self.getConn().cursor()
        try:
            res=cursor.execute(sql)
            return res
        except Exception as e:
            logging.exception(str(e))
            raise e
    def flushPrivs(self):
        cursor = self.getConn().cursor()
        sql='flush privileges'
        try:
            res = cursor.execute(sql)
            return res
        except Exception as e:
            logging.exception(str(e))
            raise e


    def grant_user_privs(self,user,host,db,table=None,privs=[]):
        speprivs=set(set(privs) & set(['super','file','process','replication slave','all']))
        routines = set(set(privs) & set(['create routine', 'alter routine']))
        print('speprivs:',speprivs,'routines',routines)
        if speprivs and routines:
            mix_privs=list(set(set(speprivs) | set(routines)))
            if len(mix_privs) > 1:
                for p in mix_privs:
                    try:
                        if p == 'all':
                            sql = "grant {p} on {db}.* to {user}@\'{host}\'".format(p=p, db=db, user=user, host=host)
                            res = self.sqlDdl(sql)
                        else:
                            sql = "grant {p} on *.* to {user}@\'{host}\'".format(p=p, user=user, host=host)
                            res = self.sqlDdl(sql)
                    except Exception as e:
                        logging.exception(str(e))
                        break
                        return 1
                if res == 0:
                    return 0
                else:
                    return 1
            else:
                if list(mix_privs)[0] == 'all':
                    sql = "grant {p} on {db}.* to {user}@\'{host}\'".format(p=list(speprivs)[0], db=db, user=user,host=host)
                else:
                    sql = "grant {p} on *.* to {user}@\'{host}\'".format(p=list(speprivs)[0], db=db, user=user,host=host)
                print(sql)
                res = self.sqlDdl(sql)
                if res == 0:
                    return 0
                else:
                    return 1
        if list(speprivs):
            if len(speprivs) > 1:
                for p in speprivs:
                    try:
                        if p == 'all':
                            sql = "grant {p} on {db}.* to {user}@\'{host}\'".format(p=p, db=db, user=user, host=host)
                            res = self.sqlDdl(sql)
                        else:
                            sql = "grant {p} on *.* to {user}@\'{host}\'".format(p=p, user=user, host=host)
                            res = self.sqlDdl(sql)
                    except Exception as e:
                        logging.exception(str(e))
                        break
                        return 1
                if res == 0:
                    return 0
                else:
                    return 1
            else:
                if list(speprivs)[0] == 'all':
                    sql = "grant {p} on {db}.* to {user}@\'{host}\'".format(p=list(speprivs)[0], db=db, user=user,host=host)
                else:
                    sql = "grant {p} on *.* to {user}@\'{host}\'".format(p=list(speprivs)[0], db=db, user=user,host=host)
                print(sql)
                res = self.sqlDdl(sql)
                if res == 0:
                    return 0
                else:
                    return 1
        if list(routines):
            if len(routines) > 1:
                for p in routines:
                    sql = "grant {p} on {db}.* to {user}@\'{host}\'".format(p=p, db=db, user=user,host=host)
                    print(sql)
                    try:
                        res = self.sqlDdl(sql)
                    except Exception as e:
                        logging.exception(str(e))
                        break
                        return 1
                if res == 0:
                    return 0
                else:
                    return 1
            else:
                sql = "grant {p} on {db}.* to {user}@\'{host}\'".format(p=list(routines)[0], db=db,user=user,host=host)
                print(sql)
                res = self.sqlDdl(sql)
                if res == 0:
                    return 0
                else:
                    return 1
        if table:
            if len(privs)>1:
                for p in privs:
                    sql="grant {p} on {db}.{table} to {user}@\'{host}\'".format(p=p,db=db,table=table,user=user,host=host)
                    print(sql)
                    res=self.sqlDdl(sql)
                    if res !=0:
                        break
                        return 1
                return 0
            else:
                sql = "grant {p} on {db}.{table} to {user}@\'{host}\'".format(p=privs, db=db, table=table,user=user,host=host)
                print(sql)
                res=self.sqlDdl(sql)
                if res==0:
                    return 0
                else:
                    return 1
        else:
            if len(privs)>1:
                for p in privs:
                    sql = "grant {p} on {db}.* to {user}@\'{host}\'".format(p=p, db=db, user=user,host=host)
                    res=self.sqlDdl(sql)
                    if res !=0:
                        break
                        return 1
                return 0
            else:
                sql = "grant {p} on {db}.* to {user}@\'{host}\'".format(p=privs, db=db, user=user,host=host)
                res=self.sqlDdl(sql)
                if res==0:
                    return 0
                else:
                    return 1

    def colseConn(self):
        self.conn.close()
    def getUser(self,db=None):
            if db:
                sql="select DISTINCT concat(user,'@',host) from mysql.db where db=\'{db}\'".format(db=db)
            else:
                sql="select DISTINCT concat(user,'@',host) from mysql.user"
            return [db[0] for db in self.sqlDql(sql) if not str(db[0]).startswith(('root','dbx','mysql'))]

    def createUser(self,username,pwd):
        user=str(username).split('@')[0]
        host=str(username).split('@')[1]
        sql="create user {user}@\'{host}\' identified by \'{pwd}\'".format(user=user,host=host,pwd=pwd)
        #5.7
        # sql="create user  {user} identified by \'{pwd:s}\' PASSWORD EXPIRE NEVER".format(**kwargs)
        res=self.sqlDdl(sql)
        return res
    def dropUser(self,username):
        user = str(username).split('@')[0]
        host = str(username).split('@')[1]
        if host:
            sql="drop user {user}@{host}".format(user=user,host=host)
            res=self.sqlDdl(sql)
        else:
            sql = "drop user {user}".format(user=user)
            res = self.sqlDdl(sql)
        return res
    def lockUser(self,user,host):
        sql = "alter user \'{username}\'@{host} account lock".format(username=user,host=host)
        print(sql)
        res = self.sqlDdl(sql)
        return res

    def unLockUser(self, user,host):
        sql = "alter user \'{username}\'@{host} account unlock".format(username=user,host=host)
        res = self.sqlDdl(sql)
        return res
    def getPrivileges(self,username):
        sql="show grants for {username}".format(username=username)
        try:
            res=self.sqlDql(sql)
        except Exception as e:
            logging.exception(str(e))
            raise str(e)
        else:
            if res:
                return [p[0] for p in res]
            else:
                return res[0]


    def revokePrivs(self, user, host, db, table=None, privs=[]):
        speprivs = set(set(privs) & set(['super', 'file', 'process', 'replication slave', 'all']))
        routines = set(set(privs) & set(['create routine', 'alter routine']))
        if speprivs and routines:
            mix_privs = list(set(set(speprivs) | set(routines)))
            if len(mix_privs) > 1:
                for p in mix_privs:
                    try:
                        if p == 'all':
                            sql = "revoke {p} on {db}.* from {user}@\'{host}\'".format(p=p, db=db, user=user,
                                                                                    host=host)
                            res = self.sqlDdl(sql)
                        else:
                            sql = "revoke {p} on *.* from {user}@\'{host}\'".format(p=p, user=user, host=host)
                            res = self.sqlDdl(sql)
                    except Exception as e:
                        logging.exception(str(e))
                        break
                        return 1
                if res == 0:
                    return 0
                else:
                    return 1
            else:
                if list(mix_privs)[0] == 'all':
                    sql = "revoke {p} on {db}.* from {user}@\'{host}\'".format(p=list(speprivs)[0], db=db, user=user,
                                                                            host=host)
                else:
                    sql = "revoke {p} on *.* from {user}@\'{host}\'".format(p=list(speprivs)[0], db=db, user=user,
                                                                         host=host)
                print(sql)
                res = self.sqlDdl(sql)
                if res == 0:
                    return 0
                else:
                    return 1
        if list(speprivs):
            if len(speprivs) > 1:
                for p in speprivs:
                    try:
                        if p == 'all':
                            sql = "revoke {p} on {db}.* from {user}@\'{host}\'".format(p=p, db=db, user=user,
                                                                                    host=host)
                            res = self.sqlDdl(sql)
                        else:
                            sql = "revoke {p} on *.* from {user}@\'{host}\'".format(p=p, user=user, host=host)
                            res = self.sqlDdl(sql)
                    except Exception as e:
                        logging.exception(str(e))
                        break
                        return 1
                if res == 0:
                    return 0
                else:
                    return 1
            else:
                if list(speprivs)[0] == 'all':
                    sql = "revoke {p} on {db}.* from {user}@\'{host}\'".format(p=list(speprivs)[0], db=db, user=user,
                                                                            host=host)
                else:
                    sql = "revoke {p} on *.* from {user}@\'{host}\'".format(p=list(speprivs)[0], db=db, user=user,
                                                                         host=host)
                res = self.sqlDdl(sql)
                if res == 0:
                    return 0
                else:
                    return 1
        if list(routines):
            if len(routines) > 1:
                for p in routines:
                    sql = "revoke {p} on {db}.* from {user}@\'{host}\'".format(p=p, db=db, user=user, host=host)
                    print(sql)
                    try:
                        res = self.sqlDdl(sql)
                        print(res)
                    except Exception as e:
                        logging.exception(str(e))
                        break
                        return 1
                    else:
                        if res == 0:
                            return 0

            else:
                sql = "revoke {p} on {db}.* from {user}@\'{host}\'".format(p=list(routines)[0], db=db, user=user,
                                                                        host=host)
                res = self.sqlDdl(sql)
                if res == 0:
                    return 0
                else:
                    return 1
        if table:
            if len(privs) > 1:
                for p in privs:
                    if p in list(set(set(speprivs) | set(routines))):
                        sql = "revoke {p} on *.* from {user}@\'{host}\'".format(p=p, user=user, host=host)
                    else:
                        sql = "revoke {p} on {db}.{table} from {user}@\'{host}\'".format(p=p, db=db, table=table,
                                                                                  user=user, host=host)
                    res = self.sqlDdl(sql)
                    if res != 0:
                        break
                        return 1
                return 0
            else:
                sql = "revoke {p} on {db}.{table} from {user}@\'{host}\'".format(p=privs, db=db, table=table,
                                                                              user=user, host=host)
                res = self.sqlDdl(sql)
                if res == 0:
                    return 0
                else:
                    return 1
        else:
            if len(privs) > 1:
                for p in privs:
                    if p in list(set(set(speprivs) | set(routines))):
                        sql = "revoke {p} on *.* from {user}@\'{host}\'".format(p=p, user=user, host=host)
                    else:
                        sql = "revoke {p} on {db}.* from {user}@\'{host}\'".format(p=p, db=db, user=user, host=host)
                    res = self.sqlDdl(sql)
                    if res != 0:
                        break
                        return 1
                return 0
            else:
                sql = "revoke {p} on {db}.* from {user}@\'{host}\'".format(p=privs, db=db, user=user, host=host)
                res = self.sqlDdl(sql)
                if res == 0:
                    return 0
                else:
                    return 1

    def generatePwd(self):
        pwd=random.sample(string.ascii_letters + string.digits, 10)
        return "".join(pwd)


if __name__ == "__main__":
    logging.info("test...")
    pass
    # db = DBtool(dbhost="localhost", dbport=3306, dbuser="sw", dbpwd="sw", dbname="sunway", charset='utf8mb4')
