import pandas as pd
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from lmf.dbv2 import db_write,db_command,db_query
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
import requests
import json
from zhulong.util.fake_useragent import UserAgent
from zhulong.util.etl import add_info, est_meta, est_html, est_tbs, add_info, est_meta_large
import math

_name_="fujian2"


EndTime = time.strftime("%Y-%m-%d", time.localtime())



def gcjs_zb(f):
    def warp(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span")
        title1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        if '工程建设' not in title1:
            driver.find_element_by_xpath("//ul[@class='ulpar']/li[@class='par']/a/span[contains(string(), '工程建设')]").click()
            locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span[contains(string(), '工程建设')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))

        try:
            title2 = driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil crchil']/a/span").text.strip()
            if '招标公告' not in title2:
                driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '招标公告')]").click()
                locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[string(), '招标公告']")
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        except:
            driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '招标公告')]").click()
            locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[contains(string(), '招标公告')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        # 选择时间
        try:
            driver.find_element_by_xpath("//span[@id='dateShowId'][contains(@style, 'block;')]")
        except:
            driver.find_element_by_xpath("//ul[@id='timeRange']/li/a[contains(string(), '时间区间')]").click()
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[@id='TopTime']").clear()
            driver.find_element_by_xpath("//input[@id='TopTime']").send_keys('2000-01-01')
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[@id='EndTime']").clear()
            driver.find_element_by_xpath("//input[@id='EndTime']").send_keys('%s' % EndTime)
            time.sleep(0.5)
            locator = (By.XPATH, "//div[@class='searBtn']")
            elements = WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
            driver.execute_script("arguments[0].click()", elements)
            time.sleep(0.1)
            locator = (By.XPATH, "//div[@class='loadingTextDiv']")
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(locator))
        return f(*krg)
    return warp

def gcjs_zgys(f):
    def warp(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span")
        title1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        if '工程建设' not in title1:
            driver.find_element_by_xpath("//ul[@class='ulpar']/li[@class='par']/a/span[contains(string(), '工程建设')]").click()
            locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span[contains(string(), '工程建设')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))

        try:
            title2 = driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil crchil']/a/span").text.strip()
            if '资格预审' not in title2:
                driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '资格预审')]").click()
                locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[string(), '资格预审']")
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        except:
            driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '资格预审')]").click()
            locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[contains(string(), '资格预审')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        # 选择时间
        try:
            driver.find_element_by_xpath("//span[@id='dateShowId'][contains(@style, 'block;')]")
        except:
            driver.find_element_by_xpath("//ul[@id='timeRange']/li/a[contains(string(), '时间区间')]").click()
            time.sleep(0.1)
            driver.find_element_by_xpath("//input[@id='TopTime']").clear()
            driver.find_element_by_xpath("//input[@id='TopTime']").send_keys('2000-01-01')
            time.sleep(0.1)
            driver.find_element_by_xpath("//input[@id='EndTime']").clear()
            driver.find_element_by_xpath("//input[@id='EndTime']").send_keys('%s' % EndTime)
            time.sleep(0.1)
            locator = (By.XPATH, "//div[@class='searBtn']")
            elements = WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
            driver.execute_script("arguments[0].click()", elements)
            time.sleep(0.1)
            locator = (By.XPATH, "//div[@class='loadingTextDiv']")
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(locator))
        return f(*krg)
    return warp

def gcjs_bg(f):
    def warp(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span")
        title1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        if '工程建设' not in title1:
            driver.find_element_by_xpath("//ul[@class='ulpar']/li[@class='par']/a/span[contains(string(), '工程建设')]").click()
            locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span[contains(string(), '工程建设')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))

        try:
            title2 = driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil crchil']/a/span").text.strip()
            if '变更公告' not in title2:
                driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '变更公告')]").click()
                locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[string(), '变更公告']")
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        except:
            driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '变更公告')]").click()
            locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[contains(string(), '变更公告')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        # 选择时间
        try:
            driver.find_element_by_xpath("//span[@id='dateShowId'][contains(@style, 'block;')]")
        except:
            driver.find_element_by_xpath("//ul[@id='timeRange']/li/a[contains(string(), '时间区间')]").click()
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[@id='TopTime']").clear()
            driver.find_element_by_xpath("//input[@id='TopTime']").send_keys('2000-01-01')
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[@id='EndTime']").clear()
            driver.find_element_by_xpath("//input[@id='EndTime']").send_keys('%s' % EndTime)
            time.sleep(0.5)
            locator = (By.XPATH, "//div[@class='searBtn']")
            elements = WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
            driver.execute_script("arguments[0].click()", elements)
            time.sleep(0.1)
            locator = (By.XPATH, "//div[@class='loadingTextDiv']")
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(locator))
        return f(*krg)
    return warp

def gcjs_zhongbhx(f):
    def warp(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span")
        title1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        if '工程建设' not in title1:
            driver.find_element_by_xpath("//ul[@class='ulpar']/li[@class='par']/a/span[contains(string(), '工程建设')]").click()
            locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span[contains(string(), '工程建设')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))

        try:
            title2 = driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil crchil']/a/span").text.strip()
            if '中标候选人' not in title2:
                driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '中标候选人')]").click()
                locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[string(), '中标候选人']")
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        except:
            driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '中标候选人')]").click()
            locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[contains(string(), '中标候选人')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        # 选择时间
        try:
            driver.find_element_by_xpath("//span[@id='dateShowId'][contains(@style, 'block;')]")
        except:
            driver.find_element_by_xpath("//ul[@id='timeRange']/li/a[contains(string(), '时间区间')]").click()
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[@id='TopTime']").clear()
            driver.find_element_by_xpath("//input[@id='TopTime']").send_keys('2000-01-01')
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[@id='EndTime']").clear()
            driver.find_element_by_xpath("//input[@id='EndTime']").send_keys('%s' % EndTime)
            time.sleep(0.5)
            locator = (By.XPATH, "//div[@class='searBtn']")
            elements = WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
            driver.execute_script("arguments[0].click()", elements)
            time.sleep(0.1)
            locator = (By.XPATH, "//div[@class='loadingTextDiv']")
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(locator))
        return f(*krg)
    return warp

def gcjs_zhongb(f):
    def warp(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span")
        title1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        if '工程建设' not in title1:
            driver.find_element_by_xpath("//ul[@class='ulpar']/li[@class='par']/a/span[contains(string(), '工程建设')]").click()
            locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span[contains(string(), '工程建设')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))

        try:
            title2 = driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil crchil']/a/span").text.strip()
            if '中标结果公告' not in title2:
                driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '中标结果公告')]").click()
                locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[string(), '中标结果公告']")
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        except:
            driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '中标结果公告')]").click()
            locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[contains(string(), '中标结果公告')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        # 选择时间
        try:
            driver.find_element_by_xpath("//span[@id='dateShowId'][contains(@style, 'block;')]")
        except:
            driver.find_element_by_xpath("//ul[@id='timeRange']/li/a[contains(string(), '时间区间')]").click()
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[@id='TopTime']").clear()
            driver.find_element_by_xpath("//input[@id='TopTime']").send_keys('2000-01-01')
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[@id='EndTime']").clear()
            driver.find_element_by_xpath("//input[@id='EndTime']").send_keys('%s' % EndTime)
            time.sleep(0.5)
            locator = (By.XPATH, "//div[@class='searBtn']")
            elements = WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
            driver.execute_script("arguments[0].click()", elements)
            time.sleep(0.1)
            locator = (By.XPATH, "//div[@class='loadingTextDiv']")
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(locator))
        return f(*krg)
    return warp

def zfcg_zb(f):
    def warp(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span")
        title1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        if '政府采购' not in title1:
            driver.find_element_by_xpath("//ul[@class='ulpar']/li[@class='par']/a/span[contains(string(), '政府采购')]").click()
            locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span[contains(string(), '政府采购')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))

        try:
            title2 = driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil crchil']/a/span").text.strip()
            if '资审公告' not in title2:
                driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '资审公告')]").click()
                locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[string(), '资审公告']")
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        except:
            driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '资审公告')]").click()
            locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[contains(string(), '资审公告')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        # 选择时间
        try:
            driver.find_element_by_xpath("//span[@id='dateShowId'][contains(@style, 'block;')]")
        except:
            driver.find_element_by_xpath("//ul[@id='timeRange']/li/a[contains(string(), '时间区间')]").click()
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[@id='TopTime']").clear()
            driver.find_element_by_xpath("//input[@id='TopTime']").send_keys('2000-01-01')
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[@id='EndTime']").clear()
            driver.find_element_by_xpath("//input[@id='EndTime']").send_keys('%s' % EndTime)
            time.sleep(0.5)
            locator = (By.XPATH, "//div[@class='searBtn']")
            elements = WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
            driver.execute_script("arguments[0].click()", elements)
            time.sleep(0.1)
            locator = (By.XPATH, "//div[@class='loadingTextDiv']")
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(locator))
        return f(*krg)
    return warp

def zfcg_bg(f):
    def warp(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span")
        title1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        if '政府采购' not in title1:
            driver.find_element_by_xpath("//ul[@class='ulpar']/li[@class='par']/a/span[contains(string(), '政府采购')]").click()
            locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span[contains(string(), '政府采购')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))

        try:
            title2 = driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil crchil']/a/span").text.strip()
            if '更正事项' not in title2:
                driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '更正事项')]").click()
                locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[string(), '更正事项']")
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        except:
            driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '更正事项')]").click()
            locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[contains(string(), '更正事项')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        # 选择时间
        try:
            driver.find_element_by_xpath("//span[@id='dateShowId'][contains(@style, 'block;')]")
        except:
            driver.find_element_by_xpath("//ul[@id='timeRange']/li/a[contains(string(), '时间区间')]").click()
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[@id='TopTime']").clear()
            driver.find_element_by_xpath("//input[@id='TopTime']").send_keys('2000-01-01')
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[@id='EndTime']").clear()
            driver.find_element_by_xpath("//input[@id='EndTime']").send_keys('%s' % EndTime)
            time.sleep(0.5)
            locator = (By.XPATH, "//div[@class='searBtn']")
            elements = WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
            driver.execute_script("arguments[0].click()", elements)
            time.sleep(0.1)
            locator = (By.XPATH, "//div[@class='loadingTextDiv']")
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(locator))
        return f(*krg)
    return warp

def zfcg_zhongb(f):
    def warp(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span")
        title1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        if '政府采购' not in title1:
            driver.find_element_by_xpath("//ul[@class='ulpar']/li[@class='par']/a/span[contains(string(), '政府采购')]").click()
            locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span[contains(string(), '政府采购')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))

        try:
            title2 = driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil crchil']/a/span").text.strip()
            if '中标公告' not in title2:
                driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '中标公告')]").click()
                locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[string(), '中标公告']")
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        except:
            driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '中标公告')]").click()
            locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[contains(string(), '中标公告')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        # 选择时间
        try:
            driver.find_element_by_xpath("//span[@id='dateShowId'][contains(@style, 'block;')]")
        except:
            driver.find_element_by_xpath("//ul[@id='timeRange']/li/a[contains(string(), '时间区间')]").click()
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[@id='TopTime']").clear()
            driver.find_element_by_xpath("//input[@id='TopTime']").send_keys('2000-01-01')
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[@id='EndTime']").clear()
            driver.find_element_by_xpath("//input[@id='EndTime']").send_keys('%s' % EndTime)
            time.sleep(0.5)
            locator = (By.XPATH, "//div[@class='searBtn']")
            elements = WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
            driver.execute_script("arguments[0].click()", elements)
            time.sleep(0.1)
            locator = (By.XPATH, "//div[@class='loadingTextDiv']")
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(locator))
        return f(*krg)
    return warp

def qita_zb(f):
    def warp(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span")
        title1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        if '其他' not in title1:
            driver.find_element_by_xpath("//ul[@class='ulpar']/li[@class='par']/a/span[contains(string(), '其他')]").click()
            locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span[contains(string(), '其他')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))

        try:
            title2 = driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil crchil']/a/span").text.strip()
            if '交易公告' not in title2:
                driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '交易公告')]").click()
                locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[string(), '交易公告']")
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        except:
            driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '交易公告')]").click()
            locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[contains(string(), '交易公告')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        # 选择时间
        try:
            driver.find_element_by_xpath("//span[@id='dateShowId'][contains(@style, 'block;')]")
        except:
            driver.find_element_by_xpath("//ul[@id='timeRange']/li/a[contains(string(), '时间区间')]").click()
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[@id='TopTime']").clear()
            driver.find_element_by_xpath("//input[@id='TopTime']").send_keys('2000-01-01')
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[@id='EndTime']").clear()
            driver.find_element_by_xpath("//input[@id='EndTime']").send_keys('%s' % EndTime)
            time.sleep(0.5)
            locator = (By.XPATH, "//div[@class='searBtn']")
            elements = WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
            driver.execute_script("arguments[0].click()", elements)

            time.sleep(0.1)
            locator = (By.XPATH, "//div[@class='loadingTextDiv']")
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(locator))
        return f(*krg)
    return warp

def qita_zhongb(f):
    def warp(*krg):
        driver = krg[0]
        locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span")
        title1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        if '其他' not in title1:
            driver.find_element_by_xpath("//ul[@class='ulpar']/li[@class='par']/a/span[contains(string(), '其他')]").click()
            locator = (By.XPATH, "//ul[@class='ulpar']/li[@class='par cr']/a/span[contains(string(), '其他')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))

        try:
            title2 = driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil crchil']/a/span").text.strip()
            if '成交公示' not in title2:
                driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '成交公示')]").click()
                locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[string(), '成交公示']")
                WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        except:
            driver.find_element_by_xpath("//li[@class='par cr']/ul/li[@class='chil']/a/span[contains(string(), '成交公示')]").click()
            locator = (By.XPATH, "//li[@class='par cr']/ul/li[@class='chil crchil']/a/span[contains(string(), '成交公示')]")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
        # 选择时间
        try:
            driver.find_element_by_xpath("//span[@id='dateShowId'][contains(@style, 'block;')]")
        except:
            driver.find_element_by_xpath("//ul[@id='timeRange']/li/a[contains(string(), '时间区间')]").click()
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[@id='TopTime']").clear()
            driver.find_element_by_xpath("//input[@id='TopTime']").send_keys('2000-01-01')
            time.sleep(0.5)
            driver.find_element_by_xpath("//input[@id='EndTime']").clear()
            driver.find_element_by_xpath("//input[@id='EndTime']").send_keys('%s' % EndTime)
            time.sleep(0.5)
            locator = (By.XPATH, "//div[@class='searBtn']")
            elements = WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
            driver.execute_script("arguments[0].click()", elements)
            time.sleep(0.1)
            locator = (By.XPATH, "//div[@class='loadingTextDiv']")
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located(locator))
        return f(*krg)
    return warp


def f1_data(driver, num):
    driver.get(surl)
    locator = (By.XPATH, "//div[@id='list']/div[1]//h4/a")
    val = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).get_attribute('href')[-9:]
    locator = (By.XPATH, "//span[@class='fp-text']/b")
    cnum = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text

    url = driver.current_url
    if num != int(cnum):
        driver.execute_script('setPage(%d)' % num)
        locator = (By.XPATH, "//div[@id='list']/div[1]//h4/a[not(contains(@href, '%s'))]" % val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find("div", id="list")
    trs = table.find_all("div" ,class_='publicont')
    data = []
    for tr in trs:
        a = tr.find_all('a')
        try:
            title = a[0]["title"].strip()
        except:
            title = a[0].text.strip()
        if not title:raise ValueError
        if ss == 'dayi':
            span = tr.find_all("span", class_='span_o')[-1]
            if span.find('a'):
                href = span.find('a')["href"]
                if 'http' in href:
                    link = href
                else:
                    link = "https://www.fjggfw.gov.cn/Website/FJBID_DATA/" + href.strip()
                td = '-'
                tmp = [title, td, link]
                data.append(tmp)
            else:continue

        elif ss == 'zhongbhx':
            span = tr.find_all("span", class_='span_o')[-2]
            if span.find('a'):
                href = span.find('a')["href"]
                if 'http' in href:
                    link = href
                else:
                    link = "https://www.fjggfw.gov.cn/Website/FJBID_DATA/" + href.strip()
                td = '-'
                tmp = [title, td, link]
                data.append(tmp)
            else:continue

        elif ss == 'zhongb':
            span = tr.find_all("span", class_='span_o')[-3]
            if span.find('a'):
                href = span.find('a')["href"]
                if 'http' in href:
                    link = href
                else:
                    link = "https://www.fjggfw.gov.cn/Website/FJBID_DATA/" + href.strip()
                td = '-'
                tmp = [title, td, link]
                data.append(tmp)
            else:continue

        elif ss == 'zb':
            href = a[0]["href"]
            if 'http' in href:
                link = href
            else:
                link = "https://www.fjggfw.gov.cn/Website/FJBID_DATA/" + href.strip()
            try:
                td = tr.find_all("span", class_='span_o')[0].text.strip()
            except:
                td = '-'
            tmp = [title, td, link]
            data.append(tmp)

    df = pd.DataFrame(data)
    df['info'] = None
    return df


def f1(driver, num):
    url = driver.current_url
    if '/FJBID_DATA_LIST.aspx' in url:
        daf = f1_data(driver, num)
        return daf

    locator = (By.XPATH, "//div[@id='list']/div[last()]//a")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    cnum = driver.find_element_by_xpath("//span[@class='curr']").text.strip()

    if num != int(cnum):
        val = driver.find_element_by_xpath("//div[@id='list']/div[last()]//a").get_attribute('href')[-20:]
        driver.execute_script("kkpager._clickHandler({})".format(num))
        locator = (By.XPATH, "//div[@id='list']/div[last()]//a[not(contains(@href, '%s'))]"% val)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    data = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('div', id='list')
    lis = table.find_all('div', class_='publicont')
    for tr in lis:
        a = tr.find('a')
        try:
            name = a['title']
        except:
            name = a.text.strip()
        ggstart_time = tr.find('span', class_='span_o').text.strip()
        onclick = a['href']
        if 'http' in onclick:
            href = onclick
        else:
            href = 'https://www.fjggfw.gov.cn/Website/' + onclick
        info = {}
        p = tr.find('p', class_='p_tw')
        tn = len(p.find_all('span', class_='span_on'))
        for i in range(int(tn)):
            if i == 0:
                diqu = p.find_all('span', class_='span_on')[0].text.strip()
                info['diqu']=diqu
            elif i == 1:
                laiyuan = p.find_all('span', class_='span_on')[1].text.strip()
                info['laiyuan']=laiyuan
            elif i == 2:
                ywlx = p.find_all('span', class_='span_on')[2].text.strip()
                info['ywlx']=ywlx
            elif i == 3:
                xxlx = p.find_all('span', class_='span_on')[3].text.strip()
                info['xxlx']= xxlx
            elif i == 4:
                hy = p.find_all('span', class_='span_on')[4].text.strip()
                info['hy']= hy
        if info:info = json.dumps(info, ensure_ascii=False)
        else:info = None

        tmp = [name, ggstart_time, href, info]
        data.append(tmp)
    df = pd.DataFrame(data=data)
    return df



def f2(driver):
    url = driver.current_url
    if '/FJBID_DATA_LIST.aspx' in url:
        global surl,ss
        surl,ss=None,None
        surl = url.rsplit('/', maxsplit=1)[0]
        ss = url.rsplit('/', maxsplit=1)[1]
        driver.get(surl)
        locator = (By.XPATH, "//div[@id='list']/div[1]//h4/a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//span[@class='fp-text']/i")
        num = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        driver.quit()
        return int(num)

    else:
        locator = (By.XPATH, "//div[@id='list']/div[last()]//a")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
        locator = (By.XPATH, "//span[@class='totalPageNum']")
        num = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator)).text.strip()
        driver.quit()
        return int(num)





def f3(driver, url):
    driver.get(url)
    if ('JYXX_GCJS' in url) or ('FJBID_DATA' in url):
        locator = (By.XPATH, "//div[@class='gc_body'][string-length()>160]")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
        locator = (By.XPATH, "//div[@id='noteContentMain'][string-length()>30]")
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located(locator))
        flag = 1
    else:
        locator = (By.XPATH, "//div[@class='fully_toggle_cont'][contains(@style, 'block;')][string-length()>60]")
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(locator))
        flag = 2
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
    if flag ==1:
        div = soup.find('div', class_="gc_body")
    elif flag == 2:
        div = soup.find('div', attrs={"class":"fully_toggle_cont", "style":re.compile('block;')})
    else:raise ValueError
    return div


data = [
    ["gcjs_zhaobiao_gg",
     "https://www.fjggfw.gov.cn/Website/JYXXNew.aspx",
     ["name", "ggstart_time", "href", "info"],gcjs_zb(f1),gcjs_zb(f2)],

    ["gcjs_zgys_gg",
     "https://www.fjggfw.gov.cn/Website/JYXXNew.aspx",
     ["name", "ggstart_time", "href", "info"],gcjs_zgys(f1),gcjs_zgys(f2)],

    ["gcjs_biangeng_gg",
     "https://www.fjggfw.gov.cn/Website/JYXXNew.aspx",
     ["name", "ggstart_time", "href", "info"], gcjs_bg(f1), gcjs_bg(f2)],

    ["gcjs_zhongbiaohx_gg",
     "https://www.fjggfw.gov.cn/Website/JYXXNew.aspx",
     ["name", "ggstart_time", "href", "info"],gcjs_zhongbhx(f1), gcjs_zhongbhx(f2)],

    ["gcjs_zhongbiao_gg",
     "https://www.fjggfw.gov.cn/Website/JYXXNew.aspx",
     ["name", "ggstart_time", "href", "info"],gcjs_zhongb(f1), gcjs_zhongb(f2)],

    ["zfcg_zhaobiao_gg",
     "https://www.fjggfw.gov.cn/Website/JYXXNew.aspx",
     ["name", "ggstart_time", "href", "info"],zfcg_zb(f1), zfcg_zb(f2)],

    ["zfcg_biangeng_gg",
     "https://www.fjggfw.gov.cn/Website/JYXXNew.aspx",
     ["name", "ggstart_time", "href", "info"], zfcg_bg(f1),zfcg_bg(f2)],

    ["zfcg_zhongbiao_gg",
     "https://www.fjggfw.gov.cn/Website/JYXXNew.aspx",
     ["name", "ggstart_time", "href", "info"],zfcg_zhongb(f1),zfcg_zhongb(f2)],
    #
    ["jqita_zhaobiao_gg",
     "https://www.fjggfw.gov.cn/Website/JYXXNew.aspx",
     ["name", "ggstart_time", "href", "info"], qita_zb(f1), qita_zb(f2)],

    ["jqita_zhongbiao_gg",
     "https://www.fjggfw.gov.cn/Website/JYXXNew.aspx",
     ["name", "ggstart_time", "href", "info"], qita_zhongb(f1), qita_zhongb(f2)],

    ####
    ["jqita_zhoabiao_lishishuju_gg",
     "https://www.fjggfw.gov.cn/Website/FJBID_DATA/FJBID_DATA_LIST.aspx/zb",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["jqita_dayi_lishishuju_gg",
     "https://www.fjggfw.gov.cn/Website/FJBID_DATA/FJBID_DATA_LIST.aspx/dayi",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["jqita_zhongbiaohx_lishishuju_gg",
     "https://www.fjggfw.gov.cn/Website/FJBID_DATA/FJBID_DATA_LIST.aspx/zhongbhx",
     ["name", "ggstart_time", "href", "info"], f1, f2],

    ["jqita_zhongbiao_lishishuju_gg",
     "https://www.fjggfw.gov.cn/Website/FJBID_DATA/FJBID_DATA_LIST.aspx/zhongb",
     ["name", "ggstart_time", "href", "info"], f1, f2],
]



def work(conp,**args):
    est_meta_large(conp,data=data,diqu="福建省省级",interval_page=300,**args)
    est_html(conp,f=f3,**args)


# 修改日期：2019/7/18
if __name__=='__main__':
    work(conp=["postgres","since2015","192.168.3.171","fujian","fujian2"])

    # for d in data[-5:]:
    #     driver=webdriver.Chrome()
    #     url=d[1]
    #     print(url)
    #     driver.get(url)
    #     df = qita_zhongb(f2)(driver)
    #     print(df)
    #     driver = webdriver.Chrome()
    #     driver.get(url)
    #
    #     df=qita_zhongb(f1)(driver, 12)
    #     print(df.values)
    #     for f in df[2].values:
    #         d = f3(driver, f)
    #         print(d)

