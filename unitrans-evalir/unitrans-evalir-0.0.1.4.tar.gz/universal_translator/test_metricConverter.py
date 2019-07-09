import unittest
from metricConverter import *


class TestMetricConverter(unittest.TestCase):
    def testGetIndividualConversion(self):
        converter = MetricConverter()
        self.assertEqual(
            1, converter.getIndividualConversion(1000, "m", "km"))

    def testConvert(self):
        converter = MetricConverter()
        self.assertEqual(
            ["1000 m km 1.0"], converter.convert([["1000", "m", "km"]])
        )
