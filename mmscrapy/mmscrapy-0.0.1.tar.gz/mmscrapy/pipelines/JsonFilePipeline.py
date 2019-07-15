#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/11 0:35
# @Author  : ganliang
# @File    : JsonFilePipeline.py
# @Desc    : json文件存储
import json
import os
from datetime import datetime


class JsonFilePipeline(object):

    def __init__(self, basedir, linecount):
        self.basedir = basedir
        self.linecount = linecount
        self.counter = 0

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            basedir=crawler.settings.get('JSONFILE_BASEDIR', "/tmp"),
            linecount=int(crawler.settings.get('JSONFILE_LINECOUNT', 10000))
        )

    def open_spider(self, spider):
        if not os.path.exists(self.basedir):
            os.makedirs(self.basedir)

        self.file = open(
            os.path.normpath(os.path.join(self.basedir, '{0}.json'.format(datetime.now().strftime("%Y%m%d%H%M%S")))),
            'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        # 切换文件
        if self.counter >= self.linecount:
            self.counter = 0
            self.file.close()
            self.file = open(
                os.path.normpath(
                    os.path.join(self.basedir, '{0}.json'.format(datetime.now().strftime("%Y%m%d%H%M%S")))),
                'w')
        # 将数据保存到文件中
        line = json.dumps(dict(item), ensure_ascii=False, encoding="UTF-8") + "\n"
        self.file.write(line)

        self.counter += 1
        return item
