import unittest
from cusip_generator.main import Generator


class GenerateCusip(unittest.TestCase):
	# valid cases
	def test_AIH8_Index(self):
		generator = Generator('AIH8 Index')
		cusip = generator.convert_to_cusip()
		self.assertEqual(cusip, 'AIH820185')

	def test_C_Z7_Comdty(self):
		generator = Generator('C Z7 Comdty')
		cusip = generator.convert_to_cusip()
		self.assertEqual(cusip, 'CZ7201775')

	def test_LAZ18_Comdty(self):
		generator = Generator('LAZ18 Comdty')
		cusip = generator.convert_to_cusip()
		self.assertEqual(cusip, 'LAZ820180')

	def test_OATZ7_Comdty(self):
		generator = Generator('OATZ7 Comdty')
		cusip = generator.convert_to_cusip()
		self.assertEqual(cusip, 'OATZ72011')

if __name__ == '__main__':
	unittest.main()
