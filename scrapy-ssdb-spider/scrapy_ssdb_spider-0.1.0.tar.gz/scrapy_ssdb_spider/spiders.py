# @Time    : 19-7-1 下午4:51
# @Author  : SuanCaiYu
# @File    : spiders.py
# @Software: PyCharm
from scrapy import signals
from scrapy.spiders import Spider
from scrapy.exceptions import DontCloseSpider

from . import ssdb, ssdb_default_settings


class SsdbMixin:
    ssdb_key = None
    ssdb_batch_size = None

    ssdb_client = None
    settings = None

    def init_settings(self, crawler):

        if crawler is None:
            crawler = getattr(self, 'crawler', None)

        if crawler is None:
            raise ValueError("crawler is required")

        self.settings = crawler.settings
        if self.ssdb_key is None:
            self.ssdb_key = self.settings.get(
                'SSDB_START_URLS_KEY', ssdb_default_settings.START_URLS_KEY,
            )

        if not self.ssdb_key.strip():
            raise ValueError("ssdb_key must not be empty")
        self.ssdb_key = self.ssdb_key % {'spider': self.name}
        if self.ssdb_batch_size is None:
            self.ssdb_batch_size = self.settings.getint(
                'SSDB_START_URLS_BATCH_SIZE',
                self.settings.getint('CONCURRENT_REQUESTS'),
            )

        try:
            self.ssdb_batch_size = int(self.ssdb_batch_size)
        except (TypeError, ValueError):
            raise ValueError("ssdb_batch_size must be an integer")

        self.logger.info("Reading start URLs from ssdb key '%(ssdb_key)s' "
                         "(batch size: %(ssdb_batch_size)s",
                         self.__dict__)
        self.ssdb_client = ssdb.get_ssdb_client_from_setting(self.settings)
        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        crawler.signals.connect(self._close_conn, signal=signals.spider_closed)

    def start_requests(self):
        return self.next_requests()

    def next_requests(self):
        found = 0
        while found < self.ssdb_batch_size:
            data = self.ssdb_client.qpop_front(self.ssdb_key)
            if not data:
                break
            req = self.make_request_from_data(data)
            if req:
                yield req
                found += 1
            else:
                self.logger.debug("Request not made from data: %r", data)
        if found:
            self.logger.debug("Read %s requests from '%s'", found, self.ssdb_key)

    def make_request_from_data(self, data):
        if isinstance(data, bytes):
            data = data.decode()
        return self.make_requests_from_url(data)

    def schedule_next_requests(self):
        for req in self.next_requests():
            self.crawler.engine.crawl(req, spider=self)

    def _check_ssdb_heartbeat(self) -> bool:
        try:
            self.ssdb_client.dbsize()
        except Exception as e:
            return False
        else:
            return True

    def spider_idle(self):
        if not self._check_ssdb_heartbeat():
            self.ssdb_client = ssdb.get_ssdb_client_from_setting(self.settings)
        self.schedule_next_requests()
        raise DontCloseSpider

    def _close_conn(self, reason):
        try:
            self.ssdb_client.disconnect()
        except:
            pass


class SsdbSpider(SsdbMixin, Spider):

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        obj = super(SsdbSpider, cls).from_crawler(crawler, *args, **kwargs)
        obj.init_settings(crawler)
        return obj
