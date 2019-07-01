from ansimagic import ColorModes, CSI, SGR
from ansimagic.tools import compose_sequence, make_brush


# RESET
def reset():
    return compose_sequence(CSI.SELECT_GRAPHIC_RENDITION, SGR.RESET)


# FOREGROUND COLORS
def color(color, text=None, autoreset=True, mode=ColorModes.COLORS_8):

    sequence = make_brush(color, mode, is_background=False)

    if text:
        sequence += text
        sequence += reset() if autoreset else ''

    return sequence


# BACKGROUND COLORS
def on(color, text=None, autoreset=True, mode=ColorModes.COLORS_8):

    sequence = make_brush(color, mode, is_background=True)

    if text:
        sequence += text
        sequence += reset() if autoreset else ''

    return sequence


# DECORATORS
def style(styles, text=None, autoreset=True):
    if not isinstance(styles, list):
        styles = [styles]

    sgr = CSI.SELECT_GRAPHIC_RENDITION
    styles_list = [compose_sequence(sgr, SGR[s.name], printable=False) for s in styles]
    sequence = ''.join(styles_list)

    if text:
        sequence += text
        sequence += reset() if autoreset else ''

    return sequence
