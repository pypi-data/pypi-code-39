from unittest import TestCase

from stocknews import fetch
import pandas


class TestReadRss(TestCase):
    def test_can_read(self):
        entry = fetch.read_rss(['AMAZN'], use_csv=False)
        self.assertTrue(isinstance(entry, pandas.DataFrame))
