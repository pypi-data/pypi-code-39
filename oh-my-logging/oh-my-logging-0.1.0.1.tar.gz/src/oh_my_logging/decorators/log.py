#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (unicode_literals,
                        print_function)
import logging
from functools import wraps
if 'reduce' not in vars():
    from functools import reduce

from .logger import logger
from .log_args import log_args
from .log_returning import log_returning
from .log_stat import log_stat
from .log_error import log_error


def log(*largs, **lkwargs):
    """
    Examples:
        1. Attach to function without arguments.
    >>> @log
        def func(logger):
            pass

        2. Log arguments passed to function, returning value, count the execution time and exceptions.
    >>> @log(log.ARGS, log.RETURNING, log.STAT, log.ERROR)
        def func():
            pass
        
        3. Log specific exceptions then ignore it.
    >>> @log({'target': log.ERROR, 'ignore_errors': (FileNotFoundException,)})
        def func():
            pass
    """

    # Inject logger object to function as the last parameter.
    if len(largs) == 1 and callable(largs[0]) and len(lkwargs.items()) == 0:
        return logger(largs[0])

    targets = [None] * 4
    for larg in largs:
        k = larg.get('target') if isinstance(larg, dict) else larg
        if isinstance(larg, dict):
            items = filter(lambda item: item[0] != 'target', larg.items())
            def reducing(accu, item):
                accu.setdefault(*item)
                return accu
            
            v = reduce(reducing, items, {})
        else:
            v = True
            
        targets[k] = v

        def intermediate(func):
            inner_proxy = func
            if targets[log.ARGS] is not None:
                inner_proxy = log_args(inner_proxy)

            if targets[log.RETURNING] is not None:
                inner_proxy = log_returning(inner_proxy)

            if targets[log.STAT] is not None:
                inner_proxy = log_stat(inner_proxy)

            if isinstance(targets[log.ERROR], dict):
                inner_proxy = log_error(**targets[log.ERROR])(inner_proxy)
            elif targets[log.ERROR] == True:
                inner_proxy = log_error(inner_proxy)

            return inner_proxy

    return intermediate


log.ARGS = 0
log.RETURNING = 1
log.STAT = 2
log.ERROR = 3
