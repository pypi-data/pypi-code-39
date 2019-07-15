#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/11 19:10
# @Author  : ganliang
# @File    : XiaohuarSpider.py
# @Desc    : 校花网校花资料信息爬取
import logging
import urllib2
from datetime import datetime

from lxml import etree
from scrapy import Spider, Request

from mmscrapy.items.ImageItem import ImageItem


class XiaohuarImageSpider(Spider):
    name = "xiaohuar_image_spider"
    custom_settings = {"ITEM_PIPELINES": {
        'mmscrapy.pipelines.ConsolePipeline.ConsolePipeline': 300,
        # 'mmscrapy.pipelines.ImagePipeline.ImagePipeline': 301,
        'mmscrapy.pipelines.JsonFilePipeline.JsonFilePipeline': 302
    }}
    logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        self.category = kwargs.get("category", "hua,xiaocao,mm,meinv")  # "xiaocao", "hua", "mm", "meinv"

        # 支持的数据格式 info:个人详情，image:图片，news:新闻,video:视频(由于vip暂未实现)
        self.type = kwargs.get("type", "info")

        self.base_urls = []

        for subcategory in self.category.split(","):
            self.base_urls.append("http://www.xiaohuar.com/{0}/".format(subcategory))

        self.func = None
        if self.type == "info":
            self.func = self.parse_detail
        elif self.type == "image":
            self.func = self.parse_image
        elif self.type == "video":
            self.func = self.parse_video
        elif self.type == "news":
            self.func = self.parse_news
        else:
            self.func = self.parse

    def start_requests(self):
        for base_url in self.base_urls:
            yield Request(base_url, callback=self.func, dont_filter=False)

    def parse(self, response):
        self.logger.info(response)

    def parse_image(self, response):
        """
        解析校花 校草图片 然后进行下载
        :param response:
        :return:
        """
        imgs = []
        # 校花、校草详情页面图片抓取
        imgs.extend(response.css("#post .photo_ul img::attr(src)").getall())
        # 美女详情页面图片抓取
        imgs.extend(response.css("#detail-page-bd .photo-m img::attr(src)").getall())
        imgs = [img for img in set(imgs)]
        self.logger.info(imgs)
        for img in imgs:
            item = ImageItem()
            item['url'] = response.urljoin(img)
            yield item

        # 校花主页面跳转
        imglinks = response.css("#list_img .item_list .img a[href]::attr('href')").getall()
        # 美女主页面跳转
        imglinks.extend(response.css("#images .items a[href]::attr('href')").getall())
        # 美女详情 分页跳转
        imglinks.extend(response.css("#detail-page-bd #pages a[href]::attr('href')").getall())
        # 分页跳转
        imglinks.extend(response.css(".page_num a[href]::attr('href')").getall())

        imglinks = [imglink for imglink in set(imglinks)]
        self.logger.info(imglinks)
        for imglink in imglinks:
            yield response.follow(imglink, callback=self.parse_image, dont_filter=False)

    def parse_detail(self, resp):
        """
        解析校花详细个人信息
        :param resp:
        :return:
        """

        def parse_detail_info_post(response):
            post = response.css("#post")
            type = response.css("#map a::text").getall()
            if type and len(type) > 1: type = type[-1]
            # 个人信息
            infobox = post.css(".entry_box .res_infobox")
            title = infobox.css(".div_h1 h1::text").extract_first()
            thumb = infobox.css(".infoleft_imgdiv img::attr(src)").extract_first()
            album = infobox.css(".infoleft_imgdiv a::attr(href)").extract_first()
            url = response.request.url

            # 评分
            score = infobox.css(".score_div #span_score::text").extract_first()
            vote = infobox.css(".score_div #lbl_score::text").extract_first()

            infotable = infobox.css(".infodiv table tr td::text").getall()

            infocontent = post.css(".entry_box .infocontent p span::text").getall()

            photo_ul = post.css(".entry_box .photo_ul li img::attr(src)").getall() or []
            photo_ul = [response.urljoin(photo_url) for photo_url in photo_ul if photo_url]

            return {
                "type": type,
                "url": response.urljoin(url),
                "album": response.urljoin(album),
                "title": title,
                "thumb": response.urljoin(thumb),
                "infotable": infotable,
                "infocontent": infocontent,
                "photo_ul": [url for url in set(photo_ul)],
                "score": score,
                "vote": vote,
            }

        def parse_detail_info_bd(response):
            detailpagebd = response.css("#detail-page-bd")
            type = detailpagebd.css(".detail-tab-title a::text").extract_first()
            title = detailpagebd.css(".detail-tab-title span::text").extract_first()

            thumb = detailpagebd.css(".photo-Middle .big-pic table tr td img::attr(src)").extract_first()
            photo_ul = detailpagebd.css(".photo-Middle table tr td img::attr(src)").extract_first() or []
            photo_ul = [response.urljoin(photo_url) for photo_url in photo_ul if photo_url]

            url = response.request.url

            infocontent = detailpagebd.css(".Middle-right .userbox span::text").extract_first()
            infotable = detailpagebd.css(".Middle-right .detail-id .content span::text").getall()

            return {
                "type": type,
                "url": response.urljoin(url),
                "album": None,
                "title": title,
                "thumb": response.urljoin(thumb),
                "infotable": infotable,
                "infocontent": infocontent,
                "photo_ul": [url for url in set(photo_ul)],
                "score": None,
                "vote": None,
            }

        def parse_detail_info_meinv(response):
            detailpagebd = response.css("#detail-page-bd")
            type = detailpagebd.css(".detail-btn span a::text").getall()
            if type and len(type) > 1: type = type[-1]

            title = detailpagebd.css(".detail-tab-title h1::text").extract_first()
            url = response.request.url

            infotable = detailpagebd.css(".c_l p::text").getall()

            thumb = detailpagebd.css(".photo-m img::attr(src)").extract_first()
            photo_ul = detailpagebd.css(".photo-m img::attr(src)").getall() or []
            hphoto_ul = detailpagebd.css(".photo-m a::attr(href)").getall() or []
            # 获取分区的图册
            pages = detailpagebd.css("#pages a::attr(href)").getall()
            for page in pages:
                logging.info(response.urljoin(page))
                page_content = str(urllib2.urlopen(response.urljoin(page), timeout=5).read())
                page_html = etree.HTML(page_content)
                photo_ul.extend(page_html.xpath("//div[@class='photo-m']/a/img/@src"))
                hphoto_ul.extend(page_html.xpath("//div[@class='photo-m']/a/@href"))

            photo_ul = [response.urljoin(photo_url) for photo_url in photo_ul if photo_url]
            hphoto_ul = [response.urljoin(hphoto_url) for hphoto_url in hphoto_ul if hphoto_url]

            return {
                "type": type,
                "url": response.urljoin(url),
                "album": None,
                "title": title,
                "thumb": response.urljoin(thumb),
                "infotable": infotable,
                "infocontent": [],
                "photo_ul": [url for url in set(photo_ul)],
                "hphoto_ul": [hurl for hurl in set(hphoto_ul)],
                "score": None,
                "vote": None,
            }

        def parse_detail_info(response):
            """
            解析详情页面 详情页面可能包含如下三种类型 post bd
            :param response:
            :return:
            """
            post = response.css("#post").getall()
            if post:
                result = parse_detail_info_post(response)
            else:
                detailpagebd = response.css("#detail-page-bd")
                if detailpagebd.css(".Middle-right").getall():
                    result = parse_detail_info_bd(response)
                else:
                    result = parse_detail_info_meinv(response)
            if result and result.get("title"):
                result.setdefault("create_time", datetime.now().strftime("%Y%m%d%H%M%S"))
                yield result

        # 解析校花个人信息
        imglinks = resp.css("#list_img .item_list .img a[href]::attr('href')").getall()
        imglinks.extend(resp.css("#images .items a[href]::attr('href')").getall())
        imglinks = [imglink for imglink in set(imglinks)]
        self.logger.info(imglinks)
        for imglink in imglinks:
            yield resp.follow(imglink, callback=parse_detail_info, dont_filter=False)

        # 美女
        # 分页
        pages = resp.css(".page_num a[href]::attr('href')").getall()
        for page in pages:
            yield resp.follow(page, callback=self.parse_detail, dont_filter=False)

    def parse_news(self, resp):
        """
        解析新闻
        :param response:
        :return:
        """
        # 获取新闻内容
        if resp.css(".mainbox").getall():
            title = resp.css(".mainbox .pagetite::text").extract_first()
            edit_time = resp.css(".mainbox .info::text").extract_first()
            type = resp.css(".mainbox .info a::text").extract_first()
            author = resp.css(".mainbox .info::text").getall()
            if author and len(author) > 1:
                author = author[-1].strip()
            else:
                author = "".join(author)

            thumb = resp.css(".mainbox img::attr(src)").extract_first()
            content = resp.css(".mainbox .content_wrap p::text").getall()

            yield {
                "author": author,
                "title": title,
                "edit_time": edit_time.strip(),
                "type": type,
                "thumb": resp.urljoin(thumb),
                "content": content,
                "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "url": resp.request.url
            }
        # 获取标题的超链接
        # forwardlinks = resp.css(".g-doc .g-mn .container ul li a[href]::attr('href')").getall()
        # forwardlinks = [forwardlink for forwardlink in set(forwardlinks)]
        # self.logger.info(forwardlinks)
        # for forwardlink in forwardlinks:
        #     yield resp.follow(forwardlink, callback=self.parse_news, dont_filter=False)

        # 分页
        pages = resp.css(".g-doc .g-mn a[href]::attr('href')").getall()
        for page in pages:
            yield resp.follow(page, callback=self.parse_news, dont_filter=False)

    def parse_video(self, response):
        """
        解析视频 TODO 视频全会vip通道,暂时没法下载
        :param response:
        :return:
        """
        pass
