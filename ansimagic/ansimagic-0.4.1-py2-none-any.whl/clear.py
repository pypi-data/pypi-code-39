from ansimagic import ClearModes, CSI
from tools import compose_sequence


def clear(in_line=False, mode=ClearModes.ENTIRE, printable=True):
    sequence = compose_sequence(CSI.ERASE_DATA, mode, printable=printable)
    if in_line:
        sequence = compose_sequence(CSI.ERASE_IN_LINE, mode, printable=printable)

    return sequence


def screen(mode=ClearModes.ENTIRE, printable=True):
    return clear(False, mode, printable)


def line(mode=ClearModes.ENTIRE, printable=True):
    return clear(True, mode, printable)
