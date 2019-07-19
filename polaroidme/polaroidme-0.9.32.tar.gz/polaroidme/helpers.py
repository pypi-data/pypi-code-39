#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime as dt
from collections import OrderedDict
import logging
from operator import itemgetter
import os
import json

from polaroidme.polaroidme import get_exif

import exifread
from PIL import Image

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

def get_images_in_dir(directory=None, suffix=('jpg','jpeg','png','gif', 'bmp', 'tif','tiff'),traversal=True):
    res = []
    if traversal:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(suffix):
                    fqfn = os.path.join(root, file)
                    res.append(fqfn)
                    log.debug("file match: {}".format(fqfn))
    else:
        for file in os.listdir(directory):
            if file.endswith(suffix):
                fqfn = os.path.join(directory, file)
                res.append(fqfn)
    return res

def sort_images_by_name(images):
    pass

def sort_images_by_time(images, exclude_on_no_data = True, reverse= True, return_meta = False):
    return sort_images_by_original_ctime(images, exclude_on_no_data = exclude_on_no_data, reverse = reverse, return_meta = return_meta)

def sort_images_by_original_ctime(images, exclude_on_no_data = True, reverse = True, return_meta = True):
    """
    """
    DATA_UNAVAIL = []
    meta = { }

    for fn in images:
        exif_data = get_exif(fn)
        if ('EXIF DateTimeOriginal') in exif_data:
            log.debug("exif_data about DateTime: {}; {}; {}".format(fn, exif_data['Image DateTime'], exif_data['EXIF DateTimeOriginal']))
            v = exif_data['EXIF DateTimeOriginal']
            timestamp = dt.datetime.strptime(str(v), '%Y:%m:%d %H:%M:%S')
            meta[fn] = timestamp
        else:
            log.debug("exif_data about DateTime unavailable: {}; ;".format(fn))
            DATA_UNAVAIL.append(fn)
    log.info("exif_data about DateTime unavailable for {} images.".format(len(DATA_UNAVAIL)))
    # create sorted list
    for k,v in meta.items():
        if (k == None) or (v == None):
            log.critical("Oooouch. This should not happen... :-/ %s,%s" % (k,v))
    meta_sorted = OrderedDict(sorted(meta.items(), key = itemgetter(1), reverse = reverse))
    sorted_list = meta_sorted.keys()
    sorted_list = list(sorted_list)
    if not exclude_on_no_data:
        sorted_list.append(DATA_UNAVAIL)
        for fn in DATA_UNAVAIL:
            meta_sorted[fn] = None
        log.warning("exlude_on_no_data={} => added {} images without exif-data.".format(exclude_on_no_data, len(DATA_UNAVAIL)))
    else:
        log.warning("exlude_on_no_data={} => skipped {} images without exif-data.".format(exclude_on_no_data, len(DATA_UNAVAIL)))
    if return_meta:
        return sorted_list, meta_sorted, DATA_UNAVAIL
    return sorted_list


def filter_images_by_time(images, exclude_on_no_data = True):
    pass

def filter_images_by_size(images, min_size, max_size = None):
    """
    usefull to find only high-resolution photos and kicking out
    thumbnails and junk on the fly
    """
    pass
