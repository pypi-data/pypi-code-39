import os
import unittest
import json

from jsondler.constants import TESTS_PATH, jsondler_logger
from jsondler import dicts_list


PACKAGE_TEST_DATA_DIR = "jsondler"
INPUT_DIR = os.path.join(TESTS_PATH, 'test_data', PACKAGE_TEST_DATA_DIR)
OUTPUT_DIR = os.path.join(TESTS_PATH, 'test_results', PACKAGE_TEST_DATA_DIR)

try:
    os.makedirs(OUTPUT_DIR)
except OSError:
    pass


class TestDictsList(unittest.TestCase):

    dicts_list_obj = dicts_list.DictsList([
        {"id": 1, "coords": {"x": 0, "y": 0}},
        {"id": 3, "coords": {"x": 2, "y": 0}},
        {"id": 2, "coords": {"x": 0, "y": 1}},
        {"id": 3, "coords": {"x": 1, "y": 0}},
        {"id": 10},
    ])

    def test_DictsList_sort(self):
        sorted_dicts_list = dicts_list.DictsList([
            {"id": 1, "coords": {"x": 0, "y": 0}},
            {"id": 2, "coords": {"x": 0, "y": 1}},
            {"id": 3, "coords": {"x": 1, "y": 0}},
            {"id": 3, "coords": {"x": 2, "y": 0}},
            {"id": 10},
        ])

        self.dicts_list_obj.sort(prior_list=(("*", "id"), ("*", "coords", "x")))
        self.assertEqual(sorted_dicts_list, self.dicts_list_obj)


if __name__ == "main":
    unittest.main()
