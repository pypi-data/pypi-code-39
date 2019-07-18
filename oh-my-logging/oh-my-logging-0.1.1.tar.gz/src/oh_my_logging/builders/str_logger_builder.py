#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .logger_builder import LoggerBuilder


class StrLoggerBuilder(LoggerBuilder):
    """Documentation for StrLoggerBuilder

    """

    def __init__(self, name):
        super(StrLoggerBuilder, self).__init__(name)
