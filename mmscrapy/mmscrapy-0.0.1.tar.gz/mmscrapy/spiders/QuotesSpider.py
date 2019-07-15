#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/10 23:25
# @Author  : ganliang
# @File    : QuotesSpider.py
# @Desc    : QuotesSpider
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes_spider'

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.xpath('span/small/text()').get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
