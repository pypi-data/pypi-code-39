import unittest
from cusip_generator.utils import calculate_check_digit


class CalculateCheckDigitTest(unittest.TestCase):
	# valid cases
	def test_037833100(self):
		check_digit = calculate_check_digit("03783310")
		self.assertEqual(check_digit, 0)

	def test_AIH82018_5(self):
		check_digit = calculate_check_digit("AIH82018")
		self.assertEqual(check_digit, 5)

	def test_CZ720177_5(self):
		check_digit = calculate_check_digit("CZ720177")
		self.assertEqual(check_digit, 5)

	def test_LAZ82018_0(self):
		check_digit = calculate_check_digit("LAZ82018")
		self.assertEqual(check_digit, 0)

	def test_OATZ7201_1(self):
		check_digit = calculate_check_digit("OATZ7201")
		self.assertEqual(check_digit, 1)

	# invalid cases
	def test_cusip_non_string(self):
		check_digit = calculate_check_digit(12345678)
		self.assertEqual(check_digit, None)

	def test_cusip_not_length_eight(self):
		check_digit = calculate_check_digit("123456789")
		self.assertEqual(check_digit, None)


if __name__ == '__main__':
	unittest.main()
