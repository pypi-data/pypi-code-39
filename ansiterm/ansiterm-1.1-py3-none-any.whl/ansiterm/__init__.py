#!/usr/bin/env python3
#
# Change color and style (bold, reverse) of text on display
# Copyright (c) 2018-2019, Hiroyuki Ohsaki.
# All rights reserved.
#
# $Id: term.py,v 1.6 2018/10/24 04:45:02 ohsaki Exp $
#

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# SGR (Select Graphic Rendition) parameters
# https://en.wikipedia.org/wiki/ANSI_escape_code
SGR_PARAM = {
    'reset': 0,
    'bold': 1,
    'underline': 4,
    'reverse': 7,
    'gray': 90,
    'red': 91,
    'green': 92,
    'yellow': 93,
    'blue': 94,
    'magenta': 95,
    'cyan': 96,
    'white': 97,
}

# precompute escape sequences
SGR_SEQ = {}
for key, val in SGR_PARAM.items():
    SGR_SEQ[key] = '\x1b[{}m'.format(val)

def color(astr, name='bold', bold=False, reverse=False):
    """Embed ANSI escape sequences to change the text color to NAME.  Make the
    text boldface and reversed video if BOLD or REVERSE is True,
    respectively."""
    prefix = ''
    if reverse:
        prefix += SGR_SEQ['reverse']
    if bold:
        prefix += SGR_SEQ['bold']
    if name is not None:
        prefix += SGR_SEQ[name]
    return prefix + astr + SGR_SEQ['reset']

def reset(astr, bold=False, reverse=False):
    return color(astr, name='reset', bold=bold, reverse=reverse)

def bold(astr, bold=True, reverse=False):
    return color(astr, name=None, bold=bold, reverse=reverse)

def gray(astr, bold=False, reverse=False):
    return color(astr, name='gray', bold=bold, reverse=reverse)

def red(astr, bold=False, reverse=False):
    return color(astr, name='red', bold=bold, reverse=reverse)

def green(astr, bold=False, reverse=False):
    return color(astr, name='green', bold=bold, reverse=reverse)

def yellow(astr, bold=False, reverse=False):
    return color(astr, name='yellow', bold=bold, reverse=reverse)

def blue(astr, bold=False, reverse=False):
    return color(astr, name='blue', bold=bold, reverse=reverse)

def magenta(astr, bold=False, reverse=False):
    return color(astr, name='magenta', bold=bold, reverse=reverse)

def cyan(astr, bold=False, reverse=False):
    return color(astr, name='cyan', bold=bold, reverse=reverse)

def white(astr, bold=False, reverse=False):
    return color(astr, name='white', bold=bold, reverse=reverse)

def main():
    for bold in (False, True):
        for reverse in (False, True):
            for name in SGR_SEQ:
                astr = color(
                    'text in {} with bold={}, reverse={}'.format(
                        name, bold, reverse),
                    name,
                    bold=bold,
                    reverse=reverse)
                print(astr)

if __name__ == "__main__":
    main()
