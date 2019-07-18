#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from functools import wraps

from ..builders import LoggerBuilderFactory


def log_args(func):
    """
    Log arguments of function.
    
    Args:
        func(callable): The original function which be decorated.

    Returns:
        function(..., logger: Logger): Proxy function.
    """

    logger = LoggerBuilderFactory().builder(func).build()
    if logger is None:
        return func

    @wraps(func)
    def proxy(*args, **kwargs):
        arg_list = map(lambda nv: '{}={}'.format(nv[0], nv[1]),
                       zip(func.__code__.co_varnames, args))
        logger.debug(log_args.__TEMPLATE, ', '.join(arg_list))

        return func(*args, **kwargs)

    return proxy

log_args.__TEMPLATE = 'params: %s'
