import unittest
from cusip_generator.utils import guess_year


class GuessYearTest(unittest.TestCase):
	# valid cases
	def test_two_digits(self):
		truncated_year = '21'
		guessed = guess_year(truncated_year, '2019')
		self.assertEqual(guessed, '2021')

	def test_one_digit_in_2019(self):
		truncated_year = '8'
		guessed = guess_year(truncated_year, '2019')
		self.assertEqual(guessed, '2018')

	def test_in_digit_in_2029(self):
		truncated_year = '8'
		guessed = guess_year(truncated_year, '2029')
		self.assertEqual(guessed, '2028')

	# invalid cases
	def test_truncated_year_three_digits(self):
		truncated_year = '111'
		guessed = guess_year(truncated_year, '2019')
		self.assertEqual(guessed, None)

	def test_truncated_year_not_number(self):
		truncated_year = 'ab'
		guessed = guess_year(truncated_year, '2019')
		self.assertEqual(guessed, None)


if __name__ == '__main__':
	unittest.main()
