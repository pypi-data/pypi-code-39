#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: mongo.py
Desc: mongodb操作类
Author:yanjingang(yanjingang@mail.com)
Date: 2019/2/21 23:34
"""
import logging
import copy
import time
import pymongo
from bson.objectid import ObjectId
from dp import utils,constants


class MongoDB():
    """
    mongodb操作基础类
    """

    def __init__(self, dbconf):
        """
        初始化链接

        :param dbconf: 数据库链接配置{'user':'xxx','passwd':'xxx','hostname':'xxx','port':'xx','db':'xx','name':'collection_name'}
        :return:
        """
        self.uri = None
        self.con = None
        self.db = None
        self.collection = None

        if type(dbconf) is not dict or 'db' not in dbconf or 'hostname' not in dbconf:
            logging.error("Mongo __init__ failed! dbconf is invalid!")
            exit(-1)
        self.dbconf = dbconf
        # uri
        if dbconf['hostname'].startswith("mongodb://"):
            self.uri = dbconf['hostname']
        else:
            self.uri = 'mongodb://' + dbconf['user'] + ':' + dbconf['passwd'] + '@' + dbconf[
                'hostname'] + ':' + dbconf['port'] + '/' + dbconf['db']
        print(self.uri)

        self.connect()

    '''
    def __del__(self):
        logging.info('__disconnect_mongo__')
        self.disconnect()
    '''

    def connect(self):
        """
        连接mongodb

        :return:
        """
        logging.info('__connect_mongo__')
        try:
            if self.con is None:
                self.con = pymongo.MongoClient(self.uri)
                self.db = eval('self.con.' + self.dbconf['db'])
                if 'name' in self.dbconf:
                    self.collection = self.db[self.dbconf['name']]
        except:
            logging.error('connect mongo fail! [' + utils.get_trace() + ']')

    def disconnect(self):
        """
        断开mongodb连接

        :return:
        """
        try:
            self.con.close()
        except:
            pass

    def get_collection(self, name):
        """
        返回表collection对象

        :param name: 集合名称（即表名）
        :return: 集合对象
        """
        if name is not None:
            return self.db[name]
        else:
            return self.collection

    def count(self, cond=None, name=None):
        """
        查询mongo符合查询条件的记录数

        :param cond: 查询条件
        :param name: 表名
        :return: 符合条件的记录数
        """
        logging.info('__count_mongo__[' + str(cond) + ']')
        try:
            if self.con is None:
                self.connect()

            collection = self.get_collection(name)
            if cond is None or len(cond) == 0:
                count = collection.count()
            else:
                count = collection.count(cond)
            return True, '', count
        except:
            msg = 'get count fail[' + str(cond) + '][' + utils.get_trace() + ']'
            logging.error(msg)
            return False, msg, 0

    def insert(self, data, name=None):
        """
        将数据插入到mongo中

        :param name: 表名
        :param cond: 修改条件
        :param data: 数据
        :return:
        """
        logging.info('__insert_mongo__')
        # return self.update(cond, data, upsert=True, isset=True, name=name)
        # get data
        try:
            if self.con is None:
                self.connect()

            collection = self.get_collection(name)
            mret = collection.insert_one(data)
            if mret.inserted_id:
                return True,'', mret.inserted_id
            else:
                return False, str(mret), ''
        except:
            msg = 'insert mongo fail![' + utils.get_trace() + ']'
            logging.error(msg)
            return False, msg, ''

    def update(self, cond, data, name=None, isset=True, upsert=False, multi=False, attempts=1):
        """
        将数据更新到mongo中，如果不存在则插入

        :param cond: 修改条件
        :param data: 需要插入或修改的数据
        :param isset: 是否使用set
        :param upsert: 不存在时是否插入
        :param name: 表名
        :param multi: 是否修改多个
        :param attempts: 尝试更新的次数，默认只更新一次, 最多执行三次
        :return:
        """
        logging.info('__update_mongo__')
        if not attempts or not str(attempts).isdigit() or int(attempts) <= 0:
            attempts = 1
        elif int(attempts) > 3:
            attempts = 3
        else:
            attempts = int(attempts)
        # update data
        try:
            if self.con is None:
                self.connect()

            collection = self.get_collection(name)
            mret = ''
            while attempts > 0:
                if isset is True:
                    mret = collection.update(cond, {'$set': data}, upsert, multi=multi)
                else:
                    mret = collection.update(cond, data, upsert, multi=multi)
                if 'ok' in mret and mret['ok'] == 1:
                    return True, str(mret)
                else:
                    attempts -= 1
            return False, str(mret)
        except:
            msg = 'update mongo fail![' + utils.get_trace() + ']'
            logging.error(msg)
            return False, msg

    def find_one(self, cond={}, fields='', name=None):
        """
        查询，返回单条数据

        :param cond: 查询条件
        :param fields: 查询字段，多个字段之间,分隔
        :param name: 数据表名
        :return:
        """
        logging.info('__findOne_mongo__[' + str(cond) + '][' + str(fields) + ']')
        response = {}

        try:
            if self.con is None:
                self.connect()

            collection = self.get_collection(name)

            # find
            fields = fields.strip().split(',')
            if len(fields) == 0:
                response = collection.find_one(cond)
            else:
                field_need = {'_id': 0}
                for field in fields:
                    if field.strip() != '':
                        field_need[field.strip()] = 1
                response = collection.find_one(cond, field_need)
            # 返回dict
            return True, '', response
        except:
            msg = 'findOne mongo failed![' + utils.get_trace() + ']'
            logging.error(msg)
            return False, msg, response

    def find(self, cond={}, fields='', sort=None, limit=0, name=None, skip=0,
             no_cursor_timeout=False, batch_size=None):
        """
        查询

        :param cond: 查询条件
        :param fields: 查询字段，多个字段之间,分隔
        :param sort: 排序条件，按哪个字段进行排序
        :param limit: 限制返回条数
        :param name: 数据表名
        :param skip: 跳过的记录数
        :param no_cursor_timeout: 默认为False,会在10分钟之后关闭，如果10分钟处理不完，可以设置为True,但是需自己调用close()显示关闭游标
        :param batch_size: 默认为None，表示使用默认的返回条数/容量限制，用户可以设置条数，比如30，对于过大值，pymongo内部会使用默认配置
        :return:
        """
        logging.info('__find_mongo__[' + str(cond) + '][' + str(fields) + '][' +
                     str(sort) + '][' + str(limit) + ']')
        try:
            if self.con is None:
                self.connect()

            collection = self.get_collection(name)

            # find
            fields = fields.strip().split(',')
            if len(fields) == 0:
                cursor = collection.find(cond, no_cursor_timeout=no_cursor_timeout)
            else:
                field_need = {'_id': 0}
                for field in fields:
                    if field.strip() != '':
                        field_need[field.strip()] = 1
                cursor = collection.find(cond, field_need, no_cursor_timeout=no_cursor_timeout)
            # 排序条件
            if sort is not None:
                cursor = cursor.sort(sort)
            # 跳过的记录条数
            if skip > 0:
                cursor = cursor.skip(skip)
            # 限制条数
            if limit > 0:
                cursor = cursor.limit(limit)
            # 返回游标
            if batch_size and str(batch_size).isdigit():
                return True, '', cursor.batch_size(int(batch_size))
            return True, '', cursor
        except:
            msg = 'find mongo failed![' + utils.get_trace() + ']'
            logging.error(msg)
            return False, msg, []

    def aggregate(self, pipeline, name=None):
        """
        mongo中聚合操作

        :param pipeline: 聚合管道操作列表
        :param name: 数据库表名
        :return:

        """
        logging.info('__aggregate_mongo__[' + str(pipeline) + ']')
        response = []
        try:
            if self.con is None:
                self.connect()
            collection = self.get_collection(name)
            cursor = collection.aggregate(pipeline)
            for data in cursor:
                response.append(data)
            return True, '', response
        except:
            logging.error(
                'aggregate data fail![' + utils.get_trace() + ']')
            return False, 'aggregate data fail!', []

    def remove(self, cond, name=None):
        """
        删除符合某条件的数据

        :param name: 表名
        :param cond: 条件
        :return:
        """
        logging.info('__remove_mongo__[' + str(cond) + ']')
        try:
            if self.con is None:
                self.connect()
            collection = self.get_collection(name)
            collection.remove(cond)
            return True, ''
        except:
            logging.error('remove data fail[' + str(cond) + '][' +
                          utils.get_trace() + ']')
            return False, 'remove data fail!'



if __name__ == '__main__':
    """测试"""
    # log
    utils.init_logging(log_file='mongo', log_path=constants.APP_PATH)
    
    # mongodb
    db = MongoDB({'user':'test_admin','passwd':'abc123','hostname':'127.0.0.1','port':'27017','db':'test','name':'test'})
    # insert
    ret, msg, id = db.insert({'val':'test','time':time.time()})
    print('db.insert: {},{},{}'.format(ret, msg, id))
    # update
    ret, msg = db.update({'_id': id}, {'abc':'xyz'})
    print('db.update: {},{}'.format(ret, msg))
    # find_one
    ret, msg, res = db.find_one({'_id': id}) #ObjectId("5d306128844771e17d9f8af5")} )
    print('db.find_one: {},{},{}'.format(ret,msg,res))
    # count
    ret = db.count({})
    print('db.count: {}'.format(ret))
    # find
    ret, msg, res = db.find({'time':{'$exists':True}},fields='_id,val,time')
    print('db.find: {},{}'.format(ret,msg))
    for row in res:
        print(row)
    # remove
    ret = db.remove({})
    print('db.remove: {}'.format(ret))
