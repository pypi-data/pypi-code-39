import pandas as pd
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from zlest.util.etl import est_html, est_meta, add_info, est_meta_large

_name_ = "ggzy_hubei_yicheng"

def f1(driver, num):
    locator = (By.XPATH, "//div[@class='tow_list']/ul/li[not(@class)][last()]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url
    locator = (By.XPATH, "//li[@class='currentpage']")
    cnum = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()

    if num != int(cnum):
        val = driver.find_element_by_xpath("//div[@class='tow_list']/ul/li[not(@class)][last()]/a").get_attribute('href')[-20:]
        url = re.sub('page=[0-9]+','page=%d'%num, url)
        driver.get(url)
        locator = (By.XPATH, "//div[@class='tow_list']/ul/li[not(@class)][last()]/a[not(contains(@href,'%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    data = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('div', class_='tow_list').ul
    lis = table.find_all('li', class_=False)
    for tr in lis:
        a = tr.find('a')
        try:
            name = a['title']
        except:
            name = a.text.strip()
        ggstart_time = tr.find('span').text.strip()
        href = 'http://www.ych.gov.cn'+a['href']
        tmp = [name, ggstart_time, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    df['info']=None
    return df



def f2(driver):
    locator = (By.XPATH, "//div[@class='tow_list']/ul/li[not(@class)][last()]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    locator = (By.XPATH, "//li[@class='nextpage'][last()]/a")
    total_page = WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator)).get_attribute('href')
    num = re.findall(r'page=(\d+)', total_page)[0]
    driver.quit()
    return int(num)



def f3(driver, url):
    driver.get(url)
    locator = (By.XPATH, "//table[contains(@width, '80%')][string-length()>200]")
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(locator))
    before = len(driver.page_source)
    time.sleep(0.5)
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
    div = soup.find('table', width='80%')
    return div


data = [
    ["gcjs_zhaobiao_gg",
     "http://www.ych.gov.cn/web/zbb/tow_all/index.aspx?c_id=658&page=1",
     ["name", "ggstart_time", "href", "info"],f1,f2],

    ####
    ["gcjs_zhongbiao_gg",
     "http://www.ych.gov.cn/web/zbb/tow_all/index.aspx?c_id=667&page=1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhongbiao_gg",
     "http://www.ych.gov.cn/web/zbb/tow_all/index.aspx?c_id=668&page=1",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ####
    ["zfcg_gaita_zhao_bian_gg",
     "http://www.ych.gov.cn/web/zbb/tow_all/index.aspx?c_id=660&page=1",
     ["name", "ggstart_time", "href", "info"], f1, f2],
]


def work(conp, **args):
    est_meta_large(conp, data=data, diqu="湖北省宜城市", **args)
    est_html(conp, f=f3, **args)


if __name__ == '__main__':
    work(conp=["postgres", "since2015", "192.168.3.171", "zlest", "ggzy_hubei_yicheng"])


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
    #     df=f1(driver, 2)
    #     print(df.values)
    #     for f in df[2].values:
    #         d = f3(driver, f)
    #         print(d)


