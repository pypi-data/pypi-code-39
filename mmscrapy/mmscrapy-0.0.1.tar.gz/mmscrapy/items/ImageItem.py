#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/10 22:49
# @Author  : ganliang
# @File    : ImageItem.py
# @Desc    : 360图片实体信息
import scrapy


class ImageItem(scrapy.Item):
    collection = table = 'images'
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    thumb = scrapy.Field()
