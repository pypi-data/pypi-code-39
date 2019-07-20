import re
import datetime

ExpiryMonthMapping = {
	"Jan": "F",
	"Feb": "G",
	"Mar": "H",
	"Apr": "J",
	"May": "K",
	"Jun": "M",
	"Jul": "N",
	"Aug": "Q",
	"Sep": "U",
	"Oct": "V",
	"Nov": "X",
	"Dec": "Z",
}

CheckDigitMapping = {
	"*": 36,
	"@": 37,
	"#": 38,
}


def validate(bbg_ticker=""):
	# check the type of the ticker
	if type(bbg_ticker) != str:
		return False, None

	# remove the empty space around the ticker
	bbg_ticker = bbg_ticker.strip()

	valid_expiry_month_codes = [code for month, code in ExpiryMonthMapping.items()]
	valid_sectors = ["Index", "Comdty"]

	# extract prefix, expiry month, expiry year and sector using regexp
	prefix_regex = "(?P<prefix>[A-Z](?: |[A-Z]{1,2}))"
	month_regex = "(?P<month>" + "|".join(valid_expiry_month_codes) + ")"
	year_regex = r"(?P<year>\d{1,2})"
	sector_regex = "(?P<sector>" + "|".join(valid_sectors) + ")"

	ticker_regex = "^" + prefix_regex + month_regex + year_regex + " " + sector_regex + "$"

	rematch = re.match(ticker_regex, bbg_ticker)

	if rematch is None:
		return False, None

	return True, {
		"prefix": rematch.group("prefix"),
		"month": rematch.group("month"),
		"year": rematch.group("year"),
		"sector": rematch.group("sector")
	}


def guess_year(truncated_year_str, current_year_str):
	# check the number of digits in truncated year
	if re.match(r'^\d{1,2}$', truncated_year_str) is None:
		return None

	# replace the last digits of current_year with truncated_year
	return current_year_str[: -len(truncated_year_str)] + truncated_year_str


def compose_eight_digits_cusip(prefix, month, year):
	year_last_digit = year[-1]

	composed_cusip = prefix + month + year_last_digit + year

	return composed_cusip[:8].ljust(8, year_last_digit)


def calculate_check_digit(cusip):
	# check cusip is string
	if type(cusip) != str:
		return None

	cusip = cusip.strip()

	# check cusip is of length 8
	if len(cusip) != 8:
		return None

	result = 0
	v = 0

	for i, char in enumerate(cusip):
		index = i + 1

		if re.match(r'\d', char) is not None:
			v = int(char)
		elif re.match(r'[a-zA-Z]', char) is not None:
			p = ord(char.upper()) - ord('A') + 1
			v = p + 9
		elif char in CheckDigitMapping:
			v = CheckDigitMapping[char]

		if index % 2 == 0:
			v = v * 2

		div, mod = divmod(v, 10)
		result = result + div + mod

	return (10 - result % 10) % 10
