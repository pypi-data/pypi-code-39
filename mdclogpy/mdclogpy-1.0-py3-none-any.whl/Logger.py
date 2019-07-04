# Copyright (c) 2019 AT&T Intellectual Property.
# Copyright (c) 2018-2019 Nokia.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Structured logging library with Mapped Diagnostic Context

Outputs the log entries to standard out in structured format, json currently.
Severity based filtering.
Supports Mapped Diagnostic Context (MDC).

Set MDC pairs are automatically added to log entries by the library.
"""
from typing import TypeVar
from enum import IntEnum
import sys
import json
import time


class Level(IntEnum):
    """Severity levels of the log messages."""
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40


LEVEL_STRINGS = {Level.DEBUG: "DEBUG",
                 Level.INFO: "INFO",
                 Level.WARNING: "WARNING",
                 Level.ERROR: "ERROR"}


Value = TypeVar('Value', str, int)


class Logger():
    """Initialize the mdclogging module.
    Calling of the function is optional. If not called, the process name
    (sys.argv[0]) is used by default.

    Keyword arguments:
    name -- name of the component. The name will appear as part of the log
            entries.
    """
    def __init__(self, name: str = sys.argv[0], level: Level = Level.DEBUG):
        """Initialize a Logger instance.

            Keyword arguments:
            name -- name of the component. The name will appear as part of the
                    log entries.
        """
        self.procname = name
        self.current_level = level
        self.mdc = {}

    def _output_log(self, log: str):
        """Output the log, currently to stdout."""
        print(log)

    def log(self, level: Level, message: str):
        """Log a message.

        Logs the message with the given severity if it is equal or higher than
        the current logging level.

        Keyword arguments:
        level -- severity of the log message
        message -- log message
        """
        if level >= self.current_level:
            log_entry = {}
            log_entry["ts"] = int(round(time.time() * 1000))
            log_entry["crit"] = LEVEL_STRINGS[level]
            log_entry["id"] = self.procname
            log_entry["mdc"] = self.mdc
            log_entry["msg"] = message
            self._output_log(json.dumps(log_entry))

    def error(self, message: str):
        """Log an error message. Equals to log(ERROR, msg)."""
        self.log(Level.ERROR, message)

    def warning(self, message: str):
        """Log a warning message. Equals to log(WARNING, msg)."""
        self.log(Level.WARNING, message)

    def info(self, message: str):
        """Log an info message. Equals to log(INFO, msg)."""
        self.log(Level.INFO, message)

    def debug(self, message: str):
        """Log a debug message. Equals to log(DEBUG, msg)."""
        self.log(Level.DEBUG, message)

    def set_level(self, level: Level):
        """Set current logging level.

        Keyword arguments:
        level -- logging level. Log messages with lower severity will be
                 filtered.
        """
        if level in Level:
            self.current_level = level

    def get_level(self) -> Level:
        """Return the current logging level."""
        return self.current_level

    def add_mdc(self, key: str, value: Value):
        """Add a logger specific MDC.

        If an MDC with the given key exists, it is replaced with the new one.
        An MDC can be removed with remove_mdc() or clean_mdc().

        Keyword arguments:
        key -- MDC key
        value -- MDC value
        """
        self.mdc[key] = value

    def get_mdc(self, key: str) -> Value:
        """Return logger's MDC value with the given key or None."""
        try:
            return self.mdc[key]
        except KeyError:
            return None

    def remove_mdc(self, key: str):
        """Remove logger's MDC with the given key."""
        try:
            del self.mdc[key]
        except KeyError:
            pass

    def clean_mdc(self):
        """Remove all MDCs of the logger instance."""
        self.mdc = {}
