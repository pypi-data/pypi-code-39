#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from functools import wraps

from ..builders import LoggerBuilderFactory


def log_returning(func):
    """
    Log retuning value of function.
    
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
        ret = func(*args, **kwargs)
        logger.debug(log_returning.__TEMPLATE, repr(ret))

        return ret

    return proxy

log_returning.__TEMPLATE = 'returning: %s'
