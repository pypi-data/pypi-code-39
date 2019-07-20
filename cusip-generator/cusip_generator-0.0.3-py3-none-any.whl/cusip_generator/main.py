from .utils import validate, guess_year, compose_eight_digits_cusip, calculate_check_digit
import datetime


class Generator:
	def __init__(self, bbg_ticker):
		self.bbg_ticker = bbg_ticker

	def validate_bbg_ticker(self):
		valid, result = validate(self.bbg_ticker)
		return valid

	def convert_to_cusip(self):
		# validate the bbg ticker
		valid, result = validate(self.bbg_ticker)

		if not valid:
			return 'The ticker format is incorrect'

		prefix = result['prefix'].strip()
		expiry_month = result['month']

		# guess the expiry year
		now = datetime.datetime.now()
		current_year = now.year
		expiry_year = guess_year(result['year'], str(current_year))

		# compose 8 digits CUSIP
		eight_digits_cusip = compose_eight_digits_cusip(prefix, expiry_month, expiry_year)
		check_digit = calculate_check_digit(eight_digits_cusip)

		return eight_digits_cusip + str(check_digit)

