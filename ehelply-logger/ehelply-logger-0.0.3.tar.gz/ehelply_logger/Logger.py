from __future__ import annotations
import random
import string


class Logger:
    def __init__(self, prefix: str = None, debug_mode: bool = False):
        self.prefix: str = prefix
        self._chosen_prefix: bool = True
        if not self.prefix:
            self.prefix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
            self._chosen_prefix: bool = False

        self.debug_mode: bool = debug_mode

    def _output(self, message: str):
        print(self.prefix + " " + message, flush=True)

    def info(self, message: str = ""):
        self._output("[INFO] " + message)

    def warning(self, message: str = ""):
        self._output("[WARNING] " + message)

    def severe(self, message: str = ""):
        self._output("[SEVERE] " + message)

    def newline(self):
        self._output("")

    def debug(self, message: str = "", force: bool = False):
        if self.debug_mode or force:
            self._output("[DEBUG] " + message)

    def spinoff(self) -> Logger:
        prefix = None
        if self._chosen_prefix:
            prefix = self.prefix + "!"
        return Logger(prefix=prefix, debug_mode=self.debug_mode)
