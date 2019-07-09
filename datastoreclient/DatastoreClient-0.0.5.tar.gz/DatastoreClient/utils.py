import hashlib
import ntpath
import json
import re
import logging as log

def compute_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return str(hash_md5.hexdigest())

def get_filename(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def turn_metadata(metadata):
    s = json.dumps(metadata)
    regex = r'(?<!:)"(\S*?)":'
    strip_s = re.sub(regex,'\\1:',s)
    return strip_s

def check_protoype(protoype, dictdata):
    if set(protoype) - set(dictdata):
        log.info({"your metadata should catains all protoype kyes: ": protoype})
        raise Exception({"your metadata should catains all protoype kyes: ": protoype})
    return True
