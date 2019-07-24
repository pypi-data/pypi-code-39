import re
import datetime

WHITE = '\033[97m'
CYAN = '\033[96m'
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


class LogFormatter:
    def format(self, text: str = "", severity: str = "", prefix: str = "") -> str:
        # Timestamp, Severity, prefix, message
        if not self.do_colors():
            text = self.strip_color(text)

        meta = ""
        if self.do_timestamps():
            meta += str(datetime.datetime.now().isoformat()) + " "

        if self.do_severity() and len(severity) > 0:
            meta += "{:9} ".format("[" + severity.upper() + "]")

        if self.do_prefix() and len(prefix) > 0:
            meta += prefix + ": "

        if self.do_colors():
            return WHITE + meta + text + ENDC
        return meta + text

    def do_timestamps(self) -> bool:
        return False

    def do_colors(self) -> bool:
        return False

    def do_prefix(self) -> bool:
        return True

    def do_severity(self) -> bool:
        return True

    def strip_color(self, text):
        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', text)
