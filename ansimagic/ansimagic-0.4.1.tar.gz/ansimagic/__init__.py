from enum import Enum, unique
from ansimagic.presets import Presets

__version__ = '0.4.1'


@unique
class Colors(Enum):
    BLACK = 0
    BRIGHT_BLACK = 1
    RED = 2
    BRIGHT_RED = 3
    GREEN = 4
    BRIGHT_GREEN = 5
    YELLOW = 6
    BRIGHT_YELLOW = 7
    BLUE = 8
    BRIGHT_BLUE = 9
    MAGENTA = 10
    BRIGHT_MAGENTA = 11
    CYAN = 12
    BRIGHT_CYAN = 13
    WHITE = 14
    BRIGHT_WHITE = 15


@unique
class Styles(Enum):
    RESET = 0
    BOLD = 1
    FAINT = 2
    ITALIC = 3
    UNDERLINE = 4
    REVERSE = 5
    CROSSED_OUT = 6


@unique
class ClearModes(Enum):
    TO_END = 0
    TO_BEGINNING = 1
    ENTIRE = 2


@unique
class ColorModes(Enum):
    COLORS_8 = 0
    COLORS_256 = 1
    TRUECOLOR = 2


presets = Presets()


@unique
class CSI(Enum):
    CURSOR_UP = 'A'  # CUU
    CURSOR_DOWN = 'B'  # CUD
    CURSOR_FORWARD = 'C'  # CUF
    CURSOR_BACK = 'D'  # CUB
    CURSOR_NEXT_LINE = 'E'  # CNL
    CURSOR_PREVIOUS_LINE = 'F'  # CPL

    CURSOR_HORIZONTAL_ABSOLUTE = 'G'  # CHA
    CURSOR_POSITION = 'H'  # CUP

    ERASE_DATA = 'J'  # ED
    ERASE_IN_LINE = 'K'  # EL

    SCROLL_UP = 'S'  # SU
    SCROLL_DOWN = 'T'  # SD

    SELECT_GRAPHIC_RENDITION = 'm'  # SGR

    SAVE_CURSOR_POSITION = 's'  # CSP
    RESTORE_CURSOR_POSITION = 'u'  # RCP

    CURSOR_HIDE = '?25l'
    CURSOR_SHOW = '?25h'


@unique
class SGR(Enum):
    RESET = 0
    # text decorators
    BOLD = 1
    FAINT = 2
    ITALIC = 3
    UNDERLINE = 4
    REVERSE = 7
    CROSSED_OUT = 9
    # foreground colors
    FOREGROUND_BLACK = 30
    FOREGROUND_RED = 31
    FOREGROUND_GREEN = 32
    FOREGROUND_YELLOW = 33
    FOREGROUND_BLUE = 34
    FOREGROUND_MAGENTA = 35
    FOREGROUND_CYAN = 36
    FOREGROUND_WHITE = 37
    FOREGROUND_COLOR = 38
    # background colors
    BACKGROUND_BLACK = 40
    BACKGROUND_RED = 41
    BACKGROUND_GREEN = 42
    BACKGROUND_YELLOW = 43
    BACKGROUND_BLUE = 44
    BACKGROUND_MAGENTA = 45
    BACKGROUND_CYAN = 46
    BACKGROUND_WHITE = 47
    BACKGROUND_COLOR = 48


@unique
class SGR_COLORS(Enum):
    COLORS_256 = 5
    TRUECOLOR = 2
