import pandas as pd
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from zlest1.util.etl import est_html, est_meta, add_info, est_meta_large


_name_ = "eps_sdic_com_cn"

def f1(driver, num):
    locator = (By.XPATH, "//div[@class='lb-link']/ul[1]/li[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    url = driver.current_url

    locator = (By.XPATH, "//div[@class='pag-txt']/em[1]")
    cnum = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()

    if num != int(cnum):
        val = driver.find_element_by_xpath("//div[@class='lb-link']/ul[1]/li[1]/a").get_attribute('href')[-15:]
        if "index_" not in url:
            s = "index_%d" % (num) if num > 1 else "index"
            url = re.sub("index", s, url)
        elif num == 1:
            url = re.sub("index_[0-9]*", "index", url)
        else:
            s = "index_%d" % (num) if num > 1 else "index"
            url = re.sub("index_[0-9]*", s, url)
        driver.get(url)

        locator = (By.XPATH, "//div[@class='lb-link']/ul[1]/li[1]/a[not(contains(@href, '%s'))]" % val)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(locator))

    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    div = soup.find("div", class_='lb-link')
    uls = div.find_all('ul')
    data = []
    for ul in uls:
        lis = ul.find_all('li')
        for li in lis:
            a = li.find("a")
            try:
                title = a['title'].strip()
            except:
                title = li.find('span', class_='bidLink').text.strip()
            link = a["href"]
            if 'http' in link:
                href = link
            else:
                href = 'http://eps.sdic.com.cn' + link
            span = li.find("span", class_='bidDate').text.strip()
            tmp = [title, span, href]
            data.append(tmp)
    df = pd.DataFrame(data=data)
    df['info'] = None
    return df



def f2(driver):
    locator = (By.XPATH, "//div[@class='lb-link']/ul[1]/li[1]/a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    locator = (By.XPATH, "//div[@class='pag-txt']/em[last()]")
    num = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
    driver.quit()
    return int(num)


def f3(driver, url):
    driver.get(url)
    locator = (By.XPATH, "//table[@class='StdInputTable'][string-length()>60] | //div[@class='mbox lpInfo'][string-length()>60]")
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
    div = soup.find('table', class_='StdInputTable')
    if div == None:
        div = soup.find('div', class_='mbox lpInfo')
    return div


data = [
    ["qy_zhaobiao_huowu_gg",
     "http://eps.sdic.com.cn/gghw/index.jhtml",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'lx':'货物'}), f2],
    #
    ["qy_zhaobiao_gongcheng_gg",
     "http://eps.sdic.com.cn/gggc/index.jhtml",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'lx':'工程'}), f2],

    ["qy_zhaobiao_fuwu_gg",
     "http://eps.sdic.com.cn/ggjg/index.jhtml",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'lx':'服务'}), f2],
    # # # ####
    ["qy_biangeng_huowu_gg",
     "http://eps.sdic.com.cn/bghw/index.jhtml",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'lx':'货物'}), f2],
    #
    ["qy_biangeng_gongcheng_gg",
     "http://eps.sdic.com.cn/bggc/index.jhtml",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'lx':'工程'}), f2],

    ["qy_biangeng_fuwu_gg",
     "http://eps.sdic.com.cn/bgfw/index.jhtml",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'lx':'服务'}), f2],
    # ####
    ["qy_zhongbiaohx_huowu_gg",
     "http://eps.sdic.com.cn/zbhw/index.jhtml",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'lx':'货物'}), f2],
    #
    ["qy_zhongbiaohx_gongcheng_gg",
     "http://eps.sdic.com.cn/zbgc/index.jhtml",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'lx':'工程'}), f2],

    ["qy_zhongbiaohx_fuwu_gg",
     "http://eps.sdic.com.cn/zbfw/index.jhtml",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'lx':'服务'}), f2],
    # # # ####
    ["qy_zhaobiao_lx1_huowu_gg",
     "http://eps.sdic.com.cn/cghw/index.jhtml",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'lx':'货物'}), f2],

    ["qy_zhaobiao_lx1_gongcheng_gg",
     "http://eps.sdic.com.cn/cggc/index.jhtml",
     ["name", "ggstart_time", "href", "info"], add_info(f1, {'lx': '工程'}), f2],
    #
    ["qy_zhaobiao_lx1_fuwu_gg",
     "http://eps.sdic.com.cn/cgfw/index.jhtml",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'lx':'服务'}), f2],
    ###
    ["qy_zhongbiao_huowu_gg",
     "http://eps.sdic.com.cn/kzjhw/index.jhtml",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'lx':'货物'}), f2],

    ["qy_zhongbiao_gongcheng_gg",
     "http://eps.sdic.com.cn/kzjgc/index.jhtml",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'lx':'工程'}), f2],
    ####
    ["qy_zhongbiao_fuwu_gg",
     "http://eps.sdic.com.cn/kzjfw/index.jhtml",
     ["name", "ggstart_time", "href", "info"], add_info(f1,{'lx':'服务'}), f2],
]


def work(conp, **args):
    est_meta(conp, data=data, diqu="国家开发投资公司", **args)
    est_html(conp, f=f3, **args)


if __name__ == '__main__':
    work(conp=["postgres", "since2015", "192.168.3.171", "zlest1", "eps_sdic_com_cn"])


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


