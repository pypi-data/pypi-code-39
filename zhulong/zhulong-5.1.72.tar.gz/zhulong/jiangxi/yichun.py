import time

import pandas as pd
import re

from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from zhulong.util.etl import est_tbs, est_meta, est_html, est_gg, add_info

# __conp=["postgres","since2015","192.168.3.171","hunan","hengyang"]


# url="http://ggzy.hengyang.gov.cn/jyxx/jsgc/zbgg_64796/index.html"
# driver=webdriver.Chrome()
# driver.minimize_window()
# driver.get(url)

_name_="yichun"

def f1(driver,num):
    locator=(By.XPATH,"//tr[@class='tdLine'][1]/td/a")
    WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    url=driver.current_url
    cnum=re.findall('-(\d+?).html',url)[0]
    if num != int(cnum):

        url=re.sub("-\d+?.html",'-%s.html'%num,url)
        val=driver.find_element_by_xpath("//tr[@class='tdLine'][1]/td/a").get_attribute('href')[-20:-5]
        driver.get(url)
        locator=(By.XPATH,"//tr[@class='tdLine'][1]/td/a[not(contains(@href,'%s'))]"%val)
        WebDriverWait(driver,10).until(EC.presence_of_element_located(locator))

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find_all('tr', class_='tdLine')
    data = []
    for tr in trs:
        tds = tr.find_all('td')
        href = tds[0].a['href']
        name = tds[0].a['title']
        ggstart_time = tds[1].get_text().strip()
        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df=pd.DataFrame(data=data)
    df["info"] = None
    return df


def f2(driver):
    locator = (By.XPATH, "//tr[@class='tdLine'][1]/td/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page = driver.find_element_by_xpath('//a[@class="clz1"][last()]').get_attribute('href')
    total = re.findall(r'-(\d+?).html', page)[0]
    total=int(total)
    return total


def f3(driver, url):
    driver.get(url)

    locator = (By.XPATH, '//td[@class="NewsContent"][string-length()>10]')

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

    soup = BeautifulSoup(page, 'html.parser')
    div = soup.find('td',class_='NewsContent').parent.parent
    return div

data=[
    #
    ["gcjs_fangjianshizheng_gqita_zhao_bian_gg","http://ggzyjyzx.yichun.gov.cn/news-list-jsgcaa-1.html",["name","ggstart_time","href",'info'],add_info(f1,{"gclx":"房建市政"}),f2],
    ["gcjs_jiaotong_gqita_zhao_bian_gg","http://ggzyjyzx.yichun.gov.cn/news-list-gljtaa-1.html",["name","ggstart_time","href",'info'],add_info(f1,{"gclx":"交通工程"}),f2],
    ["gcjs_shuili_gqita_zhao_bian_gg","http://ggzyjyzx.yichun.gov.cn/news-list-slgcaa-1.html",["name","ggstart_time","href",'info'],add_info(f1,{"gclx":"水利工程"}),f2],
    ["zfcg_gqita_zhao_bian_gg","http://ggzyjyzx.yichun.gov.cn/news-list-zfcgaa-1.html",["name","ggstart_time","href",'info'],f1,f2],

    ["gcjs_fangjianshizheng_gqita_zhonghx_liu_gg","http://ggzyjyzx.yichun.gov.cn/news-list-jsgcaaa-1.html",["name","ggstart_time","href",'info'],add_info(f1,{"gclx":"房建市政"}),f2],
    ["gcjs_jiaotong_gqita_zhonghx_liu_gg","http://ggzyjyzx.yichun.gov.cn/news-list-gljtaaa-1.html",["name","ggstart_time","href",'info'],add_info(f1,{"gclx":"交通工程"}),f2],
    ["gcjs_shuili_gqita_zhonghx_liu_gg","http://ggzyjyzx.yichun.gov.cn/news-list-slgcaaa-1.html",["name","ggstart_time","href",'info'],add_info(f1,{"gclx":"水利工程"}),f2],
    ["zfcg_gqita_zhong_liu_gg","http://ggzyjyzx.yichun.gov.cn/news-list-zfcgaaa-1.html",["name","ggstart_time","href",'info'],f1,f2],

]
def work(conp,**args):
    est_meta(conp,data=data,diqu="江西省宜春市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':

    conp=["postgres","since2015","192.168.3.171","jiangxi","yichun"]

    work(conp=conp,headless=False,num=1)