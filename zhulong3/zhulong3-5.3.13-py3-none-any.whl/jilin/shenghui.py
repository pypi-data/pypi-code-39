import json
import random
import re

import math
import requests
from bs4 import BeautifulSoup
from lmfscrap import web
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from zhulong3.util.etl import est_html, est_meta
from zhulong3.util.fake_useragent import UserAgent
import time

ua = UserAgent()
_name_ = 'jilin_shenghui'
headers = {

    'User-Agent': ua.random
}
proxy = {}


def request_res(driver, url):
    driver_info = webdriver.DesiredCapabilities.CHROME
    try:
        if "--proxy" in driver_info['goog:chromeOptions']['args'][0]:
            proxy_ip = driver_info['goog:chromeOptions']['args'][0].split('=')[1].split('://')
            proxies = {proxy_ip[0]: proxy_ip[1]}
            page = requests.get(url, proxies=proxies, headers=headers, timeout=40).text
        else:
            if proxy == {}: get_ip()
            page = requests.get(url, headers=headers, timeout=40, proxies=proxy).text
    except:
        try:
            page = requests.get(url, headers=headers, timeout=40, proxies=proxy).text
        except:
            get_ip()
            page = requests.get(url, headers=headers, timeout=40, proxies=proxy).text
    return page


def get_ip():
    global proxy
    try:
        url = """http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=1&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson="""
        r = requests.get(url)
        time.sleep(1)
        ip = r.text
        proxy = {'http': ip}
    except:
        proxy = {}
    return proxy


def f1(driver, num):
    new_url = re.sub('pageNumber=\d+?', 'pageNumber=' + str(num), driver.current_url)

    page = request_res(driver, new_url)
    body = json.loads(page)

    content_list = body.get('rows')
    data = []
    for content in content_list:
        name = content.get("projectName")
        project_code = content.get("projectNum")
        project_type = content.get("dataType").get('text')
        project_area = content.get("region").get('text')
        ggstart_time = content.get("releaseDate")
        id = content.get("id")
        url_temp = driver.current_url.split('list')[0]

        url = url_temp  + ('detail/' if 'resultInfo' not in url_temp else 'todetail/') + str(id)
        info = json.dumps({"project_code": project_code, "project_type": project_type, 'project_area': project_area}, ensure_ascii=False)

        temp = [name, ggstart_time, url, info]
        data.append(temp)

    df = pd.DataFrame(data=data)

    return df


def f2(driver):
    page = request_res(driver, driver.current_url)

    body = json.loads(page)
    total_items = body['total']
    total_page = math.ceil(int(total_items) / 100)
    driver.quit()
    return int(total_page)


def f3(driver, url):
    driver.get(url)
    locator = (By.XPATH, "//div[@class='container']")
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
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
    soup = BeautifulSoup(page, 'lxml')
    div = soup.find('div', class_='container')
    return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://www.jlsjsxxw.com:20001/web/bblistdata?sortOrder=desc&pageSize=100&pageNumber=1&_=1551778523007",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_biangeng_gg",
     "http://www.jlsjsxxw.com:20001/web/alterationShow/list?sortOrder=desc&pageSize=100&pageNumber=1&_=1562924757681",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_zhongbiaohx_gg",
     "http://www.jlsjsxxw.com:20001/web/candidateShow/list?sortOrder=desc&pageSize=100&pageNumber=1&_=1551778629317",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    ["gcjs_zhongbiao_gg",
     "http://www.jlsjsxxw.com:20001/web/resultInfo/list?sortOrder=desc&pageSize=100&pageNumber=1&projectName=&dataType=&region=&_=1551778705090",
     ["name", "ggstart_time", "href", "info"], f1, f2],

]


def work(conp, **args):
    est_meta(conp, data=data, diqu="吉林省", **args)
    est_html(conp, f=f3, **args)


if __name__ == "__main__":
    conp = ["postgres", "since2015", "192.168.3.171", "anbang2", "jilin"]
    work(conp)

    # for d in data[-1:]:
    #     driver = webdriver.Chrome()
    #     driver.get(d[1])
    #     total = f2(driver)
    #     print(total)
    #     driver = webdriver.Chrome()
    #     for i in range(1, total, 10):
    #         driver.get(d[1])
    #         print(d[1])
    #         df_list = f1(driver, i).values.tolist()
    #         print(df_list[:10])
    #         df1 = random.choice(df_list)
    #         print(str(f3(driver, df1[2]))[:100])
    #
