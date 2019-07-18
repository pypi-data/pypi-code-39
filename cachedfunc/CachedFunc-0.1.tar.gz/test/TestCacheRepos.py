import os
import unittest
from unittest.mock import patch

import fakeredis
import uuid

from CachedFunc.CacheRepos import MemRepo, RedisRepo, JsonRepo


# Here we use MemRepo as the basic test case and cache repo.
class TestMemRepo(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = MemRepo()

    def test_saveAndGet(self):
        l = [1, 2, 3]
        self.repo['key1'] = l
        self.assertEqual(self.repo['key1'], [1, 2, 3])
        self.assertFalse(self.repo['key1'] is l)
        ll = self.repo['key1']
        self.assertFalse(self.repo['key1'] is ll)

    def test_in(self):
        self.assertFalse('key2' in self.repo)
        self.repo['key2'] = 3
        self.assertTrue('key2' in self.repo)


class TestRedisRepo(TestMemRepo):
    def setUp(self) -> None:
        redis_patcher = patch('redis.Redis', fakeredis.FakeStrictRedis)
        self.redis = redis_patcher.start()
        self.addCleanup(redis_patcher.stop)
        self.repo = RedisRepo()


class TestJsonRepo(TestMemRepo):
    def setUp(self) -> None:
        self.repo = JsonRepo('tmp.json', -1)

    def test_dumpAndLoad(self):
        self.repo['key3'] = 15
        del self.repo
        self.repo = JsonRepo('tmp.json')
        self.assertTrue('key3' in self.repo)

    def tearDown(self) -> None:
        del self.repo
        os.remove('tmp.json')
