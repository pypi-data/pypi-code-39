import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from zlest1.util.etl import est_html, est_meta, add_info, est_meta_large


_name_ = "csbidding_csair_com"

def f1(driver, num):
    locator = (By.XPATH, "//ul[@id='list1']/li[last()]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    locator = (By.XPATH, "//div[@class='paging-nav']")
    txt = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    cnum = re.findall(r'(\d+)/', txt)[0]
    # print(cnum)

    if num != int(cnum):
        val = driver.find_element_by_xpath("//ul[@id='list1']/li[last()]/a").get_attribute('href')[-15:]

        driver.execute_script("page({})".format(num))

        locator = (By.XPATH, "//ul[@id='list1']/li[last()]/a[not(contains(@href, '%s'))]" % val)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))

    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    ul = soup.find("ul", id='list1')
    data = []
    lis = ul.find_all('li')
    for li in lis:
        a = li.find("a")
        try:
            title = a['title'].strip()
        except:
            title = a.text.strip()
        link = a["href"]
        if 'http' in link:
            href = link
        else:
            href = 'https://csbidding.csair.com' + link
        span = li.find("em").text.strip()
        tmp = [title, span, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    df['info'] = None
    return df



def f2(driver):
    locator = (By.XPATH, "//ul[@id='list1']/li[last()]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    locator = (By.XPATH, "//div[@class='paging-nav']")
    txt = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    num = re.findall(r'/(\d+)页', txt)[0]
    driver.quit()
    return int(num)


def f3(driver, url):
    driver.get(url)
    locator = (By.XPATH, "//div[@class='main-text'][string-length()>100]")
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))

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
    div = soup.find('div', class_='main-text')
    return div


data = [
    ["qy_zhaobiao_gg",
     "https://csbidding.csair.com/cms/channel/zbgg/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    #
    ["qy_zhongbiaohx_gg",
     "https://csbidding.csair.com/cms/channel/pbgs/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["qy_zhongbiao_gg",
     "https://csbidding.csair.com/cms/channel/bidzbgg/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    # # # ####
    ["qy_gqita_gg",
     "https://csbidding.csair.com/cms/channel/qtgg/index.htm",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    # #
    ["qy_zhaobiao_fzb_gg",
     "https://csbidding.csair.com/cms/channel/cggg/index.htm",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'cglx':'非招标采购'}), f2],

    ["qy_zhaobiao_danyilaiyuan_fzb_gg",
     "https://csbidding.csair.com/cms/channel/dylycgxmgs/index.htm",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'cglx':'非招标采购','zbfs':'单一来源'}), f2],

    ["qy_zhongbiao_fzb_gg",
     "https://csbidding.csair.com/cms/channel/cgjg/index.htm",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'cglx':'非招标采购'}), f2],
    # #

    ["qy_gqita_fzb_gg",
     "https://csbidding.csair.com/cms/channel/fzbqtgg/index.htm",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'cglx':'非招标采购'}), f2],
]


def work(conp, **args):
    est_meta(conp, data=data, diqu="中国南方航空采购招标网", **args)
    est_html(conp, f=f3, **args)


if __name__ == '__main__':
    work(conp=["postgres", "since2015", "192.168.3.171", "zlest1", "csbidding_csair_com"])


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
    #     df=f1(driver, 12)
    #     print(df.values)
    #     for f in df[2].values:
    #         d = f3(driver, f)
    #         print(d)


