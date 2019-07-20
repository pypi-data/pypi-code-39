import unittest
from cusip_generator.utils import validate


class ValidateTypeString(unittest.TestCase):
	# valid cases
	def test_is_string(self):
		ticker = 'C Z7 Comdty'
		valid, result = validate(ticker)
		self.assertEqual(valid, True)

	# invalid cases
	def test_is_not_string(self):
		ticker = 120
		valid, result = validate(ticker)
		self.assertEqual(valid, False)


class ValidatePrefix(unittest.TestCase):
	# valid cases
	def test_one_uppercase_alphas(self):
		ticker = 'C Z7 Comdty'
		valid, result = validate(ticker)
		self.assertEqual(valid, True)

	def test_two_uppercase_alphas(self):
		ticker = 'CAZ7 Comdty'
		valid, result = validate(ticker)
		self.assertEqual(valid, True)

	def test_three_uppercase_alphas(self):
		ticker = 'CAAZ7 Comdty'
		valid, result = validate(ticker)
		self.assertEqual(valid, True)

	# invalid cases
	def test_four_uppercase_alphas(self):
		ticker = 'CAAAZ7 Comdty'
		valid, result = validate(ticker)
		self.assertEqual(valid, False)

	def test_contains_lowercase_alphas(self):
		ticker = 'CaZ7 Comdty'
		valid, result = validate(ticker)
		self.assertEqual(valid, False)

	def test_length_one(self):
		ticker = 'CZ7 Comdty'
		valid, result = validate(ticker)
		self.assertEqual(valid, False)


class ValidateExpirationMonth(unittest.TestCase):
	# valid cases
	def test_month_code_in_mapping(self):
		ticker = 'C Z7 Comdty'
		valid, result = validate(ticker)
		self.assertEqual(valid, True)

	# invalid cases
	def test_month_code_not_in_mapping(self):
		ticker = 'C A7 Comdty'
		valid, result = validate(ticker)
		self.assertEqual(valid, False)


class ValidateExpirationYear(unittest.TestCase):
	# valid cases
	def test_one_digit(self):
		ticker = 'C Z7 Comdty'
		valid, result = validate(ticker)
		self.assertEqual(valid, True)

	def test_two_digits(self):
		ticker = 'C Z17 Comdty'
		valid, result = validate(ticker)
		self.assertEqual(valid, True)

	# invalid cases
	def test_three_digits(self):
		ticker = 'C Z177 Comdty'
		valid, result = validate(ticker)
		self.assertEqual(valid, False)

	def test_no_digits(self):
		ticker = 'C Z Comdty'
		valid, result = validate(ticker)
		self.assertEqual(valid, False)

	def test_non_digits(self):
		ticker = 'C Za Comdty'
		valid, result = validate(ticker)
		self.assertEqual(valid, False)


class ValidateSector(unittest.TestCase):
	# valid cases
	def test_is_Index(self):
		ticker = 'C Z7 Index'
		valid, result = validate(ticker)
		self.assertEqual(valid, True)

	def test_is_Comdty(self):
		ticker = 'C Z7 Comdty'
		valid, result = validate(ticker)
		self.assertEqual(valid, True)

	# invalid cases
	def test_no_space_in_front(self):
		ticker = 'CAZ7Index'
		valid, result = validate(ticker)
		self.assertEqual(valid, False)

	def test_not_Index_nor_Comdty(self):
		ticker = 'C Za Sector'
		valid, result = validate(ticker)
		self.assertEqual(valid, False)


if __name__ == '__main__':
	unittest.main()
