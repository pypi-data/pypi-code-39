#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

class CustomLogger:
    def __init__(
        self,
        handler_name="CustomLogger",
        stream_handler=True,
        file_handler=False,
        level="INFO",
        filename=None,
        fmt="default",
    ):

        self.handler_name = handler_name
        self.stream_handler = stream_handler
        self.file_handler = file_handler
        self.level = level

        if filename is not None:
            if type(filename) == str:
                filename = [filename]
            if not isinstance(filename, list):
                raise ValueError("Filename must be string or list of string")

        self.filenames = filename

        self.fmt = CustomFormatter(
            "%(asctime)s %(splitted_name)-15s %(levelname)-8s %(message)s"
        )
        if fmt != "default":
            self.fmt = fmt

        self.logger = logging.getLogger(self.handler_name)

        self.set_level(self.level)

        if self.stream_handler:
            self.set_handlers("stream")

        if self.file_handler:

            if self.filenames == None:
                raise KeyError("filename cannot be None with file_handler at True!")

            self.set_handlers("file")

    def set_level(self, level, handler_name=None):

        if handler_name:
            if handler_name not in logging.root.manager.loggerDict:
                logging.getLogger(handler_name).setLevel(level)
                return

        for internal_logger in logging.root.manager.loggerDict:
            logging.getLogger(internal_logger).setLevel(level)

    def get_loggers(self):
        return logging.root.manager.loggerDict

    def set_handlers(self, handler):
        if handler == "file":
            for filename in self.filenames:
                h = logging.FileHandler(filename)
                h.setFormatter(self.fmt)
                logging.getLogger().handlers.append(h)
                # così si applicherebbe solo allo handler appena creato, senza propagarsi
                # self.logger.handlers.append(h)
        if handler == "stream":
            h = logging.StreamHandler()
            h.setFormatter(self.fmt)
            logging.getLogger().handlers.append(h)
            # così si applicherebbe solo allo handler appena creato, senza propagarsi
            # self.logger.handlers.append(h)

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
        self.logger.info("*"*20 + " Exiting... " + "*"*20)


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

        record.splitted_name = record.__dict__['name'].split(".")[-1]

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