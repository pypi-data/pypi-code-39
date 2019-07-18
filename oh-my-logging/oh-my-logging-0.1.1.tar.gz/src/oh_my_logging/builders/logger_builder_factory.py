#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Lock
import logging.config
import json

from .str_logger_builder import StrLoggerBuilder
from .function_logger_builder import FunctionLoggerBuilder
from .type_logger_builder import TypeLoggerBuilder


class LoggerBuilderFactory(object):
    """Documentation for LoggerBuilderFactory

    """

    __instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls.__instance is not None:
            return cls.__instance

        cls._lock.acquire()
        try:
            if cls.__instance is not None:
                return cls.__instance

            return super().__new__(cls)
        finally:
            cls._lock.release()

    def __init__(self, config=None):
        if self.__class__.__instance is None:
            self.__class__.__instance = self
        else:
            return

        dictConfig = None
        if config is None:
            # Default config.
            logging.config.fileConfig('logging.ini')
        elif isinstance(config, str):
            if clonfig.endswith('.ini'):
                logging.config.fileConfig(config)
            else:
                if config.endswith('.json') or config.endswith('.js'):
                    with open(config, encoding='utf-8') as f:
                        dictConfig = json.load(f)
                elif config.endswith('.yml') or config.endswith('.yaml'):
                    import yaml
                    with open(config, encoding='utf-8') as f:
                        dictConfig = yaml.load(f)
        elif isinstance(config, dict):
            dictConfig = config

        if dictConfig != None:
            logging.config.dictConfig(dictConfig)

    @classmethod
    def unsafe_clear(cls, ):
        cls._lock.acquire()        
        cls.__instance = None
        cls._lock.release()

    def builder(
            self,
            logger_name,
    ):
        """
        Create logger builder by logger name.
        
        Args:
            logger_name(str|function|type): logger name

        Returns:
            LoggerBuilder
        """

        if isinstance(logger_name, str):
            return StrLoggerBuilder(logger_name)
        elif callable(logger_name):
            return FunctionLoggerBuilder(logger_name)
        elif isinstance(logger_name, type):
            return TypeLoggerBuilder(logger_name)
        else:
            raise TypeError()
