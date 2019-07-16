#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
import json
import six

from redis import StrictRedis

from .constants import NOT_FOUND, DEFAULT_TIMEOUT


@six.add_metaclass(ABCMeta)
class AbstractStore(object):

    @abstractmethod
    def get(self, key, default=NOT_FOUND):
        pass

    @abstractmethod
    def set(self, key, value, timeout=DEFAULT_TIMEOUT):
        pass

    @abstractmethod
    def delete(self, *keys):
        pass


class RedisStore(AbstractStore):

    def __init__(self, conn, serializer=json):
        self._conn = conn
        self._serializer = serializer

    @staticmethod
    def from_url(url):
        conn = StrictRedis.from_url(url)
        return RedisStore(conn)

    def get(self, key, default=NOT_FOUND):
        data = self._conn.get(key)
        if data is None:
            return default
        return self._serializer.loads(data)

    def set(self, key, value, timeout=DEFAULT_TIMEOUT):
        data = value if isinstance(key, six.string_types) else self._serializer.dumps(value)
        self._conn.setex(key, timeout, data)

    def delete(self, *keys):
        self._conn.delete(*keys)
