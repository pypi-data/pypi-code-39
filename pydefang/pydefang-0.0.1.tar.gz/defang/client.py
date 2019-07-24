#!/usr/bin/env python3

import sys
import argparse

from defang import *

# Taken from: https://mail.python.org/pipermail/tutor/2003-November/026645.html
class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

# Remove buffering, processing large datasets eats memory otherwise
sys.stdout = Unbuffered(sys.stdout)

def parse_args(prog):
    parser = argparse.ArgumentParser(prog=prog)
    parser.add_argument('value', nargs='?', type=str, default=None,
                        help="Value to convert (can also be supplied on stdin)")

    return parser.parse_args()

def run(prog):
    args = parse_args(prog)

    urls = sys.stdin
    if args.value != None:
        urls = [args.value]

    for url in urls:
        url = url.rstrip()
        print(getattr(lib, prog)(url))

def defang():
    run('defang')

def refang():
    run('refang')

