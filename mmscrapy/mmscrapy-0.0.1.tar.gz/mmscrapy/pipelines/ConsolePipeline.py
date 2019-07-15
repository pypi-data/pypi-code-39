#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/10 22:47
# @Author  : ganliang
# @File    : ConsolePipeline.py
# @Desc    : 控制台打印输出
import json
import logging


class ConsolePipeline(object):
    ids = set()
    logger = logging.getLogger(__name__)

    def process_item(self, item, spider):
        itemdict = dict(item.iteritems())
        self.ids.add(itemdict.get("url"))
        self.logger.info(json.dumps(itemdict, ensure_ascii=False))
        return item
