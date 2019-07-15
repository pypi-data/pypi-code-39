#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/13 9:11
# @Author  : ganliang
# @File    : FreeProxySpider.py
# @Desc    : 西刺免费代理爬虫
from datetime import datetime

from scrapy import Spider, Request


class FreeProxySpider(Spider):
    name = "xicidaili_proxy_spider"

    custom_settings = {
        "ITEM_PIPELINES": {
            'mmscrapy.pipelines.ConsolePipeline.ConsolePipeline': 300,
            'mmscrapy.pipelines.JsonFilePipeline.JsonFilePipeline': 310
        },
        "DOWNLOADER_MIDDLEWARES": {
            'mmscrapy.middlewares.MmscrapyDownloaderMiddleware': 543,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
            'mmscrapy.middleware.ProxyMiddleware.ProxyMiddleware': 541,
        }
    }

    def __init__(self, *args, **kwargs):
        self.proxyType = kwargs.get("type", "nn,nn")
        self.base_url = "https://www.xicidaili.com/"

        self.base_urls = []
        for sub_proxy_type in self.proxyType.split(","):
            self.base_urls.append("{0}{1}".format(self.base_url, sub_proxy_type))

    def start_requests(self):
        for base_url in self.base_urls:
            yield Request(base_url, callback=self.parse, dont_filter=False)

    def parse(self, response):

        # 解析页面数据
        ip_trs = response.css("#ip_list tr")
        for ip_tr in ip_trs:
            proxy_dict = {}
            tds = ip_tr.css("td")
            for index, td in enumerate(tds):
                # 国家
                if index == 0:
                    proxy_dict.setdefault("country", td.css("img::attr(alt)").extract_first())
                # ip
                elif index == 1:
                    proxy_dict.setdefault("ip", td.css("td::text").extract_first())
                # 端口
                elif index == 2:
                    proxy_dict.setdefault("port", td.css("td::text").extract_first())
                # 服务器地址信息
                elif index == 3:
                    proxy_dict.setdefault("address", td.css("a::text").extract_first())
                # 是否隐匿
                elif index == 4:
                    proxy_dict.setdefault("hidden", td.css("td::text").extract_first())
                # http类型
                elif index == 5:
                    proxy_dict.setdefault("type", td.css("td::text").extract_first())
                # 速度
                elif index == 6:
                    proxy_dict.setdefault("speed", td.css(".bar::attr(title)").extract_first())
                # 连接时间
                elif index == 7:
                    proxy_dict.setdefault("connect", td.css(".bar::attr(title)").extract_first())
                # 存活时间
                elif index == 8:
                    proxy_dict.setdefault("expire", td.css("td::text").extract_first())
                # 验证时间
                elif index == 9:
                    proxy_dict.setdefault("verify", td.css("td::text").extract_first())

            if proxy_dict:
                proxy_dict.setdefault("create_time", datetime.now().strftime("%Y%m%d%H%M%S"))
                yield proxy_dict

        # 分页页面跳转
        paginations = response.css(".pagination a[href]::attr(href)").getall()
        for pagination in paginations:
            yield response.follow(pagination, callback=self.parse, dont_filter=False)
