#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from functools import wraps

from ..builders import LoggerBuilderFactory

def logger(func):
    """
    Inject logger object to function as the last parameter.
    
    Args:
        func(callable): The original function which be decorated.

    Returns:
        function(..., logger: Logger): Proxy function.
    """

    logger = LoggerBuilderFactory().builder(func).build(logging.CRITICAL)
    
    @wraps(func)
    def proxy(*args, **kwargs):
        args += (logger,)
        return func(*args, **kwargs)

    return proxy
