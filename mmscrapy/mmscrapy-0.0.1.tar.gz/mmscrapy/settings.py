# -*- coding: utf-8 -*-

# Scrapy settings for mmscrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging

BOT_NAME = 'mmscrapy'

SPIDER_MODULES = ['mmscrapy.spiders']
NEWSPIDER_MODULE = 'mmscrapy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'mmscrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

"""
当COOKIES_ENABLED是注释的时候scrapy默认没有开启cookie
当COOKIES_ENABLED没有注释设置为False的时候scrapy默认使用了settings里面的cookie
当COOKIES_ENABLED设置为True的时候scrapy就会把settings的cookie关掉，使用自定义cookie
"""
# Disable cookies (enabled by default)
COOKIES_ENABLED = True
COOKIES_DEBUG = True

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = True

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    "Cookie": "__jsluid_s=38346ecf045cb5db588036f93f6b68f6; __jsl_clearance=1562907762.47|0|8VpAb79S%2BsFw6YzdwC62tRvML6k%3D; JSESSIONID=1463E3E90C2E00D2E35E3CA7E43DFD44"
}

# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'mmscrapy.middlewares.MmscrapySpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'mmscrapy.middlewares.MmscrapyDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'mmscrapy.pipelines.ConsolePipeline.ConsolePipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# log
LOG_ENABLED = True
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(asctime)s|%(process)d|%(thread)d|%(filename)s[%(funcName)s:%(lineno)d]|%(levelname)s|%(message)s"

# filter
dont_filter = False
DUPEFILTER_CLASS = "scrapy.dupefilters.RFPDupeFilter"
DUPEFILTER_DEBUG = True

# 处理http请求521反爬虫错误 403 Forbidden(The server understood the request but refuses to authorize it.)
HTTPERROR_ALLOWED_CODES = [521, 301, 403, 503]
