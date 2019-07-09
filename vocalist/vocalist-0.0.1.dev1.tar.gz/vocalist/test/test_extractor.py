import queue
import time
from unittest import TestCase
from ..extractor import Extractor


class ExtractorTest(TestCase):

    def setUp(self) -> None:
        self._test_input_q = queue.Queue()
        self._extractor = Extractor(self._test_input_q)
        pass

    def tearDown(self) -> None:
        pass

    def test_successful_start(self):
        self._extractor.observe()
        self._test_input_q.put("test!")
        time.sleep(.1)
        assert not self._extractor.output_q.empty()

    def test_successful_stop(self):
        self._extractor.observe()
        self._extractor.ignore()
        self._test_input_q.put("test!")
        _ = self._extractor.output_q.get(True)
        self._test_input_q.put("test again!")
        time.sleep(.1)
        assert self._extractor.output_q.empty()
