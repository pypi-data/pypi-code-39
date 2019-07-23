"""Provide convenient top-level imports for the :mod:`campy.graphics` subpackage.

Library code should still use absolute imports where possible. That is, prefer::

    from campy.graphics.gcolor import GColor

more than::

    from campy.graphics import GColor

These overrides are provided for student (and debugging!) convenience. They are
subject to be removed at any time in the future and should not be considered
part of the API.
"""
# from campy.graphics.gbufferedimage import GBufferedImage
from campy.graphics.gcolor import GColor, Pixel
# GEvents?
# from campy.graphics.gfilechooser import show_open_dialog, show_save_dialog
from campy.graphics.gmath import (
    PI, E,
    to_degrees, to_radians,
    sin_degrees, cos_degrees, tan_degrees,
    vector_magnitude, vector_angle,
    count_digits
)
# from campy.graphics.gobjects import (
#     GObject,
#     GRect, GRoundRect, G3DRect,
#     GOval, GArc,
#     GLine,
#     GImage,
#     GLabel,
#     GPolygon,
#     GCompound
# )
from campy.graphics.goptionpane import ConfirmType, ConfirmResult, MessageType, GOptionPane
from campy.graphics.gtimer import GTimer
from campy.graphics.gtypes import GPoint, GDimension, GRectangle
from campy.graphics.gwindow import GWindow
