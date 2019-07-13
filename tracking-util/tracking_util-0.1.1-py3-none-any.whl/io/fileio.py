#!/usr/bin/env python
import shutil
import os


def copy_or_link(src, dst):
    """
    copy file, or copy symlink
    """
    # if dst is a dir, then use the same name
    src = os.path.abspath(src)
    if os.path.isdir(dst):
        fn = src.split('/')[-1]
        dst = os.path.join(dst, fn)

    if os.path.islink(src):
        linkto = os.readlink(src)
        os.symlink(linkto, dst)
    else:
        shutil.copy(src, dst)


def link(src, dst):
    """
    link file, or copy symlink
    """
    # if dst is a dir, then use the same name

    src = os.path.abspath(src)
    if os.path.isdir(dst):
        fn = src.split('/')[-1]
        dst = os.path.join(dst, fn)

    if os.path.islink(src):
        linkto = os.readlink(src)
        os.symlink(linkto, dst)
    else:
        os.symlink(src, dst)
        # shutil.copy(src, dst)
