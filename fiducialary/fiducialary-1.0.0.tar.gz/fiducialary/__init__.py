"""
  .-.                ___                                       ___
 /    \    .-.      (   )                       .-.           (   )
 | .`. ;  ( __)   .-.| |   ___  ___    .--.    ( __)   .---.   | |    .---.   ___ .-.     ___  ___
 | |(___) (''")  /   \ |  (   )(   )  /    \   (''")  / .-, \  | |   / .-, \ (   )   \   (   )(   )
 | |_      | |  |  .-. |   | |  | |  |  .-. ;   | |  (__) ; |  | |  (__) ; |  | ' .-. ;   | |  | |
(   __)    | |  | |  | |   | |  | |  |  |(___)  | |    .'`  |  | |    .'`  |  |  / (___)  | |  | |
 | |       | |  | |  | |   | |  | |  |  |       | |   / .'| |  | |   / .'| |  | |         | '  | |
 | |       | |  | |  | |   | |  | |  |  | ___   | |  | /  | |  | |  | /  | |  | |         '  `-' |
 | |       | |  | '  | |   | |  ; '  |  '(   )  | |  ; |  ; |  | |  ; |  ; |  | |          `.__. |
 | |       | |  ' `-'  /   ' `-'  /  '  `-' |   | |  ' `-'  |  | |  ' `-'  |  | |          ___ | |
(___)     (___)  `.__,'     '.__.'    `.__,'   (___) `.__.'_. (___) `.__.'_. (___)        (   )' |
                                                                                           ; `-' '
GPL3
By Luke Miller
"""

import cairo
import math
import random


__version__ = "1.0.0"


MARKER_SCALE = 1.2  # how large is the marker on its square


def blank_canvas(width=256, height=256):
    """ Create a blank white canvas """
    #surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    surf = cairo.SVGSurface(None, width, height)
    ctx = cairo.Context(surf)
    ctx.scale(width, height)  # Normalizing the canvas

    ctx = cairo.Context(surf)
    ctx.scale(width, height)
    ctx.rectangle(0, 0,  width, height)
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill()

    return surf, ctx


def arc(ctx, start, end, scale=1.0):
    # arc
    ring = (0.5/3)
    ctx.arc(0.5, 0.5, MARKER_SCALE*ring*math.pi/2, start, end)
    ctx.set_line_width(MARKER_SCALE*scale*ring/(math.pi/2))


def outer_circle(ctx):
    """
    A solid outer circle
    """
    ctx.set_source_rgb(0, 0, 0)
    arc(ctx, 0, math.pi*2)
    ctx.stroke()


def inner_circle(ctx):
    """
    A solid outer circle
    """
    # arc
    ring = (0.5/3)
    ctx.arc(0.5, 0.5, MARKER_SCALE*ring/1.8, 0, math.pi * 2)
    ctx.set_source_rgb(0, 0, 0)
    ctx.fill()


def segment(ctx, bit, bits=12):
    """ Blank out one segment of the outer circle that is 1/bit of the arc """
    arc_size = (math.pi*2)/bits
    ctx.set_source_rgb(1, 1, 1)
    arc(ctx, bit*arc_size, (bit+1)*arc_size+math.pi/360, scale=1.1)
    ctx.stroke()


def generate_text(ctx, text):
    #ctx.select_font_face('Sans')
    ctx.set_font_size(0.03)
    ctx.move_to(0.05, 0.95)
    ctx.set_source_rgb(0, 0, 0)
    ctx.show_text(text)
    ctx.stroke()


def generate_layout(bits=12):
    """ A marker is composed of an circle divided into <bit> segments randomly on or off"""
    return [random.choice(["0", "1"]) for x in range(bits)]


def generate_marker(layout=None, text=None, width=256, height=256, bits=12):
    """ Generate a marker with a layout that corresponds to the layout of bits """
    if not layout:
        layout = generate_layout(bits)
    surface, context = blank_canvas(width, height)
    outer_circle(context)
    for bit, value in enumerate(layout):
        if value == "0":  # turn off this segment of the outer circle
            segment(context, bit, bits=bits)
    inner_circle(context)
    if text:
        generate_text(context, text)
    return surface


def generate_makers(number, width=256, height=256, bits=12, labels=True):
    """ Generate a number of markers that are different from each other """
    unique = []
    checked = 0
    # get unique layouts for the markers
    while len(unique) < number:
        potential = generate_layout(bits)
        checked += 1
        if potential not in unique:
            # make sure markers have some interesting features
            changes1 = len("".join(potential).split("01"))
            changes2 = len("".join(potential).split("10"))
            good_layout = True if changes1 >= 4 or changes2 >= 4 else False
            if good_layout:
                unique.append(potential)
        if checked % 100 == 0:
            print(f"Tried {checked} combinations.")
    print(f"Tried {checked} combinations.")
    surfaces = []
    for i in range(number):
        layout = unique.pop()
        print("layout", layout)
        if labels:
            text = f"{i+1:03}"
        marker_surface = generate_marker(text=text, layout=layout, width=width, height=height, bits=bits)
        surfaces.append(marker_surface)
    return surfaces


def tile_markers(name, surfaces, columns=2, width=256, height=256):
    new_width = width*columns
    rows = (len(surfaces)//columns)
    new_height = height*rows
    new_surface = cairo.PDFSurface(name,
                                 new_width,
                                 new_height
                                     )
    ctx = cairo.Context(new_surface)
    ctx.rectangle(0, 0,  width*columns, height)
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill()

    i = 0
    for column in range(columns):
        for row in range(rows):
            if surfaces:
                marker_surface = surfaces.pop()
                ctx.set_source_surface(marker_surface, width*column, height*row)
                ctx.paint()
                #marker_surface.write_to_png(f"marker{i + 1:03}.png")
                i += 1
    return new_surface


def save_markers_individually(surfaces):
    """ Save markers as their own individual files """
    for i, marker_surface in enumerate(surfaces):
        marker_surface.write_to_png(f"marker{i + 1:03}.png")


def generate_page_of_markers_A4(fname="A4markers.png"):
    height = width = 500
    num_of_markers = 12
    marker_surfaces = generate_makers(num_of_markers, width=width, height=height, bits=12)
#    save_markers_individually(marker_surfaces)
    new_surface = tile_markers("9_markers_A4.pdf", marker_surfaces, columns=3, width=width, height=height)
    new_surface.finish()


if __name__ == "__main__":
    print("Generating 6 standard markers on a page (recommend 12, 16 or 20 bit markers.")
    generate_page_of_markers_A4()