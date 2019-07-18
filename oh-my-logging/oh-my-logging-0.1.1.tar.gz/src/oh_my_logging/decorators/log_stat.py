#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import time
from functools import wraps

from ..builders import LoggerBuilderFactory


def log_stat(func):
    """
    Count the execution time cost of specific function.
    
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
        start_time = time.clock()
        try:
            return func(*args, **kwargs)
        finally:
            end_time = time.clock()
            cost = (end_time - start_time)*1000
            # Try to add attribute `__log_stat` to the proxy func for storing the latest statistic milliseconds.
            proxy.__log_stat = cost
            
            logger.debug(log_stat.__TEMPLATE, cost)

    return proxy

log_stat.__TEMPLATE = 'statistic: %fms'
