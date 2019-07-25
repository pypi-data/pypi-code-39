from selenium import webdriver
import pandas as pd
import sys
import time, math
from sqlalchemy import create_engine, types
import re
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import traceback
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from threading import Semaphore
from lmf.dbv2 import db_write
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lmfscrap.fake_useragent import UserAgent


def singleton(cls, *args, **kwargs):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class web:
    def __init__(self, add_ip_flag=False):
        self.add_ip_flag = add_ip_flag
        self.ua = UserAgent()
        self.add_ip()
        self.headless = True
        self.pageloadstrategy = 'normal'
        self.pageloadtimeout = 40
        self.url = "http://www.jy.whzbtb.com/V2PRTS/TendererNoticeInfoListInit.do"
        self.get_ip_url = """http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=1&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson="""
        self.result_q = Queue()
        self.tmp_q = Queue()
        self.ip_q = Queue()
        self.__init_tmp_q(10)
        self.sema = Semaphore(1)
        # 本地ip数量设置
        self.__init_localhost_q(ipNum=0)

    def get_driver(self, ip=None):

        chrome_option = webdriver.ChromeOptions()
        if ip is not None: chrome_option.add_argument("--proxy-server=http://%s" % (ip))
        if self.headless:
            chrome_option.add_argument("--headless")
            chrome_option.add_argument("--no-sandbox")

        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = self.pageloadstrategy
        # complete#caps["pageLoadStrategy"] = "eager" # interactive#caps["pageLoadStrategy"] = "none"
        args = {"desired_capabilities": caps, "chrome_options": chrome_option}

        driver = webdriver.Chrome(**args)
        driver.maximize_window()
        driver.set_page_load_timeout(self.pageloadtimeout)
        return driver

    def add_ip(self):
        # 获取本机ip，是否在白名单中
        if self.add_ip_flag:
            try:
                try:
                    r = requests.get("http://www.trackip.net/", timeout=10, headers={'User-Agent': self.ua.random,
                                                                                     'Cookie': '__cfduid=d5cc00aa0983286bb09108ccaef017a2e1563845122; _ga=GA1.2.200115857.1563845158; _gid=GA1.2.766328626.1563845158'}, ).text

                except:
                    r = requests.get("http://200019.ip138.com/", timeout=10, headers={'User-Agent': self.ua.random}).text
                ip = r[r.find('title') + 6:r.find('/title') - 1]
                ip = re.findall("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ip)
                i = 3
                while ip == []:
                    try:
                        r = requests.get("http://www.trackip.net/", timeout=10, headers={'User-Agent': self.ua.random}).text
                    except:
                        r = requests.get("http://200019.ip138.com/", timeout=10, headers={'User-Agent': self.ua.random}).text
                    ip = r[r.find('title') + 6:r.find('/title') - 1]
                    ip = re.findall("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ip)
                    i -= 1
                    if i < 0: break
                ip = ip[0]
                i = 3
                while i > 0:
                    x = """http://http.zhiliandaili.cn/Users-whiteIpListNew.html?appid=3105&appkey=982479357306065df6b3c2f47ec124fc"""
                    r = requests.get(x, timeout=40, headers={'User-Agent': self.ua.random}).json()

                    if "data" in r.keys():
                        ips = r["data"]
                        print('ips', ips)
                        break
                    else:
                        time.sleep(1)
                        i -= 1
                if ips == None:
                    return False
                if ip in ips:
                    print("%s 已经在白名单中" % ip)
                    return True
                i = 3

                while i > 0:
                    x = """http://http.zhiliandaili.cn/Users-whiteIpAddNew.html?appid=3105&appkey=982479357306065df6b3c2f47ec124fc&whiteip=%s""" % ip
                    r = requests.get(x, timeout=40, headers={'User-Agent': self.ua.random}).json()
                    if "存在" in r["msg"]:
                        print("ip : [ %s ] 已经在白名单中" % ip)
                        break
                    if "最多数量" in r["msg"]:
                        time.sleep(1)
                        x = """http://http.zhiliandaili.cn/Users-whiteIpAddNew.html?appid=3105&appkey=982479357306065df6b3c2f47ec124fc&whiteip=%s&index=5""" % ip
                        r = requests.get(x, timeout=40, headers={'User-Agent': self.ua.random}).json()

                    if "成功" in r["msg"]:
                        print("添加ip%s" % ip)
                        break
                    i -= 1
                    time.sleep(1)
                self.add_ip_flag = False
            except:
                traceback.print_exc()
        else:
            print('[Info]:不执行添加本地ip到白名单的操作。')

    def get_ip(self, get_ip_url=False):
        if get_ip_url is False: get_ip_url = self.get_ip_url
        # print(self.get_ip_url)
        self.sema.acquire()
        i = 3
        try:
            url = get_ip_url
            r = requests.get(url, timeout=40, headers={'User-Agent': self.ua.random})
            time.sleep(1)
            ip = r.text
            while re.match("[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}:[0-9]{1,5}", ip) is None and i > 0:
                time.sleep(3 - i)
                i -= 1
                url = get_ip_url
                r = requests.get(url, timeout=40, headers={'User-Agent': self.ua.random})
                time.sleep(1)
                ip = r.text

            self.ip_q.put(r.text)
        except:
            ip = False
        finally:
            self.sema.release()
        return ip

    def __init_localhost_q(self, ipNum=2):
        self.localhost_q = Queue()
        for i in range(ipNum): self.localhost_q.put(i)

    def __init_total(self, f2, ipNum=3, retry=10):
        if retry < 0: retry = 5
        num = retry - ipNum
        if num < 0:
            num = 0
            ipNum = retry
        print("""总共 %s 次尝试爬取页面总量，代理ip爬 %s 次，剩余 %s 本地 ip 爬取。""" % (retry, ipNum, num))
        m = ipNum

        while m > 0:
            try:
                ip = self.get_ip()
                # ip="1.28.0.90:20455"
                print("使用代理ip %s" % ip)
                try:
                    driver = self.get_driver(ip)
                    driver.get(self.url)
                    self.total = f2(driver)
                except Exception as e:
                    driver.quit()
                    traceback.print_exc()
                    raise ValueError('[Error]:url 或 f2_get_total 错了。')
                print("全局共 %d 页面" % self.total)
                return "sccess"
            except Exception as e:
                traceback.print_exc()
                m -= 1
                print("[Error]:用代理ip获取总量,第 %d 次失败" % (ipNum - m))
        while num > 0:
            try:
                try:
                    driver = self.get_driver()
                    driver.get(self.url)
                    self.total = f2(driver)
                except Exception as e:
                    driver.quit()
                    traceback.print_exc()
                    raise ValueError('[Error]:url 或 f2_get_total 错了。')
                print("用本地ip获取总量,全局共 %d 页面" % self.total)
                return "sccess"
            except Exception as e:
                traceback.print_exc()
                num -= 1
                print("[Error]:用本地ip获取总量,第 %d 次失败" % (retry - ipNum - num))

        return "failed"

    def __init_tmp_q(self, total):
        self.tmp_q.queue.clear()
        for i in range(total):
            self.tmp_q.put(i + 1)

    def __read_thread(self, f):
        url = self.url
        if self.localhost_q.empty():
            ip = self.get_ip()
            # ip="1.28.0.90:20455"
            print("本次 ip %s" % ip)
            if re.match("[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}:[0-9]{1,5}", ip) is None:
                print("ip不合法")
                return False

            try:

                driver = self.get_driver(ip)
                driver.get(url)

            except Exception as e:
                traceback.print_exc()
                driver.quit()
                return False
        else:
            try:
                print("使用本机ip")
                self.localhost_q.get(block=False)
                driver = self.get_driver()
                driver.get(url)
            except Exception as e:
                traceback.print_exc()

                driver.quit()
                return False

        while not self.tmp_q.empty():
            try:
                x = self.tmp_q.get(block=False)
            except:
                traceback.print_exc()
                continue
            if x is None: continue
            try:
                df = f(driver, x)
                self.result_q.put(df)

            except Exception as e:
                traceback.print_exc()
                msg = traceback.format_exc()
                print("[Error]:第 %d 页面异常" % x)
                if "违反" not in msg:
                    self.tmp_q.put(x)
                driver.quit()
                return False
        driver.quit()
        print("线程正常退出")
        return True

    def read_thread(self, f, thread_retry=5):

        num = thread_retry
        flag = self.__read_thread(f)
        while not flag and num > 0:
            num -= 1
            print("切换ip,本线程第 %d 次,已经消耗 ip %d 个" % (thread_retry - num, self.ip_q.qsize()))
            flag = self.__read_thread(f)

    def read_threads(self, f, num=10, total=100, ipNum=3, thread_retry=5):
        bg = time.time()
        ths = []
        dfs = []
        if total == 0:
            print("0页,线程不启动，任务结束")
            return False
        if total < 2: num = 1
        if num / total > 1: num = int(total / 5) + 1 if int(total / 5) + 1 < 4 else num
        if total / num < 10: num = int(total / 10) + 1
        if ipNum > num: ipNum = math.ceil(num / 3)
        print("开始爬[%s],本次共 %d 个页面,共 %d 个线程，代理ip %s 个，本地ip %s 个。" % (self.url, total, num, ipNum, num - ipNum))
        self.result_q.queue.clear()
        self.__init_tmp_q(total)
        self.__init_localhost_q(ipNum=(num - ipNum))

        for _ in range(num):
            t = Thread(target=self.read_thread, args=(f, thread_retry))
            ths.append(t)
        for t in ths:
            t.start()
        for t in ths:
            t.join()
        self.__init_localhost_q(ipNum=(num - ipNum))
        left_page = self.tmp_q.qsize()
        print("剩余 %d 页" % (left_page))
        if left_page > 0:
            self.read_thread(f, thread_retry)
            left_page = self.tmp_q.qsize()
            print("剩余 %d 页" % (left_page))
        ed = time.time()
        cost = ed - bg
        if cost < 100:
            print("耗时 %d --秒" % cost)
        else:
            print("耗时 %.4f 分" % (cost / 60))
        print("read_threads结束")

    def getdf_from_result(self):
        if self.result_q.empty():
            return pd.DataFrame(data=[])
        dfs = list(self.result_q.queue)
        df = pd.concat(dfs, ignore_index=False)
        return df

    def getdf(self, url, f1, f2, total, num, ipNum, retry=10, thread_retry=5):
        if ipNum > 10: ipNum = 10
        if ipNum < 0: ipNum = 0
        self.url = url
        self.__init_total(f2, ipNum=ipNum, retry=retry)
        self.__init_tmp_q(self.total)
        if total is None:
            total = self.total
        elif total > self.total:
            total = self.total

        if num is None: num = 10
        if total == 0: return pd.DataFrame()
        self.read_threads(f=f1, num=num, total=total, ipNum=ipNum, thread_retry=thread_retry)
        df = self.getdf_from_result()
        return df

    def write(self, **krg):
        url = krg["url"]
        f1 = krg["f1"]
        f2 = krg["f2"]
        tb = krg["tb"]
        col = krg["col"]
        # headless=krg["headless"]
        if "total" not in krg.keys():
            total = None
        else:
            total = krg["total"]

        if "num" not in krg.keys():
            num = None
        else:
            num = krg["num"]

        if "ipNum" not in krg.keys():
            ipNum = 3
        else:
            ipNum = krg["ipNum"]

        if "thread_retry" not in krg.keys():
            thread_retry = 5
        else:
            thread_retry = krg["thread_retry"]

        if "retry" not in krg.keys():
            retry = 3
        else:
            retry = krg["retry"]

        if "dbtype" not in krg.keys():
            dbtype = "postgresql"
        else:
            dbtype = krg["dbtype"]
        if "conp" not in krg.keys():
            conp = ["postgres", "since2015", "127.0.0.1", "postgres", "public"]
        else:
            conp = krg["conp"]

        if "add_ip_flag" not in krg.keys():
            self.add_ip_flag = False
        else:
            self.add_ip_flag = krg["add_ip_flag"]

        if "get_ip_url" not in krg.keys():
            self.get_ip_url = """http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=1&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson="""
        else:
            self.get_ip_url = krg["get_ip_url"]

        if "headless" not in krg.keys():
            self.headless = True
        else:
            self.headless = krg["headless"]

        if "pageloadstrategy" not in krg.keys():
            self.pageloadstrategy = 'normal'
        else:
            self.pageloadstrategy = krg["pageloadstrategy"]

        if "pageloadtimeout" not in krg.keys():
            self.pageloadtimeout = 40
        else:
            self.pageloadtimeout = krg["pageloadtimeout"]

        print("%s 开始,爬取[%s]" % (tb, url))
        if total == 0: return False
        df = self.getdf(url, f1, f2, total, num, ipNum=ipNum, retry=retry, thread_retry=thread_retry)

        if len(df) > 1:
            print(url)
            # print(df)
            df.columns = col
        else:
            df = pd.DataFrame(columns=col)
            print("暂无数据")
        print("将数据df 写入 %s" % tb)
        db_write(df, tb, dbtype=dbtype, conp=conp, datadict='postgresql-text')
        print("df写入%s完毕" % tb)

    ###页数过多时
    def write_large(self, **krg):
        # 初始化页面队列
        # 开启多线程
        # 写入
        url = krg["url"]
        f1 = krg["f1"]
        f2 = krg["f2"]
        tb = krg["tb"]
        col = krg["col"]

        # headless=krg["headless"]
        if "total" not in krg.keys():
            total = None
        else:
            total = krg["total"]

        if "num" not in krg.keys():
            num = None
        else:
            num = krg["num"]

        if "dbtype" not in krg.keys():
            dbtype = "postgresql"
        else:
            dbtype = krg["dbtype"]

        if "conp" not in krg.keys():
            conp = ["postgres", "since2015", "127.0.0.1", "postgres", "public"]
        else:
            conp = krg["conp"]

        if "ipNum" not in krg.keys():
            ipNum = 3
        else:
            ipNum = krg["ipNum"]

        if "get_ip_url" not in krg.keys():
            self.get_ip_url = """http://ip.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=0&fa=0&fetch_key=&qty=1&time=1&pro=&city=&port=1&format=txt&ss=1&css=&dt=1&specialTxt=3&specialJson="""
        else:
            self.get_ip_url = krg["get_ip_url"]

        if "thread_retry" not in krg.keys():
            thread_retry = 5
        else:
            thread_retry = krg["thread_retry"]

        if "retry" not in krg.keys():
            retry = 3
        else:
            retry = krg["retry"]

        if "add_ip_flag" not in krg.keys():
            self.add_ip_flag = False
        else:
            self.add_ip_flag = krg["add_ip_flag"]

        if "headless" not in krg.keys():
            self.headless = True
        else:
            self.headless = krg["headless"]

        if "pageloadstrategy" not in krg.keys():
            self.pageloadstrategy = 'normal'
        else:
            self.pageloadstrategy = krg["pageloadstrategy"]

        if "pageloadtimeout" not in krg.keys():
            self.pageloadtimeout = 40
        else:
            self.pageloadtimeout = krg["pageloadtimeout"]

        print("%s 开始,爬取[%s]" % (tb, url))
        if not total: return False
        df = self.getdf_large(url, f1, f2, total, num, ipNum=ipNum, retry=retry, thread_retry=thread_retry)

        if len(df) > 1:
            print(url)
            # print(df)
            df.columns = col
        else:
            df = pd.DataFrame(columns=col)
            print("暂无数据")
        print("将数据df 写入 %s" % tb)
        db_write(df, tb, dbtype=dbtype, conp=conp, datadict='postgresql-text', if_exists='append')
        print("df写入%s完毕" % tb)

    def read_threads_large(self, f, num=10, total=list(range(100)), ipNum=3, retry=10, thread_retry=5):
        bg = time.time()
        ths = []
        dfs = []
        total_count = len(total)
        self.__init_localhost_q(ipNum=ipNum)
        if total_count == 0:
            print("0页,线程不启动，任务结束")
            return False
        if total_count < 2: num = 1
        if num / total_count > 1: num = int(total_count / 5) + 1 if int(total_count / 5) + 1 < 4 else num
        if ipNum > num: ipNum = math.ceil(num / 3)
        print("开始爬[%s],本次共 %d 个页面,共 %d 个线程，代理ip %s 个，本地ip %s 个。" % (self.url, total_count, num, ipNum, num - ipNum))
        self.__init_localhost_q(ipNum=(num - ipNum))
        self.result_q.queue.clear()

        # 生成页码queue
        self.tmp_q.queue.clear()
        for i in total:
            self.tmp_q.put(i + 1)

        for _ in range(num):
            t = Thread(target=self.read_thread, args=(f, thread_retry))
            ths.append(t)
        for t in ths:
            t.start()
        for t in ths:
            t.join()
        self.__init_localhost_q(ipNum=3)
        left_page = self.tmp_q.qsize()
        print("剩余 %d 页" % (left_page))
        if left_page > 0:
            self.read_thread(f, thread_retry)
            left_page = self.tmp_q.qsize()
            print("剩余 %d 页" % (left_page))
        ed = time.time()
        cost = ed - bg
        if cost < 100:
            print("耗时 %d --秒" % cost)
        else:
            print("耗时 %.4f 分" % (cost / 60))
        print("read_threads结束")

    def getdf_large(self, url, f1, f2, total, num, ipNum, retry=10, thread_retry=5):
        if ipNum > 10: ipNum = 10
        if ipNum < 0: ipNum = 0
        self.url = url

        ##生成页码queue
        self.tmp_q.queue.clear()
        for i in total:
            self.tmp_q.put(i + 1)

        if not total:
            total = list(range(self.total))
        elif len(total) > self.total:
            total = list(range(self.total))

        if num is None: num = 10
        if total == 0: return pd.DataFrame()
        self.read_threads_large(f=f1, num=num, total=total, ipNum=ipNum, retry=retry, thread_retry=thread_retry)
        df = self.getdf_from_result()
        return df

    def get_total(self, f2, url, ipNum=3, retry=10):

        if retry < 0: retry = 5
        if ipNum > retry: ipNum = retry
        num = retry - ipNum
        if num < 0:
            num = 0
            ipNum = retry
        print("""获取需要爬取的页面总量，先用代理ip爬 %s 次，若失败本地ip爬 %s 次""" % (ipNum, num))

        m = ipNum
        while m > 0:
            try:
                ip = self.get_ip()
                print("使用代理ip %s" % ip)
                driver = self.get_driver(ip)

                driver.get(url)

                self.total = f2(driver)
                driver.quit()
                print("全局共%d 页面" % self.total)
                return self.total
            except Exception as e:
                traceback.print_exc()
                driver.quit()
                m -= 1
                print("[Error]:用代理ip获取总量,第 %d 次失败" % (ipNum - m))
        while num > 0:
            try:
                driver = self.get_driver()
                driver.get(url)
                self.total = f2(driver)
                driver.quit()
                print("用本地ip获取总量,全局共 %d 页面" % self.total)
                return self.total
            except Exception as e:
                traceback.print_exc()
                driver.quit()
                num -= 1
                print("[Error]:用本地ip获取总量,第 %d 次失败" % (retry - ipNum - num))
        return "failed"


