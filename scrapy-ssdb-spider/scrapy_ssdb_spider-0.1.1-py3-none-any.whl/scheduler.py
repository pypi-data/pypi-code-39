# @Time    : 19-7-1 上午11:54
# @Author  : SuanCaiYu
# @File    : scheduler.py
# @Software: PyCharm

from scrapy.utils.misc import load_object
from . import ssdb_default_settings, ssdb


class Scheduler:

    def __init__(self,
                 ssdb_client,
                 queue_key=ssdb_default_settings.SCHEDULER_QUEUE_KEY,
                 queue_cls=ssdb_default_settings.SCHEDULER_QUEUE_CLASS,
                 dupefilter_key=ssdb_default_settings.SCHEDULER_DUPEFILTER_KEY,
                 dupefilter_cls=ssdb_default_settings.SCHEDULER_DUPEFILTER_CLASS,
                 open_clear=ssdb_default_settings.SCHEDULER_OPEN_CLEAR_QUEUE,
                 close_clear=ssdb_default_settings.SCHEDULER_CLOSE_CLEAR_QUEUE):
        self.queue_cls = queue_cls
        self.queue_key = queue_key
        self.ssdb_client = ssdb_client
        self.df_cls = dupefilter_cls
        self.df_key = dupefilter_key
        self.stats = None
        self.open_clear = open_clear
        self.close_clear = close_clear

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        optional = {
            'queue_key': 'SCHEDULER_QUEUE_KEY',
            'queue_cls': 'SCHEDULER_QUEUE_CLASS',
            'dupefilter_key': 'SCHEDULER_DUPEFILTER_KEY',
            'dupefilter_cls': 'DUPEFILTER_CLASS',
            'open_clear': 'SCHEDULER_OPEN_CLEAR_QUEUE',
            'close_clear': 'SCHEDULER_CLOSE_CLEAR_QUEUE',
        }
        kwargs = {}
        for k, v in optional.items():
            val = settings.get(v)
            if val:
                kwargs[k] = val

        kwargs['ssdb_client'] = ssdb.get_ssdb_client_from_setting(settings)
        instance = cls(**kwargs)
        instance.stats = crawler.stats
        return instance

    def open(self, spider):
        self.spider = spider
        try:
            self.queue = load_object(self.queue_cls)(
                ssdb_client=self.ssdb_client,
                spider=self.spider,
                key=self.queue_key % {'spider': spider.name},
            )
        except TypeError as e:
            raise ValueError("Failed to instantiate queue class '%s': %s",
                             self.queue_cls, e)

        try:
            self.df = load_object(self.df_cls)(
                ssdb_client=self.ssdb_client,
                key=self.df_key % {'spider': spider.name}
            )
        except TypeError as e:
            raise ValueError("Failed to instantiate queue class '%s': %s",
                             self.queue_cls, e)

        if self.open_clear:
            self.clear()

    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            self.df.log(request, self.spider)
            return False
        if self.stats:
            self.stats.inc_value('scheduler/enqueued/ssdb', spider=self.spider)
        self.queue.push(request)
        return True

    def next_request(self):
        request = self.queue.pop()
        if request and self.stats:
            self.stats.inc_value('scheduler/dequeued/ssdb', spider=self.spider)
        return request

    def has_pending_requests(self):
        return len(self) > 0

    def __len__(self):
        return len(self.queue)

    def close(self, reason):
        if self.close_clear:
            self.clear()
        self.ssdb_client.disconnect()

    def clear(self):
        self.df.clear()
        self.queue.clear()
