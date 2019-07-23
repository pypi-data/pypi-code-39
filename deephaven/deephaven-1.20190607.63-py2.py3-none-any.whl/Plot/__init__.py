#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

####################################################################################
#               This code is auto generated. DO NOT EDIT FILE!
# Run generatePythonFigureWrapper or
# "./gradlew :Generators:generatePythonFigureWrapper" to generate
####################################################################################


import jpy
import wrapt
from .figure_wrapper import FigureWrapper, _convert_arguments_


_plotting_convenience_ = None  # this module will be useless with no jvm


def defineSymbols():
    """
    Defines appropriate java symbol, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global _plotting_convenience_
    if _plotting_convenience_ is None:
        # an exception will be raised if not in the jvm classpath
        _plotting_convenience_ = jpy.get_type("com.illumon.iris.db.plot.PlottingConvenience")


@wrapt.decorator
def _convertArguments(wrapped, instance, args, kwargs):
    """
    For decoration of FigureWrapper class methods, to convert arguments as necessary

    :param wrapped: the method to be decorated
    :param instance: the object to which the wrapped function was bound when it was called
    :param args: the argument list for `wrapped`
    :param kwargs: the keyword argument dictionary for `wrapped`
    :return: the decorated version of the method
    """

    defineSymbols()
    return wrapped(*_convert_arguments_(args))


# Define all of our functionality, if currently possible
try:
    defineSymbols()
except Exception as e:
    pass


def figure(*args):
    return FigureWrapper(*args)


def catErrorBar(*args):
    return FigureWrapper().catErrorBar(*args)


def catErrorBarBy(*args):
    return FigureWrapper().catErrorBarBy(*args)


def catHistPlot(*args):
    return FigureWrapper().catHistPlot(*args)


def catPlot(*args):
    return FigureWrapper().catPlot(*args)


def catPlot3d(*args):
    return FigureWrapper().catPlot3d(*args)


def catPlot3dBy(seriesName, t, xCategoriesColumn, zCategoriesColumn, valuesColumn, *byColumns):
    return FigureWrapper().catPlot3dBy(seriesName, t, xCategoriesColumn, zCategoriesColumn, valuesColumn, *byColumns)


def catPlotBy(*args):
    return FigureWrapper().catPlotBy(*args)


@_convertArguments
def color(color):
    return _plotting_convenience_.color(color)


@_convertArguments
def colorHSL(*args):
    return _plotting_convenience_.colorHSL(*args)


@_convertArguments
def colorNames():
    return list(_plotting_convenience_.colorNames())


@_convertArguments
def colorRGB(*args):
    return _plotting_convenience_.colorRGB(*args)


def errorBarX(*args):
    return FigureWrapper().errorBarX(*args)


def errorBarXBy(*args):
    return FigureWrapper().errorBarXBy(*args)


def errorBarXY(*args):
    return FigureWrapper().errorBarXY(*args)


def errorBarXYBy(*args):
    return FigureWrapper().errorBarXYBy(*args)


def errorBarY(*args):
    return FigureWrapper().errorBarY(*args)


def errorBarYBy(*args):
    return FigureWrapper().errorBarYBy(*args)


@_convertArguments
def font(family, style, size):
    return _plotting_convenience_.font(family, style, size)


@_convertArguments
def fontFamilyNames():
    return list(_plotting_convenience_.fontFamilyNames())


@_convertArguments
def fontStyle(style):
    return _plotting_convenience_.fontStyle(style)


@_convertArguments
def fontStyleNames():
    return list(_plotting_convenience_.fontStyleNames())


def histPlot(*args):
    return FigureWrapper().histPlot(*args)


@_convertArguments
def lineEndStyle(style):
    return _plotting_convenience_.lineEndStyle(style)


@_convertArguments
def lineEndStyleNames():
    return list(_plotting_convenience_.lineEndStyleNames())


@_convertArguments
def lineJoinStyle(style):
    return _plotting_convenience_.lineJoinStyle(style)


@_convertArguments
def lineJoinStyleNames():
    return list(_plotting_convenience_.lineJoinStyleNames())


@_convertArguments
def lineStyle(*args):
    return _plotting_convenience_.lineStyle(*args)


def newAxes(*args):
    return FigureWrapper().newAxes(*args)


def newChart(*args):
    return FigureWrapper().newChart(*args)


def ohlcPlot(*args):
    return FigureWrapper().ohlcPlot(*args)


def ohlcPlotBy(*args):
    return FigureWrapper().ohlcPlotBy(*args)


@_convertArguments
def oneClick(*args):
    return _plotting_convenience_.oneClick(*args)


def piePlot(*args):
    return FigureWrapper().piePlot(*args)


def plot(*args):
    return FigureWrapper().plot(*args)


def plot3d(*args):
    return FigureWrapper().plot3d(*args)


def plot3dBy(seriesName, t, x, y, z, *byColumns):
    return FigureWrapper().plot3dBy(seriesName, t, x, y, z, *byColumns)


def plotBy(*args):
    return FigureWrapper().plotBy(*args)


@_convertArguments
def plotStyleNames():
    return list(_plotting_convenience_.plotStyleNames())


@_convertArguments
def scatterPlotMatrix(*args):
    return _plotting_convenience_.scatterPlotMatrix(*args)


@_convertArguments
def themeNames():
    return list(_plotting_convenience_.themeNames())
