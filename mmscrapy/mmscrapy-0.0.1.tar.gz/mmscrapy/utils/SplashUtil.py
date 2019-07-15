#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/14 23:31
# @Author  : ganliang
# @File    : SplashUtil.py
# @Desc    : TODO

import requests

from scrapy.selector import Selector


def splash():
    splash_url = 'http://192.168.0.23:8050/render.html'

    args = {'url': 'http://quotes.toscrape.com/js', 'timeout': 5, 'image': 0}

    response = requests.get(splash_url, params=args)
    print response.content

    sel = Selector(response)

    print sel

    sel.css('div.quote span.text::text').extract()


if __name__ == "__main__":
    splash()
