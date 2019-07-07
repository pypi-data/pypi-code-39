import requests
from datetime import datetime
from gerridae.log import logger


class Spider:
    start_urls = []

    def _start(self, url):
        pass

    def parse(self, response):
        raise NotImplementedError

    @classmethod
    def start(cls):
        start_time = datetime.now()
        spider_ins = cls()
        for url in cls.start_urls:
            spider_ins.parse(requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}))

        logger.info(f'total time is {(datetime.now() - start_time)}')
