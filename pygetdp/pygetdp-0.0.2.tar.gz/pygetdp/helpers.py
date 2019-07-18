# -*- coding: utf-8 -*-
#
from __future__ import print_function

import os
import shutil
import subprocess
import tempfile
import textwrap
import tokenize
from glob import glob
from io import StringIO

import matplotlib.pyplot as plt
import numpy
from sphinx_gallery.scrapers import figure_rst

from .rendering import render


def make_png(code, filename="tmp"):
    with open(filename, "w") as f:
        f.write(code)
    render(filename, "{}.png".format(filename))


def show_png(filename="tmp"):
    image = plt.imread("{}.png".format(filename))
    plt.imshow(image)
    plt.axis("off")
    plt.tight_layout()


def build_example_png(code, filename="tmp"):
    make_png(code, filename=filename)
    show_png(filename=filename)


class PNGScraper(object):
    def __init__(self):
        self.seen = set()

    def __repr__(self):
        return "PNGScraper"

    def __call__(self, block, block_vars, gallery_conf):
        path_current_example = os.path.dirname(block_vars["src_file"])
        pngs = sorted(glob(os.path.join(os.getcwd(), "*.png")))
        image_names = list()
        image_path_iterator = block_vars["image_path_iterator"]
        for png in pngs:
            if png not in seen:
                seen |= set(png)
                this_image_path = image_path_iterator.next()
                image_names.append(this_image_path)
                shutil.move(png, this_image_path)
        rst_ = figure_rst(image_names, gallery_conf["src_dir"])
        print(rst_)
        return rst_


def _add_raw_code(s, raw_code, newline=True):
    if newline:
        nl = "\n"
    else:
        nl = ""
    s += nl + raw_code
    return s


def _comment(s, style="short", newline=False):
    if newline:
        nl = "\n"
    else:
        nl = ""
    if style is "short":
        if len(s) > 80:
            s = "\n".join(textwrap.wrap(s))
            return _comment(s, style="long", newline=newline)
        else:
            return nl + r"// " + s
    elif style is "long":
        return nl + r"/*  " + s + r" */"


def _is_string(obj):
    return isinstance(obj, str)


def _is_list(obj):
    return isinstance(obj, list)


def _is_complex(obj):
    return isinstance(obj, complex)


def _get_getdp_exe():
    macos_getdp_location = "/Applications/Getdp.app/Contents/MacOS/getdp"
    return macos_getdp_location if os.path.isfile(macos_getdp_location) else "getdp"


#
# def py2getdplist(l):
#     return "{" + ",".join([str(_) for _ in l]) + "}"
#


def get_getdp_major_version(getdp_exe=_get_getdp_exe()):
    out = (
        subprocess.check_output([getdp_exe, "--version"], stderr=subprocess.STDOUT)
        .strip()
        .decode("utf8")
    )
    ex = out.split(".")
    return int(ex[0])


def make_args(glist, sep=","):
    sep = sep + " "
    if isinstance(glist, list):
        if len(glist) == 1:
            glist = str(glist[0])
        else:
            glist = sep.join([str(g) for g in glist])
            glist = "{" + glist + "}"
    return str(glist)


def replace_formula(str_in, to_replace, replacement):
    tok = [
        token[1]
        for token in tokenize.generate_tokens(StringIO(str_in).readline)
        if token[1]
    ]

    for rold, rnew in zip(to_replace, replacement):
        for i, t in enumerate(tok):
            if t == rold:
                tok[i] = rnew
    return "".join(tok)
