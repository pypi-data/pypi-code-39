#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/12 10:26
# @Author  : ganliang
# @File    : CnvdLoopholeSpider.py
# @Desc    : cnvd漏洞爬虫
import json
import logging
import urllib2
from datetime import datetime

from lxml import etree
from scrapy import Spider, Request

from mmscrapy.utils.SeleniumCookieUtil import get_cookie


class CnvdLoopholeSpider(Spider):
    name = "cnvd_loophole_spider"
    allowed_domains = ['cnvd.org.cn']

    custom_settings = {
        "ITEM_PIPELINES": {
            'mmscrapy.pipelines.ConsolePipeline.ConsolePipeline': 300,
            'mmscrapy.pipelines.JsonFilePipeline.JsonFilePipeline': 302
        },
        "COOKIE_SELENIUM_URL": "http://www.cnvd.org.cn/flaw/show/CNVD-2017-27958",
        "DOWNLOADER_MIDDLEWARES": {
            'mmscrapy.middlewares.MmscrapyDownloaderMiddleware': 543,
            'mmscrapy.middleware.RandomUserAgent.RandomUserAgent': 540,
            'mmscrapy.middleware.ProxyMiddleware.ProxyMiddleware': 541,
        }
    }
    logger = logging.getLogger(__name__)
    application_loophole_type = {
        "29": "WEB应用",
        "32": "产品安全",
        "28": "应用程序",
        "27": "操作系统",
        "30": "数据库",
        "33": "智能设备（物联网终端设备",
        "31": "网络设备（交换机、路由器等网络端设备）",
    }

    industry_loophole_type = {
        "telecom": "电信",
        "mi": "移动互联网",
        "ics": "工控系统"
    }

    # cookies = {"__jsluid_s": "38346ecf045cb5db588036f93f6b68f6",
    #            " __jsluid_h": "13f7b0b9313af8d2154cd7036a47b58b",
    #            " __jsl_clearance": "1562927910.858|0|TnPMwOWG4Z2sK9rFL%2F%2FAM0zGPYo%3D",
    #            "JSESSIONID": "DDEA057AF4F64AC0F2D2AF7B49ABE074"}

    def __init__(self, *args, **kwargs):
        # typeId  应用漏洞列表 2
        self.typeId = kwargs.get("typeId", "")

        self.base_urls = []
        self.base_domain = "cnvd.org.cn"
        for sub_typeid in self.typeId.split(","):
            if sub_typeid == "":
                self.base_urls.append("https://www.{0}/flaw/list.htm".format(self.base_domain))
            elif sub_typeid.isdigit():
                # self.base_urls.append("https://www.{0}/flaw/typelist?typeId={1}".format(self.base_domain, sub_typeid))
                self.base_urls.append("https://www.{0}/flaw/typeResult?typeId={1}".format(self.base_domain, sub_typeid))
            else:
                self.base_urls.append("https://{0}.{1}/".format(sub_typeid, self.base_domain))

        self.cookies = get_cookie(self.base_urls[0])
        self.logger.info("get cookie from selenium : {0}".format(json.dumps(self.cookies, ensure_ascii=False)))

    def start_requests(self):
        for base_url in self.base_urls:
            yield Request(base_url, callback=self.parse, dont_filter=False, meta={'cookiejar': 1}, cookies=self.cookies)

    def parse(self, response):
        """
        即系漏洞列表数据
        :param response:
        :return:
        """
        self.logger.info(response.request.url)
        # 应用漏洞列表
        if response.css(".tlist tr").getall():
            loophole_urls = response.css(".tlist tr td a[href]::attr(href)").getall()
            # 分页
            pages = response.css(".pages a[href]::attr(href)").getall()
        # 行业漏洞
        elif response.css(".con .con_left .list").getall():
            # 跳转到详情页面进行解析
            loophole_urls = response.css(".con .con_left .list table tr td a[href]::attr(href)")
            # 分页
            pages = response.css(".con .con_left .list .pages a[href]::attr(href)").getall()
        else:
            self.logger.warn("not match loophole")
            self.logger.warn(response)
            loophole_urls = []
            pages = []

        self.logger.info(loophole_urls)
        for loophole_url in loophole_urls:
            yield response.follow(loophole_url, callback=self.parse_loophole_info, dont_filter=False,
                                  meta={'cookiejar': 1}, cookies=self.cookies)

        for page in pages:
            yield response.follow(page, callback=self.parse, dont_filter=False, meta={'cookiejar': 1},
                                  cookies=self.cookies)

    def parse_loophole_info(self, response):
        """
        爬取漏洞详情页面
        :param response:
        :return:
        """
        blkContainerSblk = response.css(".blkContainer .blkContainerPblk .blkContainerSblk")

        loophole_result = {}

        # 标题信息
        loophole_result.setdefault("url", response.request.url)
        loophole_result.setdefault("title", blkContainerSblk.css("h1::text").extract_first())
        loophole_result.setdefault("create_time", datetime.now().strftime("%Y%m%d%H%M%S"))

        # 漏洞信息
        trs = blkContainerSblk.css(".blkContainerSblkCon .tableDiv table tr")
        for tr in trs:
            tds = tr.css("td::text").getall()
            key, value = tds[0], ",".join(tds[1:])
            if key == "CNVD-ID":
                loophole_result.setdefault("cnvdId", value.strip())
            elif key == "公开日期":
                loophole_result.setdefault("pubdate", value.strip())
            elif key == "危害级别":
                loophole_result.setdefault("damegeLevel", value.strip())
            elif key == "影响产品":
                loophole_result.setdefault("reflectProduct", value.strip())
            elif key == "BUGTRAQ ID":
                loophole_result.setdefault("bugtraqId", value.strip())
            elif key == "CVE ID":
                loophole_result.setdefault("cveId", tr.css("td a::text").extract_first())
                loophole_result.setdefault("cveUrl", tr.css("td a::attr(href)").extract_first())
            elif key == "漏洞描述":
                loophole_result.setdefault("desc", value.strip())
            elif key == "漏洞类型":
                loophole_result.setdefault("type", value.strip())
            elif key == "参考链接":
                loophole_result.setdefault("referLinks", ",".join(tr.css("td a::attr(href)").getall()))
            elif key == "漏洞解决方案":
                loophole_result.setdefault("resolves", value.strip())
            elif key == "厂商补丁":
                loophole_result.setdefault("vendorPatchLink",
                                           response.urljoin(tr.css("td a::attr(href)").extract_first()))
                loophole_result.setdefault("vendorPatchDesc", tr.css("td a::text").extract_first())
            elif key == "验证信息":
                loophole_result.setdefault("verify", value.strip())
            elif key == "报送时间":
                loophole_result.setdefault("submitDate", value.strip())
            elif key == "收录时间":
                loophole_result.setdefault("InclusionDate", value.strip())
            elif key == "更新时间":
                loophole_result.setdefault("updateDate", value.strip())
            elif key == "漏洞附件":
                loophole_result.setdefault("attach", value.strip())

        if not loophole_result.get("title"):
            self.logger.warn(response)
        else:
            yield loophole_result


if __name__ == "__main__":
    DEFAULT_REQUEST_HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        "Cookie": "__jsluid_s=38346ecf045cb5db588036f93f6b68f6; JSESSIONID=1463E3E90C2E00D2E35E3CA7E43DFD44; __jsluid_h=13f7b0b9313af8d2154cd7036a47b58b; __jsl_clearance=1562913569.837|0|uKqg1WOP%2B8O9CMRlFzjRCU1PzDE%3D"
    }

    request = urllib2.Request("https://www.cnvd.org.cn/flaw/typeResult?typeId=29&max=20&offset=20",
                              headers=DEFAULT_REQUEST_HEADERS)
    page_content = urllib2.urlopen(request).read()
    # 获取html内容的content-type标签 找到html编码

    print (page_content)
    page_html = etree.HTML(page_content)
    flawList = page_html.xpath("//table[@class='tlist']//tr/td/a/text()")
    print flawList
