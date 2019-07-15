#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/13 0:06
# @Author  : ganliang
# @File    : SeleniumCookieUtil.py
# @Desc    : SeleniumCookieUtil工具类，通过Selenium模拟浏览器获取cookie
from selenium import webdriver


def get_cookie(url):
    """
    通过selenium 模拟浏览器获取cookie信息
    :return:
    """
    driver = webdriver.Chrome()
    driver.get(url)
    cj = driver.get_cookies()
    cookie = ''
    cookie_dict = {}
    for c in cj:
        cookie += c['name'] + '=' + c['value'] + ';'
        cookie_dict.setdefault(c['name'], c['value'])
    driver.quit()
    return cookie_dict
