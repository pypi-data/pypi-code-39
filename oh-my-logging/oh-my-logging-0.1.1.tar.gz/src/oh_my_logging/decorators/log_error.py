#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from functools import wraps

from ..builders import LoggerBuilderFactory


class ErrorContext(object):
    """Documentation for ErrorContext

    """

    def __init__(
            self,
            logger,
            ignore_errors,
    ):
        super(ErrorContext, self).__init__()
        self.logger = logger
        self.ignore_errors = ignore_errors

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.logger.exception(value)
        
        if type in self.ignore_errors:
            return True
        else:
            return False


def log_error(*largs, **lkwargs):
    """
    @log_error(ignore_errors=(FileNotFoundException,))
    """

    # @log_error
    if len(largs) == 1 and callable(largs[0]) and len(lkwargs.items()) == 0:
        func = largs[0]
        logger = LoggerBuilderFactory().builder(func).build(logging.ERROR)
        if logger is None:
            return func
        
        @wraps(func)
        def proxy(*args, **kwargs):
            with ErrorContext(logger, tuple()) as ctx:
                return func(*args, **kwargs)

        return proxy
        
    # @log_error()
    ignore_errors = lkwargs.get('ignore_errors', tuple())

    def intermediate(func):
        logger = LoggerBuilderFactory().builder(func).build(logging.ERROR)
        if logger is None:
            return func

        @wraps(func)
        def proxy(*args, **kwargs):
            with ErrorContext(logger, ignore_errors) as ctx:
                return func(*args, **kwargs)

        return proxy

    return intermediate
