from ansimagic import ColorModes, Colors, CSI, SGR, SGR_COLORS


def compose_sequence(introducer, *codes, **options):
    escape = '\u001b'

    if not isinstance(introducer, int):
        introducer = introducer.value

    codes = [str(c.value) if not isinstance(c, int) else str(c) for c in codes]
    codes_seq = ';'.join(codes)
    sequence = '{}[{}{}'.format(escape, codes_seq, introducer)

    if 'printable' in options and options['printable'] is True:
        print(sequence, end='')

    return sequence


def make_brush(color, mode, is_background):
    codes = []

    color_type = SGR.BACKGROUND_COLOR if is_background else SGR.FOREGROUND_COLOR
    color_prefix = 'BACKGROUND' if is_background else 'FOREGROUND'

    # 3/4 bits
    if mode == ColorModes.COLORS_8:
        bright = False
        if '_' in color.name:
            bright = True
            color = Colors[color.name.split('_')[1]]
        codes.append(SGR['{}_{}'.format(color_prefix, color.name)])
        if bright:
            codes.append(1)

    # 8 bit
    if mode == ColorModes.COLORS_256:
        codes.append(color_type)
        codes.append(SGR_COLORS.COLORS_256)
        codes.append(color)

    # 24 bit
    if mode == ColorModes.TRUECOLOR:
        codes.append(color_type)
        codes.append(SGR_COLORS.TRUECOLOR)
        if isinstance(color, str):
            color = [int(color[i*2:i*2+2], 16) for i in range(0, 3)]
        codes = codes + list(color)

    return compose_sequence(CSI.SELECT_GRAPHIC_RENDITION, *codes)
