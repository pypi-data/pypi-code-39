"""
Set up the dir structure for testing

Author: Yuhang (Steven) Wang
Date: 2019-07-09
"""
import os
from typing import List

def touch(path_items: List[str]):
  d = os.path.join(*path_items[:-1])
  os.makedirs(d, exist_ok=True)
  f = os.path.join(d, path_items[-1])
  with open(f, 'a'):
    os.utime(f, None)

def mkdirs():
  touch(["tmp", "test-a10", "target-1.mrc"])
  touch(["tmp", "test-a20", "target-2.mrc"])
  touch(["tmp", "test-a21", "target_3.mrc"])
  touch(["tmp", "test-a22", "target_4.mrc"])

def main():
  mkdirs()

if __name__ == "__main__":
    main()
