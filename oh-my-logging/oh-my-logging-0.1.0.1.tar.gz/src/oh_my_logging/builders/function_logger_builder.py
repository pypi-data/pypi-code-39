#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .logger_builder import LoggerBuilder


class FunctionLoggerBuilder(LoggerBuilder):
    """Documentation for FunctionLoggerBuilder

    """

    def __init__(self, func):
        name = '{}.{}'.format(func.__module__,
                              func.__qualname__)
        super(FunctionLoggerBuilder, self).__init__(name)
