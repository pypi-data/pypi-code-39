#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/10 22:23
# @Author  : ganliang
# @File    : ImageSpiders.py
# @Desc    : 360图片下载
import json
from urllib import urlencode

from scrapy import Spider, Request

from mmscrapy.items.ImageItem import ImageItem


class BasicImageSpiders(Spider):
    name = "basic_image_spider"
    custom_settings = {"IMAGES_STORE": "D:/data/mmscrapy/360images",
                       "ITEM_PIPELINES": {
                           'mmscrapy.pipelines.ConsolePipeline.ConsolePipeline': 300,
                           'mmscrapy.pipelines.ImagePipeline.ImagePipeline': 301
                       }}
    MAX_PAGE = 1000

    def start_requests(self):
        data = {'ch': 'photography', 'listtype': 'new'}
        base_url = 'https://image.so.com/zj?'
        for page in range(1, self.MAX_PAGE + 1):
            data['sn'] = page * 30
            params = urlencode(data)
            url = base_url + params
            yield Request(url, self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        if result and len(result) > 0:
            for image in result.get('list'):
                item = ImageItem()
                item['id'] = image.get('imageid')
                item['url'] = image.get('qhimg_url')
                item['title'] = image.get('group_title')
                item['thumb'] = image.get('qhimg_thumb_url')
                yield item


class ImageSpiders(Spider):
    name = "image_spider"
    custom_settings = {"IMAGES_STORE": "D:/data/mmscrapy/360images",
                       "ITEM_PIPELINES": {
                           'mmscrapy.pipelines.ConsolePipeline.ConsolePipeline': 300,
                           'mmscrapy.pipelines.ImagePipeline.ImagePipeline': 301
                       }}

    def start_requests(self):
        base_url = 'https://image.so.com/z?ch=beauty'
        yield Request(base_url, self.parse, dont_filter=False)

    def parse(self, response):
        imgs = response.css('li img::attr("src")').getall()
        print (imgs)
        for img in imgs:
            item = ImageItem()
            item['url'] = response.urljoin(img)
            if str(item["url"]).find("ps.ssl.qhmsg.com") > -1:
                yield item

        # 继续爬去页面
        srcs = response.css('li a[href]::attr("href")').getall()
        print (srcs)
        for src in srcs:
            yield response.follow(src, callback=self.parse, dont_filter=False)

    def parse_album(self, response):
        imgs = response.css('li img::attr(src)').getall()
        if not imgs:
            return

        for img in imgs:
            item = ImageItem()
            item['url'] = response.urljoin(img)
            yield item
