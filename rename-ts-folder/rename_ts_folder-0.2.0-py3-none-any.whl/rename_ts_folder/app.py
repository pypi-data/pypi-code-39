"""
Rename all folder according to a convention
"pa-exsD-2019-06-29-<number>"
Author: Yuhang (Steven) Wang
License: MIT/X11
Date: 
2019-06-09 version 1.0
"""
from typing import List, Pattern
import os
import re
import sys
import glob
import pprint
import argparse
pp = pprint.PrettyPrinter(indent=2)

def path_dir(dir: str) -> str:
  """Return "." if there is no root directory in
  the path name"""
  r = os.path.dirname(dir)
  if r is "":
    return "."
  else:
    return r

def ls(dir_prefix: str) -> List[str]:
  p = re.compile("{}".format(os.path.basename(dir_prefix)))
  root_dir = path_dir(dir_prefix)
  return map(
      lambda x: os.path.join(root_dir, x), 
      filter(lambda x: p.match(x), os.listdir(root_dir)))

def get_target_id(old_file_name: str) -> str:
  """split the input file name by non-word char and _"""
  return re.split(r"[_\W']+", os.path.splitext(old_file_name)[0])[-1]

def new_folder_name(new_prefix: str, old_file_name: str) -> str:
  return "{}{}".format(new_prefix, get_target_id(old_file_name))

def rename_dir(dir_name: str, target_file: str, new_prefix: str) -> str:
  try:
    file_name = glob.glob(os.path.join(dir_name, target_file))[0]
  except IndexError:
    sys.exit("Error hint: cannot find the target file in the designated folders")
  new_dir = new_folder_name(new_prefix, file_name)
  os.rename(dir_name, new_dir)
  return "mv {} {}".format(dir_name, new_dir)

def run(old_dir: str, target_file: str, new_dir_prefix: str) -> List[str]:
  return list(map(
        lambda d: rename_dir(d, target_file, new_dir_prefix),
        ls(old_dir)))

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("old_dir")
  parser.add_argument("target_file")
  parser.add_argument("new_dir_prefix")
  args = parser.parse_args()
  print(args)
  r = run(args.old_dir, args.target_file, args.new_dir_prefix)
  list(map(pp.pprint, r))

if __name__ == "__main__":
  main()
