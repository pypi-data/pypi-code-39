"""
Test rename_ts_folder

Author: Yuhang (Steven) Wang
Date: 2019-07-10
"""
from rename_ts_folder.app import run as rtsf
import os
import unittest
from . import setup_tests
from . import clean_up
from . import test_1
from . import test_2


def all_tests():
  return {
    "1": test_1.run,
    "2": test_2.run
  }

def test(testid):
  tests = all_tests()
  setup_tests.main()
  try:
    tests[testid]()
  finally:
    clean_up.main()

if __name__ == "__main__":
    test("1")
