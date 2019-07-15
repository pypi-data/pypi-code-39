#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/12 10:45
# @Author  : ganliang
# @File    : FreebufLoopholeSpider.py
# @Desc    : freebuf漏洞爬虫
# https://www.freebuf.com/vuls#
# https://www.freebuf.com/?action=rc-ajax&page=1&_=1563119566592
from datetime import datetime

from scrapy import Request
from scrapy_redis import defaults
from scrapy_redis.spiders import RedisSpider
from scrapy_splash import SplashRequest


class FreebufLoopholeSpider(RedisSpider):
    """
    采用redis分布式爬虫爬取数据
    """
    name = "freebuf_loophole_spider"
    # allowed_domains = ['freebuf.com']

    # splash配置
    splash_setting = {
        "SPIDER_MIDDLEWARES": {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        "ITEM_PIPELINES": {
            'mmscrapy.pipelines.ConsolePipeline.ConsolePipeline': 300,
            'scrapy_redis.pipelines.RedisPipeline': 303,
        },
        "DOWNLOADER_MIDDLEWARES": {
            'mmscrapy.middlewares.MmscrapyDownloaderMiddleware': 543,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        "HTTPCACHE_STORAGE": "scrapy_splash.SplashAwareFSCacheStorage",
        "SPLASH_URL": "http://192.168.0.23:8050",
        "SCHEDULER": "scrapy_redis.scheduler.Scheduler",
        "DUPEFILTER_CLASS": "scrapy_redis.dupefilter.RFPDupeFilter",
        "DUPEFILTER_DEBUG": True,
        "REDIS_START_URLS_KEY": defaults.START_URLS_KEY,
        "REDIS_PARAMS": {
            'host': '192.168.0.25',
            'port': '6379',
            'db': 1,
            'password': 123456
        }
    }

    # 内容配置
    content_setting = {
        "ITEM_PIPELINES": {
            'mmscrapy.pipelines.ConsolePipeline.ConsolePipeline': 300,
            'scrapy_redis.pipelines.RedisPipeline': 303,
        },
        "DOWNLOADER_MIDDLEWARES": {
            'mmscrapy.middlewares.MmscrapyDownloaderMiddleware': 543,
        },
        "SCHEDULER": "scrapy_redis.scheduler.Scheduler",
        "DUPEFILTER_CLASS": "scrapy_redis.dupefilter.RFPDupeFilter",
        "DUPEFILTER_DEBUG": True,
        "REDIS_START_URLS_KEY": defaults.START_URLS_KEY,
        "REDIS_PARAMS": {
            'host': '192.168.0.25',
            'port': '6379',
            'db': 1,
            'password': 123456
        }
    }
    custom_settings = content_setting

    def __init__(self, *args, **kwargs):
        # typeId  应用漏洞列表 2
        self.type = kwargs.get("type", "content")
        # if type == "content":
        #     custom_settings = self.content_setting
        # elif type == "splash":
        #     custom_settings = self.splash_setting

    def make_requests_from_url(self, url):
        if self.type == "content":
            return Request(url, dont_filter=False, callback=self.parse_content)
        elif type == "splash":
            return SplashRequest(url=url, callback=self.parse, args={'timeout': 90, 'wait': 0.5})

    def parse(self, response):
        """
        解析页面数据
        :param response:
        :return:
        """
        # 消息详情
        infos = response.css("#timeline .news-info dl dt a[href]::attr(href)").getall()
        self.logger.info(infos)
        for info in infos:
            yield SplashRequest(url=response.urljoin(info), callback=self.parse_news,
                                args={'timeout': 90, 'wait': 0.5})

        # 分页
        pages = response.css("#pagination a[href]::attr(href)").getall()
        self.logger.info(pages)
        for page in pages:
            yield SplashRequest(url=response.urljoin(page), callback=self.parse, args={'timeout': 90, 'wait': 0.5})

    def parse_content(self, response):
        """
        解析接口返回的数据
        :param response:
        :return:
        """
        url = str(response.request.url)
        body = response.body.replace("items", "\"items\"").replace("navi", "\"navi\"") \
            .replace("more", "\"more\"").replace("page", "\"page\"")
        self.logger.info(body)
        data = eval(body)
        items = data.get("items", [])
        for item in items:
            yield response.follow(item.get("postUrl"), dont_filter=False, callback=self.parse_news)

        navi = data.get("navi", {})
        page = int(navi.get("page", "0")) + 1
        page_index, base_url = url.rfind("&page="), url
        if page_index > 0:
            base_url = url[:page_index - len("&page=")]
        page_url = base_url + "&page={0}".format(page)
        yield response.follow(page_url, dont_filter=False, callback=self.parse_content)

    def parse_news(self, response):
        articlecontent = response.css("#getWidth .articlecontent")

        article_result = {}
        article_result.setdefault("url", response.request.url)
        article_result.setdefault("title", articlecontent.css(".title h2::text").extract_first())
        article_result.setdefault("create_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        author = articlecontent.css(".title property .name a::text").extract_first()
        article_result.setdefault("author", author)

        authorUrl = articlecontent.css(".title property .name a::attr(href)").extract_first()
        article_result.setdefault("authorUrl", authorUrl)

        pubdate = articlecontent.css(".title property .time::text").extract_first()
        article_result.setdefault("pubdate", pubdate)

        look = articlecontent.css(".title property .look strong::text").getall()
        article_result.setdefault("look", look)

        tags = articlecontent.css(".title property .tags a::attr(href)").getall()
        article_result.setdefault("tags", tags)

        content = articlecontent.css("#contenttxt").extract_first()
        article_result.setdefault("content", content)

        yield article_result
