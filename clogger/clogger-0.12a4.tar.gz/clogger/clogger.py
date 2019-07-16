#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging


class CustomLogger:

    log_format = "%(asctime)s %(splitted_name)-15s %(levelname)-8s %(message)s"

    def __init__(
        self,
        handler_name="CustomLogger",
        level="INFO",
        stream_handler=True,
        file_handler=False,
        filenames=None,
    ):

        self.formatter = CustomFormatter(self.log_format)

        self.handler_name = handler_name
        self.logger = logging.getLogger(self.handler_name)

        self.level = level
        self.stream_handler = stream_handler
        self.filenames = filenames
        self.file_handler = file_handler

        self.change_level(self.level)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        if not isinstance(value, str):
            raise ValueError("level must be an instance of string")
        if value not in ["DEBUG", "INFO", "WARNING", "ERROR"]:
            raise ValueError("level must be one of DEBUG, INFO, WARNING, ERROR")
        self._level = value

    @property
    def file_handler(self):
        return self._file_handler

    @file_handler.setter
    def file_handler(self, value):
        if isinstance(value, bool):
            if value and not self.filenames:
                raise ValueError("filename(s) cannot be None if file_handler is True!")
            self._file_handler = value
            self.add_handler("file")
        else:
            raise ValueError("file_handler must be an instance of bool")

    @property
    def stream_handler(self):
        return self._stream_handler

    @stream_handler.setter
    def stream_handler(self, value):
        if isinstance(value, bool):
            self._stream_handler = value
            self.add_handler("stream")
        else:
            raise ValueError("stream_handler must be an instance of bool")

    @property
    def filenames(self):
        return self._filenames

    @filenames.setter
    def filenames(self, value):
        if value is None:
            self._filenames = None

        elif type(value) == str:
            self._filenames = [value]

        elif isinstance(value, list):
            self._filenames = value
        else:
            raise ValueError(
                "Filename(s) must be an instance of string or list of string"
            )

    @property
    def handler_name(self):
        return self._handler_name

    @handler_name.setter
    def handler_name(self, value):
        if not isinstance(value, str):
            raise ValueError("handler_name must be an instance of string")
        self._handler_name = value

    def add_handler(self, handler):
        if handler == "file":
            for filename in self.filenames:
                h = logging.FileHandler(filename)
                h.setFormatter(self.formatter)
                logging.getLogger().handlers.append(h)
        if handler == "stream":
            h = logging.StreamHandler()
            h.setFormatter(self.formatter)
            logging.getLogger().handlers.append(h)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def exception(self, msg):
        self.logger.exception(msg)

    def starting_message(self):
        self.logger.info("*" * 20 + " Starting... " + "*" * 20)

    def exiting_message(self):
        self.logger.info("*" * 20 + " Exiting... " + "*" * 20)

    @staticmethod
    def change_level(level, handler_name=None):
        if handler_name:
            if handler_name not in logging.root.manager.loggerDict:
                logging.getLogger(handler_name).setLevel(level)
                return
        for internal_logger in logging.root.manager.loggerDict:
            logging.getLogger(internal_logger).setLevel(level)

    @staticmethod
    def get_loggers():
        return logging.root.manager.loggerDict


class CustomFormatter(logging.Formatter):
    def format(self, record):
        """
        Format the specified record as text.

        The record's attribute dictionary is used as the operand to a
        string formatting operation which yields the returned string.
        Before formatting the dictionary, a couple of preparatory steps
        are carried out. The message attribute of the record is computed
        using LogRecord.getMessage(). If the formatting string uses the
        time (as determined by a call to usesTime(), formatTime() is
        called to format the event time. If there is exception information,
        it is formatted using formatException() and appended to the message.
        """

        record.splitted_name = record.__dict__["name"].split(".")[-1]

        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        return s
