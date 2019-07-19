import os
import unittest
import json

from jsondler.constants import TESTS_PATH, jsondler_logger
from jsondler import _lib


PACKAGE_TEST_DATA_DIR = "_lib"
INPUT_DIR = os.path.join(TESTS_PATH, 'test_data', PACKAGE_TEST_DATA_DIR)
OUTPUT_DIR = os.path.join(TESTS_PATH, 'test_results', PACKAGE_TEST_DATA_DIR)

try:
    os.makedirs(OUTPUT_DIR)
except OSError:
    pass


class TestGeneralUtils(unittest.TestCase):

    pass


class TestCoordsTools(unittest.TestCase):

    pass


if __name__ == "main":
    unittest.main()
