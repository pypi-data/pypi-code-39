from ansimagic import CSI
from ansimagic.tools import compose_sequence


def up(step=1, printable=True):
    return compose_sequence(CSI.CURSOR_UP, step, printable=printable)


def down(step=1, printable=True):
    return compose_sequence(CSI.CURSOR_DOWN, step, printable=printable)


def right(step=1, printable=True):
    return compose_sequence(CSI.CURSOR_FORWARD, step, printable=printable)


def forward(step=1, printable=True):
    return right(step, printable=printable)


def left(step=1, printable=True):
    return compose_sequence(CSI.CURSOR_BACK, step, printable=printable)


def back(step=1, printable=True):
    return left(step, printable=printable)


def to(x, y=None, printable=True):
    sequence = compose_sequence(CSI.CURSOR_HORIZONTAL_ABSOLUTE, x, printable=printable)
    if y:
        sequence = compose_sequence(CSI.CURSOR_POSITION, x, y, printable=printable)

    return sequence


def next_line(step=1, printable=True):
    sequence = compose_sequence(CSI.CURSOR_NEXT_LINE, step, printable=printable)

    return sequence


def prev_line(step=1, printable=True):
    sequence = compose_sequence(CSI.CURSOR_PREVIOUS_LINE, step, printable=printable)

    return sequence


def scroll(step=1, is_up=False, printable=True):
    sequence = compose_sequence(CSI.SCROLL_DOWN, step, printable=printable)
    if is_up:
        sequence = compose_sequence(CSI.SCROLL_UP, step, printable=printable)

    return sequence


def hide(printable=True):
    return compose_sequence(CSI.CURSOR_HIDE, printable=printable)


def show(printable=True):
    return compose_sequence(CSI.CURSOR_SHOW, printable=printable)
