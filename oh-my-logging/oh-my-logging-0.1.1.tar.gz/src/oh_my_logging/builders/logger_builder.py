#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging


class LoggerBuilder(object):
    """Documentation for LoggerBuilder

    """

    @property
    def name(self, ):
        return self.__name

    def __init__(self, name):
        super(LoggerBuilder, self).__init__()
        self.__name = name

    def build(self, level=logging.DEBUG):
        """
        Get a Logger instance if the logger is enabled for specific level.
        
        Args:
            level(int): Level of log. The logging.[DEBUG|INFO|WARN|ERROR|CRITICAL] are valid value. logging.DEBUG as default.

        Returns:
            logging.Logger|None: Return None if there was no Logger instance satisfies the specific level.
        """
        logger = logging.getLogger(self.__name)
        
        if logger.isEnabledFor(level):
            return logger
