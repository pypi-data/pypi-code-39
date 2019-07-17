#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""lazy_methods.py

Concentrate day to day methods for the lazy coder that uses it so often he
feels it is clearer / less error prone to have a specific function for the
task.

WARNING : it is **not** OK to put anything you found on the web here:
    - methods can be included in this module if they **improve** the
      readability of the rest of the code, **not** if they contribute to
      obfuscate it
    - they must be **widely used** throughout OpenTea.

Created Dec 2016 by COOP team
"""



import sys
import logging
import fileinput

__all__ = ["pairwise",
           "currentnext",
           "replace_pattern_in_file"]
logger = logging.getLogger(__name__)


def pairwise(iterable):
    """
    This procedure allows to loop in a list in a pairwise fashion
    s -> (s0,s1), (s2,s3), (s4, s5), ...
    """
    return list(zip(iterable[::2], iterable[1::2]))
    # NOTE : the following is possibly a more "universal" method
    # However, it has a (arguably useless) dependancy to itertools, and it is
    # pretty obscure for beginners...
    #    from itertools import izip
    #    a = iter(iterable)
    #    return izip(a, a)


def replace_pattern_in_file(path, search_exp, replace_exp):
    """Search and replace a pattern in a file"""
    # NOTE : the use of fileinput is dark magic.  This is however an efficient
    # method in terms of lines of code.  For more on this, see e.g. :
    # http://stackoverflow.com/questions/39086
    replace = 0
    for line in fileinput.input(path, inplace=True):
        if search_exp in line:
            line = line.replace(search_exp, replace_exp)
            replace += 1
        sys.stdout.write(line)

    logger.debug("{0} replacement(s) made".format(replace))
    logger.debug("{0} : {1} > {2}".format(path, search_exp, replace_exp))


def currentnext(iterable):
    """loop over an iterables using current/Next pairs
    return a list of iterables
    """
    from itertools import islice
    new_iterable = []
    for current_item, next_item in zip(iterable, islice(iterable, 1, None)):
        new_iterable.append([current_item, next_item])

    return new_iterable
