from __future__ import annotations
import random
import string
from ehelply_logger.LogFormatter import LogFormatter


class Logger:
    def __init__(self, prefix: str = None, debug_mode: int = 0, log_formatter: LogFormatter = None):
        self.prefix: str = prefix
        if not self.prefix:
            self.prefix = self.random_chars(3)

        self.debug_mode: int = debug_mode

        self.log_formatter = log_formatter
        if not self.log_formatter:
            self.log_formatter: LogFormatter = LogFormatter()

    def random_chars(self, length: int):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def _output(self, message: str, severity: str):
        print(self.log_formatter.format(text=message, severity=severity, prefix=self.prefix), flush=True)

    def info(self, message: str = ""):
        self._output(str(message), "info")

    def warning(self, message: str = ""):
        self._output(str(message), "warning")

    def severe(self, message: str = ""):
        self._output(str(message), "severe")

    def newline(self):
        self._output("", "")

    def debug(self, message: str = "", force: bool = False):
        if self.debug_mode > 0 or force:
            self._output(str(message), "debug")

    def debugg(self, message: str = "", force: bool = False):
        if self.debug_mode > 1 or force:
            self._output(str(message), "debug")

    def debuggg(self, message: str = "", force: bool = False):
        if self.debug_mode > 2 or force:
            self._output(str(message), "debug")

    def spinoff(self, prefix: str = None) -> Logger:
        if prefix:
            prefix = self.prefix + "-" + prefix
        else:
            prefix = self.prefix + "-" + self.random_chars(3)
        return Logger(prefix=prefix, debug_mode=self.debug_mode)
