# @Time    : 19-7-1 下午1:05
# @Author  : SuanCaiYu
# @File    : ssdb_default_settings.py
# @Software: PyCharm

SCHEDULER_QUEUE_KEY = '%(spider)s:requests'
SCHEDULER_QUEUE_CLASS = 'scrapy_ssdb_spider.queues.FifoQueue'
SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'
SCHEDULER_DUPEFILTER_CLASS = 'scrapy_ssdb_spider.dupefilter.SSDBDupeFilter'

START_URLS_KEY = '%(name)s:start_urls'

SCHEDULER_OPEN_CLEAR_QUEUE = False
SCHEDULER_CLOSE_CLEAR_QUEUE = False
