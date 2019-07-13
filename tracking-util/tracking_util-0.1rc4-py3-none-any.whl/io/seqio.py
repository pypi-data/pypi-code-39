#!/usr/bin/env python
import os
import numpy as np
import argparse
import json
import sys
import scipy.io as sio
import matplotlib.pyplot as plt
import math
import glob
import logging
import time
from tqdm import tqdm

vFORMAT = ('%(asctime)s '
          '[%(filename)s %(funcName)s() line:%(lineno)d] '
          '- %(levelname)s: %(message)s')
rFORMAT = ('[%(filename)s %(funcName)s() line:%(lineno)d] '
          '- %(levelname)s: %(message)s')
sFORMAT = ('- %(levelname)s: %(message)s')
logging.basicConfig(format=sFORMAT, level=logging.DEBUG)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    '''
    templates
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')
    parser.add_argument('--list', default='all', choices=['servers', 'all'])
    parser.add_argument('--something', action='store_true')
    parser.add_argument('--something', required=True)
    parser.add_argument('file', type=argparse.FileType('r'), nargs='+')

    '''
    args = parser.parse_args()
    return args


# def main():
#     # args = parse_args()
#     # print(args)
#     write_gtrects([[1, float('nan'), 2, 3.0]], '.', dtype=float)


def load_seq(seqroot, gtfn='groundtruth.txt', img_subfolder='img'):
    """
    seqroot has following structure:
    seqroot/
        img/
        groundtruth.txt
    """
    gt_path = os.path.join(seqroot, gtfn)
    gtrects = read_gtrects(gt_path)

    img_filenames = sorted(
        glob.glob(os.path.join(seqroot, img_subfolder, '*')))

    return {'gt_rect': gtrects, 'img_fns': img_filenames}


def read_gtrects(gt_path, delimiter=',', dtype=float):
    with open(gt_path) as f:
        gtrects = [[dtype(k) for k in l.split(delimiter)] for l in f]
    return gtrects


def write_gtrects(gtrects, gt_folder,
        delimiter=',', gt_fn='groundtruth.txt', dtype=int):
    if not os.path.exists(gt_folder):
        raise FileNotFoundError("target folder %s is not found" % gt_folder)
    str_content = []
    for l in gtrects:
        l_content = []
        for n in l:
            if math.isnan(n):
                l_content.append('nan')
            else:
                l_content.append(str(dtype(n)))
        str_content.append(delimiter.join(l_content))

    logging.debug(str_content)

    with open(os.path.join(gt_folder, gt_fn), 'w') as f:
        f.writelines('\n'.join(str_content))
