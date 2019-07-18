"""
Test rename_ts_folder

Author: Yuhang (Steven) Wang
Date: 2019-07-09
"""
from rename_ts_folder.app import run as rtsf
import os
import unittest

def run():
  rtsf("tmp/test-a", "target*.mrc", "tmp/2019-07-09-")
  results = os.listdir("tmp")
  expect = ['2019-07-09-1', '2019-07-09-2', '2019-07-09-3', '2019-07-09-4']
  print("results", results)
  assert all([a == b for a, b in zip(results, expect)])

if __name__ == "__main__":
    run()
