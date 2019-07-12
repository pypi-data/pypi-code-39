#!/usr/bin/env python

import os, sqlite3, time, unittest
from unittest import mock
from matrixbot.matrixbot import Cache


class TestCache(unittest.TestCase):
    def setUp(self):
        self.timeout = time.time() + 8640000  # 100 days

    @mock.patch("sqlite3.connect")
    def test___init__(self, mock_connect):
        # test an instance with no arguments
        default = Cache()
        self.assertEqual(default.sqlite_uri, "file:memory?mode=memory&cache=shared")
        self.assertIsInstance(default.cache, dict)
        # test specifying ":memory:"
        in_memory = Cache(":memory:")
        self.assertEqual(in_memory.sqlite_uri, "file:memory?mode=memory&cache=shared")
        # test specifying a file
        dbfile = Cache(dbfile="file")
        self.assertEqual(dbfile.sqlite_uri, f"file:file?mode=rwc&cache=shared")

    def test_init_db(self):
        # don't call __init__()
        cache = Cache.__new__(Cache)
        # manually create a sqlite connection
        cache.db = sqlite3.connect(":memory:")
        # call init_db()
        cache.init_db()
        # see if the cache table exists
        self.assertTrue(cache.table_exists("cache"))

    def test_table_exists(self):
        cache = Cache()
        # "cache" should exist
        self.assertTrue(cache.table_exists("cache"))
        # "doesntexist" should not
        self.assertFalse(cache.table_exists("doesntexist"))

    def test_clean_cache(self):
        cache = Cache()
        # insert one item expiring instantly
        cache.insert("clean_test", "!@#$%^&*()_+", time.time())
        # insert one item expiring later
        cache.insert("clean_test2", "!@#$%^&*()_+", self.timeout)
        # clean the cache
        cache.clean_cache()
        # this one should be gone
        self.assertIsNone(cache.query("clean_test"))
        # this one shouldn't
        self.assertEqual(cache.query("clean_test2"), "!@#$%^&*()_+")

    def test_gen_pk(self):
        cache = Cache()
        # make sure we get the md5sum for "key"
        self.assertEqual(cache.gen_pk("key"), "3c6e0b8a9c15224a8228b9a98ca1531d")

    def test_insert(self):
        cache = Cache()
        cache.insert("insert_test", "!@#$%^&*()_+", self.timeout)
        self.assertEqual(cache.query("insert_test"), "!@#$%^&*()_+")

    def test_query(self):
        cache = Cache()
        cache.insert("query_test", "!@#$%^&*()_+", self.timeout)
        self.assertEqual(cache.query("query_test"), "!@#$%^&*()_+")
        # should return None
        self.assertIsNone(cache.query("doesntexist"))

    def test_fetch(self):
        cache = Cache()
        # returns "FETCHED"
        return_FETCHED = lambda: "FETCHED"
        # if we pre-populate the cache, we should get the value we set
        cache.insert("fetch_test", "!@#$%^&*()_+", self.timeout)
        self.assertEqual(cache.fetch("fetch_test", return_FETCHED), "!@#$%^&*()_+")
        # if we set the timeout to expire immediately we should get the callback value
        cache.insert("fetch_test2", "!@#$%^&*()_+", time.time())
        self.assertEqual(cache.fetch("fetch_test2", return_FETCHED), "FETCHED")
        # if there is no pre-set value we should get the callback value as well
        self.assertEqual(cache.fetch("fetch_test3", return_FETCHED), "FETCHED")
