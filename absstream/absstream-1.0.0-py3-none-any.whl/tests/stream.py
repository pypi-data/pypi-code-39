import unittest
from absstream.stream import Stream


class Test(unittest.TestCase):
    def test_stream(self):
        s = Stream('123')
        