#!/usr/bin/env python3

import os
import subprocess
import sys

from os import listdir
from os.path import isfile, join

ROOT = os.path.dirname(os.path.abspath(__file__)) + '/'

def run_test(numtests):
    mypath = ROOT + 'dharma/dharma/grammars/'
    onlyfiles = [mypath + f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".dg") and f != 'common.dg']
    
    p = subprocess.Popen(['python', '-m', 'dharma', '-grammars'] + onlyfiles + ["-count", str(numtests)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=ROOT + "dharma")
    out, err = [i.strip() for i in p.communicate()]
    
    lines = '\n'.join(list(filter(lambda x: "ERROR" in x, err.split("\n"))))
    if lines:
        print(err)
        print("ERROR")
        sys.exit(1)
    
    if out:
        return out


if __name__ == "__main__":
    count = 1000
    outdir = None
    
    if len(sys.argv) >= 1:
        count = int(sys.argv[0])
    
    if len(sys.argv) == 2:
        outdir = sys.argv[1]

    for num in range(count):
        
        builder = ""
        
        result = run_test(1);
        results = result.split("\n\n\n\n")
        
        for i, r in enumerate(results):
            wrapper = "function testy_%s() {\n%s\n}" % (i, r.strip())
            builder += str(wrapper) + "\n"
        
        for i, r in enumerate(results):
            builder += str("try { testy_%s(); } catch(e) { print(%s + \" \" + e); }\nprint(\"Completed %s\");\n" % (i, i, i))


file_path = os.path.join(outdir, "test_%s" % num)
with open(file_path, "w") as f:
    f.write(builder)
