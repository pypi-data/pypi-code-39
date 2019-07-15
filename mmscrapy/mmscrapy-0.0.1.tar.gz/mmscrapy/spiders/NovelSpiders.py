#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/10 17:02
# @Author  : ganliang
# @File    : NovelSpiders.py
# @Desc    : 小说爬虫器

from scrapy import Spider, Request

from mmscrapy.items.NovelItem import NovelItem


class NovelSpiders(Spider):
    base_url = "https://www.qidian.com"
    name = "novel_spider"
    custom_settings = {
        "ITEM_PIPELINES": {
            'mmscrapy.pipelines.ConsolePipeline.ConsolePipeline': 300
        }
    }

    def __init__(self, *args, **kwargs):
        super(NovelSpiders, self).__init__(*args, **kwargs)
        category = kwargs.get("category", "finish")

        self.start_urls = ['{0}/{1}'.format(self.base_url, category)]

    def start_requests(self):
        for start_url in self.start_urls:
            yield Request(start_url, dont_filter=False)

    def parse(self, response):
        item = NovelItem()
        novels = response.css('.book-mid-info')
        for novel in novels:
            item["name"] = novel.css("h4 a[href]::text").extract_first().strip()
            item["url"] = response.urljoin(novel.css("h4 a[href]::attr(href)").extract_first().strip())
            item["author"] = novel.css(".author .name::text").extract_first().strip()
            item["type"] = novel.css(".author a[href]::text").getall()[1].strip()
            item["subtype"] = novel.css(".author .go-sub-type::text").extract_first().strip()
            item["status"] = novel.css(".author span::text").extract_first().strip()
            item["intro"] = novel.css(".intro::text").extract_first().strip()
            # item["update"] = novel.css(".update span::text").extract_first().strip()
            yield item

        next_urls = response.css(".lbf-pagination-item .lbf-pagination-page::attr(href)").getall()
        if next_urls and len(next_urls) > 0:
            for next_url in next_urls:
                # next_page = response.urljoin(next_url)
                # print (next_page)
                # yield Request(next_page, callback=self.parse, dont_filter=False)
                yield response.follow(next_url, callback=self.parse, dont_filter=False)
