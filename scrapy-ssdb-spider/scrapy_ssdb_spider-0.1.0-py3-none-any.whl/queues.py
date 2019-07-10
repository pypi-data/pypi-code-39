# @Time    : 19-7-1 下午1:59
# @Author  : SuanCaiYu
# @File    : queues.py
# @Software: PyCharm
import pickle
from abc import ABCMeta, abstractmethod

from scrapy.utils.reqser import request_to_dict, request_from_dict


class BaseQueue:
    __metaclass__ = ABCMeta

    def __init__(self, ssdb_client, spider, key):
        self.ssdb_client = ssdb_client
        self.spider = spider
        self.key = key

    def _encode_request(self, request):
        obj = request_to_dict(request, self.spider)
        return pickle.dumps(obj)

    def _decode_request(self, encoded_request):
        obj = pickle.loads(encoded_request)
        return request_from_dict(obj, self.spider)

    @abstractmethod
    def push(self, request):
        pass

    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def __len__(self):
        pass


class FifoQueue(BaseQueue):
    def clear(self):
        self.ssdb_client.qclear(self.key)

    def push(self, request):
        self.ssdb_client.qpush_back(self.key, self._encode_request(request))

    def pop(self):
        data = self.ssdb_client.qpop(self.key)
        if data:
            return self._decode_request(data)

    def __len__(self):
        return self.ssdb_client.qsize(self.key)


class LifoQueue(BaseQueue):
    def clear(self):
        self.ssdb_client.qclear(self.key)

    def push(self, request):
        self.ssdb_client.qpush_front(self.key, self._encode_request(request))

    def pop(self):
        data = self.ssdb_client.qpop(self.key)
        if data:
            return self._decode_request(data)

    def __len__(self):
        return self.ssdb_client.qsize(self.key)
