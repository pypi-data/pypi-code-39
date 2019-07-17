# coding: utf-8

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Optional, Any

from flask import Flask

LOG_FILE_MAX_BYTES = 100 * 1024 * 1024
LOG_FILE_BACKUP_COUNT = 10
LOG_FORMATTER = logging.Formatter('%(asctime)s!%(levelname)s!%(process)d!%(thread)d!'
                                  '%(pathname)s!%(lineno)s!%(message)s!')


class InfoFilter(logging.Filter):
    def filter(self, record: Any) -> int:
        """
        筛选, 只需要 INFO 级别以上log
        :param record:
        """
        if logging.INFO <= record.levelno < logging.ERROR:
            return super(InfoFilter, self).filter(record)
        else:
            return 0


class Log(object):

    def __init__(self, app: Flask, app_name: str, error_path: str = None, info_path: str = None,
                 file_max_bytes: int = LOG_FILE_MAX_BYTES,
                 file_backup_count: int = LOG_FILE_BACKUP_COUNT, formatter_info: logging.Formatter = LOG_FORMATTER,
                 formatter_error: logging.Formatter = LOG_FORMATTER):
        self.app = app
        self.app_name = app_name
        self._log_path_error = error_path or f'/var/log/{self.app_name}/error'
        self._log_path_info = info_path or f'/var/log/{self.app_name}/info'
        if not os.path.exists(self._log_path_error):
            os.makedirs(self._log_path_error)
        if not os.path.exists(self._log_path_info):
            os.makedirs(self._log_path_info)
        self.log_path_error = os.path.join(self._log_path_info, f'{self.app_name}.error.log')
        self.log_path_info = os.path.join(self._log_path_info, f'{self.app_name}.info.log')
        self.log_file_max_bytes = file_max_bytes
        self.log_file_backup_count = file_backup_count
        self.log_formatter_info = formatter_info
        self.log_formatter_error = formatter_error
        self.filter_info = InfoFilter()
        self.level_info = logging.INFO
        self.level_error = logging.ERROR
        self._handler_file_info: Optional[RotatingFileHandler] = None
        self._handler_file_error: Optional[RotatingFileHandler] = None
        self._handler_screen_info: Optional[logging.StreamHandler] = None
        self._handler_screen_error: Optional[logging.StreamHandler] = None
        self.app.logger.addHandler(self.handler_file_info)
        self.app.logger.addHandler(self.handler_file_error)
        # self.app.logger.addHandler(self.handler_screen_info)
        # self.app.logger.addHandler(self.handler_screen_error)
        self.app.logger.setLevel(self.level_info)

    @property
    def handler_file_info(self) -> Optional[RotatingFileHandler]:
        if not self._handler_file_info:
            file_handler_info = RotatingFileHandler(filename=self.log_path_info)
            file_handler_info.setFormatter(self.log_formatter_info)
            file_handler_info.setLevel(self.level_info)
            file_handler_info.addFilter(self.filter_info)
            self._handler_file_info = file_handler_info
        return self._handler_file_info

    @property
    def handler_file_error(self) -> Optional[RotatingFileHandler]:
        if not self._handler_file_error:
            file_handler_error = RotatingFileHandler(filename=self.log_path_error)
            file_handler_error.setFormatter(self.log_formatter_error)
            file_handler_error.setLevel(logging.ERROR)
            self._handler_file_error = file_handler_error
        return self._handler_file_error

    @property
    def handler_screen_info(self) -> Optional[logging.StreamHandler]:
        if not self._handler_screen_info:
            self._handler_screen_info = logging.StreamHandler(sys.stdout)
            # log_filter = LogFilter(logging.NOTSET)
            # self._handler_screen_info.addFilter(log_filter)
            self._handler_screen_info.setFormatter(self.log_formatter_info)
            self._handler_screen_info.setLevel(logging.DEBUG)
        return self._handler_screen_info

    @property
    def handler_screen_error(self) -> Optional[logging.StreamHandler]:
        if not self._handler_screen_error:
            self._handler_screen_error = logging.StreamHandler(sys.stderr)
            self._handler_screen_error.setLevel(logging.DEBUG)
            self._handler_screen_error.setFormatter(self.log_formatter_error)
        return self._handler_screen_error
