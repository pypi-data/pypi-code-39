import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from zlest.util.etl import est_html, est_meta, add_info, est_meta_large


_name_ = "ggzy_beijing_haidian"

def f1(driver, num):
    locator = (By.XPATH, "//ul[@class='article clearfix']/li[last()]//a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url

    locator = (By.XPATH, "//ul[@class='pages-list']/li[1]/a")
    txt = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    cnum = re.findall(r'(\d+)/', txt)[0]

    if num != int(cnum):
        val = driver.find_element_by_xpath("//ul[@class='article clearfix']/li[last()]//a").get_attribute('href')[-15:]

        driver.execute_script("location.href=encodeURI('index_%d.jhtml');" % num)

        locator = (By.XPATH, "//ul[@class='article clearfix']/li[last()]//a[not(contains(@href, '%s'))]" % val)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))

    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    ul = soup.find("ul", class_='article clearfix')
    data = []
    lis = ul.find_all('li', class_=re.compile('zt'))
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
            href = 'http://www.bjhd.gov.cn' + link
        span = li.find("p", class_='release-time').text.strip()
        tmp = [title, span, href]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    df['info'] = None
    return df



def f2(driver):
    locator = (By.XPATH, "//ul[@class='article clearfix']/li[last()]//a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    locator = (By.XPATH, "//ul[@class='pages-list']/li[1]/a")
    txt = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    num = re.findall(r'/(\d+)', txt)[0]
    driver.quit()
    return int(num)


def f3(driver, url):
    driver.get(url)
    locator = (By.XPATH, "//div[@class='content2'][string-length()>100]")
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
    div = soup.find('div', class_='content2')
    return div


data = [
    ["zfcg_yucai_gg",
     "http://www.bjhd.gov.cn/ggzyjy/zfcgBqgs/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["zfcg_zhaobiao_gg",
     "http://www.bjhd.gov.cn/ggzyjy/zfcgZbgg/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1,f2],

    ["zfcg_biangeng_gg",
     "http://www.bjhd.gov.cn/ggzyjy/zfcgXxgzgs/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    # # # ####
    ["zfcg_zhongbiao_gg",
     "http://www.bjhd.gov.cn/ggzyjy/zfcgCjgs/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    # #
    ["zfcg_liubiao_gg",
     "http://www.bjhd.gov.cn/ggzyjy/zfcgFbgs/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhaobiao_gg",
     "http://www.bjhd.gov.cn/ggzyjy/gcjsFjgc/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],
    # # ####
    ["gcjs_zhongbiaohx_gg",
     "http://www.bjhd.gov.cn/ggzyjy/gcjsSzgc/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["gcjs_zhongbiao_gg",
     "http://www.bjhd.gov.cn/ggzyjy/gcjsSwgc/index.jhtml",
     ["name", "ggstart_time", "href", "info"], f1, f2],

]


def work(conp, **args):
    est_meta(conp, data=data, diqu="北京市海淀区", **args)
    est_html(conp, f=f3, **args)


if __name__ == '__main__':
    work(conp=["postgres", "since2015", "192.168.3.171", "zlest", "ggzy_beijing_haidian"])


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
    #     df=f1(driver, 4)
    #     print(df.values)
    #     for f in df[2].values:
    #         d = f3(driver, f)
    #         print(d)


