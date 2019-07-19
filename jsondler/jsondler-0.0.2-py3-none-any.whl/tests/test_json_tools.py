import os
import unittest
import json

from jsondler.constants import TESTS_PATH, jsondler_logger
from jsondler import json_tools


PACKAGE_TEST_DATA_DIR = "json_tools"
INPUT_DIR = os.path.join(TESTS_PATH, 'test_data', PACKAGE_TEST_DATA_DIR)
OUTPUT_DIR = os.path.join(TESTS_PATH, 'test_results', PACKAGE_TEST_DATA_DIR)

try:
    os.makedirs(OUTPUT_DIR)
except OSError:
    pass


class TestRequests(unittest.TestCase):

    def test_get_by_path(self):
        target_json = {
            "list1": [3, 4, 5],
            "list2": [{"C": 3, "D": 4, "E": 5}, {"F": 6, "G": 7}, {"C": 8, "F": 9}],
            "A": 1,
            "B": 2,
            "dict1": {"key1": "a", "key2": "b"},
            "dict2": {"l1": ["a", "b"], "l2": ["c", "d"]},
        }

        path = ("*", 0, ["C", "D"])
        exp_res = [
            (["list2", 0, "C"], 3),
            (["list2", 0, "D"], 4),
        ]
        res = json_tools.get_by_path(in_json=target_json, path_list=path)
        self.assertEqual(exp_res, res)

    def test_deepupdate(self):
        d1 = {"k1": 1, "k2": 2, "k3": {"k3_1": 31, "k3_2": 32, "k_3_3": [33, 34, 35]}}
        d2 = {"k1": 1, "k2": 22, "k3": {"k3_2": 32, "k_3_3": [33, 44, 35]}}
        exp_res = {"k1": 1, "k2": 22, "k3": {"k3_1": 31, "k3_2": 32, "k_3_3": [33, 44, 35]}}
        res = json_tools.deepupdate(d=d1, u=d2)
        self.assertEqual(exp_res, res)

    def test_deepdiff(self):
        d1 = {"k1": 1, "k2": 2, "k3": {"k3_1": 31, "k3_2": 32, "k_3_3": [33, 34, 35]}}
        d2 = {"k1": 1, "k2": 22, "k3": {"k3_2": 32, "k_3_3": [33, 44, 35]}}
        exp_res = {"k2": 22, "k3": {"k3_1": None, "k_3_3": [33, 44, 35]}}
        res = json_tools.deepdiff(d1=d1, d2=d2)
        self.assertEqual(exp_res, res)


if __name__ == "main":
    unittest.main()
