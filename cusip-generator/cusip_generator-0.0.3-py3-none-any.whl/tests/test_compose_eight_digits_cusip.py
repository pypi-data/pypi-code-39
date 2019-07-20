import unittest
from cusip_generator.utils import compose_eight_digits_cusip


class ComposeEightDigitsCusipTest(unittest.TestCase):
	def test_prefix_one_digit(self):
		cusip = compose_eight_digits_cusip("C", "Z", "2017")
		self.assertEqual(cusip, "CZ720177")

	def test_prefix_two_digits(self):
		cusip = compose_eight_digits_cusip("CA", "Z", "2017")
		self.assertEqual(cusip, "CAZ72017")

	def test_prefix_three_digits(self):
		cusip = compose_eight_digits_cusip("CAB", "Z", "2017")
		self.assertEqual(cusip, "CABZ7201")


if __name__ == '__main__':
	unittest.main()
