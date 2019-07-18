#!/usr/bin/env python
import os
import subprocess
import sys
import tempfile

from pygments import highlight
from pygments.formatters import Terminal256Formatter

from .prolexer import CustomLexer
from .prostyle import ProStyle


def render(pro_filename, out_filename=None):
    if os.path.isfile(pro_filename):
        cmd = "pygmentize -O full,line_numbers=False,style=prostyle,font_size=32 -l pro"
        if out_filename:
            cmd += " -o {}".format(out_filename)
        cmd += " {}".format(pro_filename)
        os.system(cmd)
    else:
        formatter = Terminal256Formatter(style=ProStyle)
        print(highlight(pro_filename, CustomLexer(), formatter))
