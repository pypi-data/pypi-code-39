#!/usr/bin/env python
import os
import sys
import subprocess
import tempfile
from pygments import highlight
from .prostyle import ProStyle
from .prolexer import CustomLexer
from pygments.formatters import Terminal256Formatter


def render(pro_filename, out_filename=None):
    if os.path.isfile(pro_filename):
        cmd = "pygmentize -O full,font_name=UbuntuMono,line_numbers=False,style=prostyle,font_size=32 -l pro"
        if out_filename:
            cmd += " -o {}".format(out_filename)
        cmd += " {}".format(pro_filename)
        os.system(cmd)
    else:
        formatter = Terminal256Formatter(style=ProStyle)
        print(highlight(pro_filename, CustomLexer(), formatter))
