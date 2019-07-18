import contextlib
import os
import sys


def get_base_file_name(file_path):
    base = os.path.basename(file_path)
    base_file_name, ext = os.path.splitext(base)
    return base_file_name


@contextlib.contextmanager
def smart_open_write(filename=None):
    if filename and filename != '-':
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        fh = open(filename, 'w')
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()


def replace_dash(value, replacement):
    return replacement if value == '-' else value
