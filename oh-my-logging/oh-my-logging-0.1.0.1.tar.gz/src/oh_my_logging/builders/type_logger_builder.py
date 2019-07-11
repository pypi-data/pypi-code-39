#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .logger_builder import LoggerBuilder


class TypeLoggerBuilder(LoggerBuilder):
    """Documentation for TypeLoggerBuilder

    """
    def __init__(self, cls):
        name = '{}.{}'.format(cls.__module__, cls.__name__)
        super(TypeLoggerBuilder, self).__init__(name)
