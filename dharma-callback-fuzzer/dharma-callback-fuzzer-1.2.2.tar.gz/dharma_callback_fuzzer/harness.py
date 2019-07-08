#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

from os import listdir
from os.path import isfile, join

ROOT = os.path.dirname(os.path.abspath(__file__)) + '/'

def run_test(numtests):
    mypath = ROOT + 'dharma/dharma/grammars/'
    onlyfiles = [mypath + f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".dg") and f != 'common.dg']
    
    p = subprocess.Popen(['python3', '-m', 'dharma', '-grammars'] + onlyfiles + ["-count", str(numtests)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=ROOT + "dharma")
    out, err = [i.strip() for i in p.communicate()]

    lines = '\n'.join(list(filter(lambda x: b"ERROR" in x, err.split(b"\n"))))
    if lines:
        print(err)
        print("ERROR")
        sys.exit(1)

    if out:
        return out


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="dharma callback fuzzer")
    
    parser.add_argument("-n", "--number_of_files", type=int, nargs=1, metavar="number_of_files", default=100, help="Number of files")
    parser.add_argument("-d", "--output_dir", type=str, nargs=1, metavar="output_directory", default=None, help="Output directory")
    
    args = parser.parse_args()
    count = args.number_of_files[0]
    outdir = args.output_dir[0]
    
    for num in range(count):
        
        builder = ""
        
        result = run_test(1);
        results = result.split(b"\n\n\n\n")
        
        for i, r in enumerate(results):
            wrapper = "function testy_%s() {\n%s\n}" % (i, r.strip())
            builder += str(wrapper) + "\n"
        
        for i, r in enumerate(results):
            builder += str("try { testy_%s(); } catch(e) { print(%s + \" \" + e); }\nprint(\"Completed %s\");\n" % (i, i, i))

        file_path = os.path.join(outdir, "test_%s" % num)
        with open(file_path, "w") as f:
            f.write(builder)
