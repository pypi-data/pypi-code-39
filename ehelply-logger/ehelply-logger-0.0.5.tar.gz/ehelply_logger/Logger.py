from __future__ import annotations
import random
import string


class Logger:
    def __init__(self, prefix: str = None, debug_mode: int = 0):
        self.prefix: str = prefix
        self._chosen_prefix: bool = True
        if not self.prefix:
            self.prefix = self.random_chars(3)
            self._chosen_prefix: bool = False

        self.debug_mode: int = debug_mode

    def random_chars(self, length: int):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def _output(self, message: str):
        print(self.prefix + " " + message, flush=True)

    def info(self, message: str = ""):
        self._output("[INFO] " + str(message))

    def warning(self, message: str = ""):
        self._output("[WARNING] " + str(message))

    def severe(self, message: str = ""):
        self._output("[SEVERE] " + str(message))

    def newline(self):
        self._output("")

    def debug(self, message: str = "", force: bool = False):
<<<<<<< HEAD
        if self.debug_mode > 0 or force:
            self._output("[DEBUG] " + message)

    def debugg(self, message: str = "", force: bool = False):
        if self.debug_mode > 1 or force:
            self._output("[DEBUG] " + message)

    def debuggg(self, message: str = "", force: bool = False):
        if self.debug_mode > 2 or force:
            self._output("[DEBUG] " + message)
=======
        if self.debug_mode or force:
            self._output("[DEBUG] " + str(message))
>>>>>>> ffc702866f6160e6d5a507c482c59725605d084b

    def spinoff(self, prefix: str = None) -> Logger:
        if prefix:
            prefix = self.prefix + "-" + prefix
        else:
            prefix = self.prefix + "-" + self.random_chars(3)
        return Logger(prefix=prefix, debug_mode=self.debug_mode)
