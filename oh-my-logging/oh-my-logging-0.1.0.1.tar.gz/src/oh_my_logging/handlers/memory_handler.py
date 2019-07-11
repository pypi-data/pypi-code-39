#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging


class MemoryHandler(logging.Handler):
    """Documentation for MemoryHandler

    """

    message = None

    def __init__(self, ):
        super(MemoryHandler, self).__init__()

    def emit(self, record):
        self.message = self.format(record)
