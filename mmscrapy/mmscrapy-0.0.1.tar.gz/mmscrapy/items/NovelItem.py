#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/10 22:49
# @Author  : ganliang
# @File    : NovelItem.py
# @Desc    : 小说
import scrapy


class NovelItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    type = scrapy.Field()
    subtype = scrapy.Field()
    status = scrapy.Field()
    intro = scrapy.Field()
    update = scrapy.Field()