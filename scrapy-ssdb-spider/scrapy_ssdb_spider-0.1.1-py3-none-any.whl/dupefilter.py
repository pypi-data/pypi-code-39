# @Time    : 19-7-1 下午2:45
# @Author  : SuanCaiYu
# @File    : dupefilter.py
# @Software: PyCharm
import logging
from abc import ABCMeta, abstractmethod

from scrapy.utils.request import request_fingerprint

logger = logging.getLogger(__name__)


class BaseDupeFilter:
    __metaclass__ = ABCMeta
    logger = logger

    def __init__(self, ssdb_client, key, debug=False):
        self.ssdb_client = ssdb_client
        self.key = key
        self.debug = debug
        self.logdupes = True

    @abstractmethod
    def request_seen(self, request) -> bool:
        pass

    @abstractmethod
    def close(self, reason):
        pass


class SSDBDupeFilter(BaseDupeFilter):

    def request_seen(self, request) -> bool:
        fp = request_fingerprint(request)
        flag = self.ssdb_client.zset(self.key, fp, 1)
        return flag == 0

    def close(self, reason):
        self.clear()

    def clear(self):
        self.ssdb_client.zclear(self.key)

    def log(self, request, spider):
        """Logs given request.

        Parameters
        ----------
        request : scrapy.http.Request
        spider : scrapy.spiders.Spider

        """
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False
