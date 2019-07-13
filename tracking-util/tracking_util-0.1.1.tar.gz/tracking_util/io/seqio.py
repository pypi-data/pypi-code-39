#!/usr/bin/env python
import cv2
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
logging.basicConfig(format=sFORMAT, level=logging.INFO)


def load_seqinfo(seqroot, gtfn='groundtruth.txt', img_subfolder='img',
        load_imgs=False, get_resolution=False):
    """
    seqroot has following structure:
    seqroot/
        img/
        groundtruth.txt
    """
    gt_path = os.path.join(seqroot, gtfn)
    gtrects = read_gtrects(gt_path)
    seqname = seqroot.split('/')[-1]

    img_filenames = sorted(
        glob.glob(os.path.join(seqroot, img_subfolder, '*')))
    result_dict = {'gt_rect': gtrects, 'img_fns': img_filenames,
            'seqname': seqname, 'seqlen': len(img_filenames)}

    if load_imgs:
        result_dict['imgs'] = [cv2.imread(f) for f in img_filenames]

    if get_resolution:
        if load_imgs:
            resolution = result_dict['imgs'][0].shape
        else:
            sample = img_filenames[0]
            resolution = cv2.imread(sample).shape
        result_dict.update(
            {'width': resolution[1], 'height': resolution[0],
             'channel': resolution[2]})

    return result_dict


def read_gtrects(gt_path, delimiter=',', dtype=float):
    with open(gt_path) as f:
        gtrects = [[dtype(k) for k in l.split(delimiter)] for l in f]
    return gtrects


def write_sequence(imgs, gtrects, seqfolder):
    if not os.path.exists(seqfolder):
        os.makedirs(seqfolder)
    img_folder = os.path.join(seqfolder, 'img')
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)

    write_imgs(imgs, img_folder)
    write_gtrects(gtrects, seqfolder)


def write_imgs(imgs, img_folder, img_fn_format='%04d.jpg'):
    if not os.path.exists(img_folder):
        raise FileNotFoundError("img folder does not exist: %s" % img_folder)

    for i, img in enumerate(imgs):
        cv2.imwrite(os.path.join(img_folder, img_fn_format % i), img)


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


def save_as_video(img_sequence, fn, fps=24):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # fps = fps
    height, width, _ = img_sequence[0].shape
    size = (width, height)

    if fn[-4:] != '.mp4':
        fn = fn + '.mp4'

    out = cv2.VideoWriter(fn, fourcc, fps, size)

    for frame in img_sequence:
        out.write(frame)

    out.release()
