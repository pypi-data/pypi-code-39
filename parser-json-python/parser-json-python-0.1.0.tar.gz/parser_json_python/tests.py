import unittest

from datetime import datetime

from parser_json_python.fields import *
from parser_json_python.parser import DefaultParser


class TestField(unittest.TestCase):
    def test_int(self):
        self.assertEqual(
            first=FieldInt().convert(value='100'),
            second=100, msg=True
        )
        self.assertEqual(
            first=FieldInt().convert(value='100', field_name='digit'),
            second=100, msg=True
        )
        self.assertEqual(
            first=FieldInt().convert(value='1.0'),
            second='1.0', msg=True
        )

    def test_float(self):
        self.assertEqual(
            first=FieldFloat().convert(value='1.100'),
            second=1.1, msg=True
        )
        self.assertEqual(
            first=FieldFloat().convert(value='1.111', field_name='float'),
            second=1.111, msg=True
        )
        self.assertEqual(
            first=FieldFloat().convert(value='10'),
            second='10', msg=True
        )

    def test_list(self):
        self.assertEqual(
            first=FieldList().convert(value='1,2,3,4'),
            second=['1', '2', '3', '4'], msg=True
        )
        self.assertEqual(
            first=FieldList().convert(value='1,2,3,4', field_name='list_field'),
            second=['1', '2', '3', '4'], msg=True
        )
        self.assertEqual(
            first=FieldList().convert(value='1,2,3,4', field_name='field'),
            second='1,2,3,4', msg=True
        )
        self.assertEqual(
            first=FieldList().convert(value='1'),
            second=['1'], msg=True
        )

    def test_date(self):
        self.assertEqual(
            first=FieldDate().convert(value='2000-01-01 10:00'),
            second=datetime(year=2000, month=1, day=1, hour=10, minute=0), msg=True
        )
        self.assertEqual(
            first=FieldDate().convert(value='2000-01-1 10:10', field_name='date_field'),
            second=datetime(year=2000, month=1, day=1, hour=10, minute=10), msg=True
        )
        self.assertEqual(
            first=FieldDate().convert(value='2000-01-01 10:20', field_name='field'),
            second='2000-01-01 10:20', msg=True
        )
        self.assertEqual(
            first=FieldDate().convert(value='2000-01-01'),
            second='2000-01-01', msg=True
        )


class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = DefaultParser

    def test_parser(self):
        params_input = {
            'int': '10',
            'float': '10.1',
            'list_field': '1,2,3',
            'date_field': '2000-01-01 10:00'
        }
        params_output = {
            'int': 10,
            'float': 10.1,
            'list_field': ['1', '2', '3'],
            'date_field': datetime(year=2000, month=1, day=1, hour=10, minute=0)
        }
        self.assertEqual(
            first=self.parser.parse(params_input),
            second=params_output, msg=True
        )


if __name__ == '__main__':
    unittest.main()
