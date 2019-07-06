
import pandas as pd  
import re 

from selenium import webdriver 
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write,db_query,db_command
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

from zhulong.util.etl import est_meta,est_html,add_info
import time 
_name_="yichang"


def f1(driver,num):
    locator=(By.CLASS_NAME,"categorypagingcontent")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    #if driver.find_element_by_id("ctl00_ContentPlaceHolder1_DDLPageSize").text!=""
    try:
        cnum = int(driver.find_element_by_xpath("//li[contains(@class,'ewb-page-num')]").text.split("/")[0])
    except:
        cnum=1
    if num!=cnum:
        val=driver.find_element_by_xpath("//div[@class='categorypagingcontent']/ul/li[@class='list-item'][1]/a").text

        locator=(By.ID,"GoToPagingNo")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        input=driver.find_element_by_id("GoToPagingNo")
        input.clear()
        input.send_keys(num)
        input.send_keys(Keys.ENTER)
        driver.find_element_by_class_name("wb-page-go").click()
        #driver.execute_script("GoToPaging();")
        locator=(By.XPATH,"//div[@class='categorypagingcontent']/ul/li[@class='list-item'][1]/a[string()!='%s']"%val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    page=driver.page_source

    soup=BeautifulSoup(page,"html.parser")

    div=soup.find("div",class_="categorypagingcontent")

    ul=div.find("ul",class_="ewb-info-items")

    lis=ul.find_all("li",class_=re.compile('clearfix'))
    data=[]
    for li in lis:
        a=li.find("a")
        span=li.find("span", class_='ewb-date')
        href="http://ggzyjy.yichang.gov.cn"+a["href"]
        try:
            title=a["title"]
        except:
            title = a.text.strip()
        ggstart_time=span.text.strip()
        tmp=[title,ggstart_time,href]
        data.append(tmp)
    df=pd.DataFrame(data)
    df["info"]=None
    return df

def f2(driver):
    locator=(By.CLASS_NAME,"categorypagingcontent")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))

    locator=(By.XPATH,"//li[contains(@class,'ewb-page-num')]")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    cnum=int(driver.find_element_by_xpath("//li[contains(@class,'ewb-page-num')]").text.split("/")[1])
    total=int(cnum)
    driver.quit()
    return total


def f3(driver,url):


    driver.get(url)

    locator=(By.XPATH,"//div[@class='detail-main'][string-length()>60]")

    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located(locator))

    before=len(driver.page_source)
    time.sleep(0.1)
    after=len(driver.page_source)
    i=0
    while before!=after:
        before=len(driver.page_source)
        time.sleep(0.1)
        after=len(driver.page_source)
        i+=1
        if i>5:break

    page=driver.page_source
    soup=BeautifulSoup(page,'html.parser')
    div=soup.find('div',class_='detail-main')
    #div=div.find_all('div',class_='ewb-article')[0]
    return div





data=[

    ["gcjs_shigong_zhaobiao_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003001/003001001/003001001001/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"施工"}),f2 ],

    ["gcjs_jianli_zhaobiao_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003001/003001001/003001001002/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"监理"}),f2 ],

    ["gcjs_kancha_zhaobiao_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003001/003001001/003001001003/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"勘察"}),f2 ],

    ["gcjs_gcqita_zhaobiao_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003001/003001001/003001001004/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"其它"}),f2 ],



    ["gcjs_shigong_biangeng_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003001/003001002/003001002001/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"施工"}),f2 ],

    ["gcjs_jianli_biangeng_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003001/003001002/003001002002/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"监理"}),f2 ],

    ["gcjs_kancha_biangeng_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003001/003001002/003001002003/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"勘察"}),f2 ],


    ["gcjs_gcqita_biangeng_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003001/003001002/003001002004/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"其它"}),f2 ],


    ["gcjs_shigong_zhongbiaohx_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003001/003001003/003001003001/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"施工"}),f2 ],

    ["gcjs_jianli_zhongbiaohx_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003001/003001003/003001003002/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"监理"}),f2 ],

    ["gcjs_kancha_zhongbiaohx_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003001/003001003/003001003003/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"勘察"}),f2 ],


    ["gcjs_gcqita_zhongbiaohx_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003001/003001003/003001003004/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"其它"}),f2 ],


    ["gcjs_shigong_zhongbiao_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003001/003001004/003001004001/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"施工"}),f2 ],

    ["gcjs_jianli_zhongbiao_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003001/003001004/003001004002/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"监理"}),f2 ],

    ["gcjs_kancha_zhongbiao_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003001/003001004/003001004003/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"勘察"}),f2 ],


    ["gcjs_gcqita_zhongbiao_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003001/003001004/003001004004/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"其它"}),f2 ],


    ["zfcg_huowu_zhaobiao_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003002/003002001/003002001001/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"货物"}),f2 ],
    ["zfcg_fuwu_zhaobiao_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003002/003002001/003002001002/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"服务"}),f2 ],

    ["zfcg_gongcheng_zhaobiao_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003002/003002001/003002001003/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"工程"}),f2 ],



    ["zfcg_huowu_biangeng_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003002/003002002/003002002001/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"货物"}),f2 ],

    ["zfcg_fuwu_biangeng_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003002/003002002/003002002002/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"服务"}),f2 ],




    ["zfcg_huowu_zhongbiao_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003002/003002003/003002003001/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"货物"}),f2 ],

    ["zfcg_fuwu_zhongbiao_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003002/003002003/003002003002/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"f服务"}),f2 ],


    ["zfcg_gongcheng_zhongbiao_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003002/003002003/003002003003/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"工程"}),f2 ],


    ["zfcg_huowu_liubiao_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003002/003002004/003002004001/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"货物"}),f2 ],

    ["zfcg_fuwu_liubiao_gg","http://ggzyjy.yichang.gov.cn/TPFront/jyxx/003002/003002004/003002004002/",["name","ggstart_time","href","info"],add_info(f1,{"gctype":"f服务"}),f2 ],



    ]


def work(conp,**args):
    est_meta(conp,data,diqu="湖北省宜昌市",**args)
    est_html(conp,f=f3,**args)

if __name__=='__main__':
    work(conp=["postgres","since2015","127.0.0.1","hubei","yichang"])


    # for d in data:
    #     url = d[1]
    #     driver = webdriver.Chrome()
    #     driver.get(url)
    #     f = f2(driver)
    #     print(f)
    #     driver = webdriver.Chrome()
    #     driver.get(url)
    #     dd = f1(driver, 1)
    #     print(dd.values)
    #     for i in dd[2].values:
    #         df = f3(driver, i)
    #         print(df)


