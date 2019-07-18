"""
Clean up the files

Author: Yuhang (Steven) Wang
Date: 2019-07-09
License: MIT/X11
"""
import os
import shutil

def cleanup():
  shutil.rmtree(os.path.join(".", "tmp"))

def main():
  cleanup()

if __name__ == "__main__":
  main()
