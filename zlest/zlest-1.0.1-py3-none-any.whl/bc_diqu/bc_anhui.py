import json

import pandas as pd
import re
from lxml import etree
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from zlest.util.etl import est_meta_large
from zlest.util.etl import est_meta, est_html, add_info

_name_ = 'anhuisheng'


def f3(driver, url):
    driver.get(url)
    locator = (By.XPATH, "//div[@class='zbd_left fl']")
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located(locator))
    before = len(driver.page_source)
    time.sleep(0.1)
    after = len(driver.page_source)
    i = 0
    while before != after:
        before = len(driver.page_source)
        time.sleep(0.1)
        after = len(driver.page_source)
        i += 1
        if i > 5: break

    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    div = soup.find('div', class_='zbd_left fl')
    return div


def f1(driver, num):
    locator = (By.XPATH, '//div[@class="iweifa_right_nr"]/p[1]/a')
    val = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator)).get_attribute('href')[-20:]
    locator = (By.XPATH, '//span[@class="page-cur"]')
    cnum = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

    if int(cnum) != int(num):
        url = re.sub('pageNum=\d+','pageNum='+str(num),driver.current_url)
        driver.get(url)

        locator = (By.XPATH, '//div[@class="iweifa_right_nr"]/p[1]/a[not(contains(@href,"%s"))]' % val)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))

    data = []
    page = driver.page_source
    body = etree.HTML(page)
    content_list = body.xpath('//div[@class="iweifa_right_nr"]/p')
    for content in content_list:
        name = content.xpath("./a/@title")[0].strip()
        ggstart_time = content.xpath("./span/text()")[0].strip()
        url = 'http://www.ahtba.org.cn' + content.xpath("./a/@href")[0].strip()
        temp = [name, ggstart_time, url]
        data.append(temp)

    df = pd.DataFrame(data=data)
    df['info'] = None
    return df


def f2(driver):
    locator = (By.XPATH, '//a[@class="page_show"]')
    txt = WebDriverWait(driver, 30).until(EC.presence_of_element_located(locator)).text

    total_page = re.findall('\/ (\d+)', txt)[0]
    driver.quit()
    return int(total_page)


data = [
    #
    ["gcjs_zhaobiao_1_gg",
     "http://www.ahtba.org.cn/Notice/AnhuiNoticeSearch?spid=714&scid=713&srcode=&sttype=&stime=36500&stitle=&sCompanyName=&isPageBarSearch=0&pageNum=1&pageSize=15",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    #
    ["gcjs_zgysjg_gg",
     "http://www.ahtba.org.cn/Notice/AnhuiNoticeSearch?spid=714&scid=596&srcode=&sttype=&stime=36500&stitle=&sCompanyName=&isPageBarSearch=0&pageNum=1&pageSize=15",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    #
    ["gcjs_zhaobiao_gg",
     "http://www.ahtba.org.cn/Notice/AnhuiNoticeSearch?spid=714&scid=597&srcode=&sttype=&stime=36500&stitle=&sCompanyName=&isPageBarSearch=0&pageNum=1&pageSize=15",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    #
    ["gcjs_zhongbiao_gg",
     "http://www.ahtba.org.cn/Notice/AnhuiNoticeSearch?spid=569&srcode=&sttype=&stime=36500&stitle=&sCompanyName=&isPageBarSearch=0&pageNum=1&pageSize=15",
     ["name", "ggstart_time", "href", "info"], f1, f2],


]


def work(conp, **arg):
    est_meta_large(conp, data=data, diqu="安徽省", **arg)
    est_html(conp, f=f3, **arg)


if __name__ == '__main__':
    # url = "http://www.ahtba.org.cn/Notice/AnhuiNoticeSearch?spid=714&scid=597&srcode=&sttype=&stime=36500&stitle=&sCompanyName=&isPageBarSearch=0&pageNum=1&pageSize=15"
    # for d in data:
    #
    #     driver = webdriver.Chrome()
    #     driver.get(d[1])
    #     df = f1(driver, 2)
    #     for ur in df.values.tolist():
    #         print(f3(driver, ur[2]))
    #     driver.get(d[1])
    #     print(f2(driver))

    #
    work(conp=["postgres", "since2015", "192.168.3.171", "zlest", "anhuisheng"])

    # for d in data:
    #     driver=webdriver.Chrome()
    #     url=d[1]
    #     print(url)
    #     driver.get(url)
    #     df = f2(driver)
    #     print(df)
    #     driver = webdriver.Chrome()
    #     driver.get(url)
    #
    #     df=f1(driver, 3)
    #     print(df.values)
    #     for f in df[2].values:
    #         d = f3(driver, f)
    #         print(d)
