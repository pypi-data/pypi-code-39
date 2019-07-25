#===============================================================================
# check_motifs.py
#===============================================================================

"""Check motifs"""




# Imports ======================================================================

import itertools
import re

from argparse import ArgumentParser
from pybedtools import BedTool
from dismotif.var_to_hg19 import generate_vars_from_file, var_to_hg19



# Constants ====================================================================

RSID_REGEX = re.compile('rs[1-9][0-9]+$')




# Functions ====================================================================

def parse_arguments():
    parser = ArgumentParser(description='disrupted motifs')
    parser.add_argument(
        'variants',
        metavar='<rsid or file>',
        nargs='+',
        help='Variants or list of variants'
    )
    args = parser.parse_args()
    args.variants = list(
        itertools.chain.from_iterable(
            (v,) if RSID_REGEX.match(v) else generate_vars_from_file(v)
            for v in args.variants
        )
    )
    return args

def main():
    args = parse_arguments()
    print(list(r for *r, f in var_to_hg19(args.variants)))
    print(BedTool(r for *r, f in var_to_hg19(args.variants) if len(r) == 4))