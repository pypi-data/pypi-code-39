#
# Copyright (c) 2016-2019 Deephaven Data Labs and Patent Pending
#

######################################################################################################################
#               This code is auto generated. DO NOT EDIT FILE!
# Run generatePythonFigureWrapper or "./gradlew :Generators:generatePythonFigureWrapper" to generate
######################################################################################################################


import sys
import logging
import jpy
import numpy
import pandas
import wrapt

from ..conversion_utils import _isJavaType, _isStr, makeJavaArray, _ensureBoxedArray, getJavaClassObject


_plotting_convenience_ = None  # this module will be useless with no jvm
_figure_widget_ = None


def defineSymbols():
    """
    Defines appropriate java symbols, which requires that the jvm has been initialized through the :class:`jpy` module,
    for use throughout the module AT RUNTIME. This is versus static definition upon first import, which would lead to an
    exception if the jvm wasn't initialized BEFORE importing the module.
    """

    if not jpy.has_jvm():
        raise SystemError("No java functionality can be used until the JVM has been initialized through the jpy module")

    global _plotting_convenience_, _figure_widget_
    if _plotting_convenience_ is None:
        # an exception will be raised if not in the jvm classpath
        _plotting_convenience_ = jpy.get_type("com.illumon.iris.db.plot.PlottingConvenience")
        _figure_widget_ = jpy.get_type('com.illumon.iris.db.plot.FigureWidget')


if sys.version_info[0] > 2:
    def _is_basic_type_(obj):
        return isinstance(obj, bool) or isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, str)
else:
    def _is_basic_type_(obj):
        return isinstance(obj, bool) or isinstance(obj, int) or isinstance(obj, long) \
               or isinstance(obj, float) or isinstance(obj, basestring)


def _is_widget_(obj):
    if obj is None:
        return False
    cond = False
    try:
        cond = getJavaClassObject('com.illumon.iris.db.plot.FigureWidget').isAssignableFrom(obj)
    except Exception:
        pass
    return cond


def _create_java_object_(obj):
    if obj is None:
        return None
    elif isinstance(obj, FigureWrapper) or _isJavaType(obj):
        # nothing to be done
        return obj
    elif _is_basic_type_(obj):
        # jpy will (*should*) convert this properly
        return obj
    elif isinstance(obj, numpy.ndarray) or isinstance(obj, pandas.Series) or isinstance(obj, pandas.Categorical):
        return makeJavaArray(obj, 'unknown', False)
    elif isinstance(obj, dict):
        return obj  # what would we do?
    elif isinstance(obj, list) or isinstance(obj, tuple):
        return _create_java_object_(numpy.array(obj))  # maybe it's better to pass it straight through?
    elif hasattr(obj, '__iter__'):
        # return _create_java_object_(numpy.array(list(obj))) # this is suspect
        return obj
    else:
        # I have no idea what it is - just pass it straight through
        return obj


def _convert_arguments_(args):
    return [_create_java_object_(el) for el in args]


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

    return wrapped(*_convert_arguments_(args))


@wrapt.decorator
def _convertCatPlotArguments(wrapped, instance, args, kwargs):
    """
    For decoration of FigureWrapper catPlot, catErrorBar, piePlot method, to convert arguments

    :param wrapped: the method to be decorated
    :param instance: the object to which the wrapped function was bound when it was called
    :param args: the argument list for `wrapped`
    :param kwargs: the keyword argument dictionary for `wrapped`
    :return: the decorated version of the method
    """

    cargs = _convert_arguments_(args)
    cargs[1] = _ensureBoxedArray(cargs[1])  # the category field must extend Number (i.e. be boxed)
    return wrapped(*cargs)


@wrapt.decorator
def _convertCatPlot3dArguments(wrapped, instance, args, kwargs):
    """
    For decoration of FigureWrapper catPlot3d method, to convert arguments as necessary

    :param wrapped: the method to be decorated
    :param instance: the object to which the wrapped function was bound when it was called
    :param args: the argument list for `wrapped`
    :param kwargs: the keyword argument dictionary for `wrapped`
    :return: the decorated version of the method
    """

    cargs = _convert_arguments_(args)
    cargs[1] = _ensureBoxedArray(cargs[1])
    cargs[2] = _ensureBoxedArray(cargs[2])
    return wrapped(*cargs)


class FigureWrapper(object):
    """
    Class which assembles a variety of plotting convenience methods into a single usable package
    """

    def __init__(self, *args, **kwargs):
        defineSymbols()
        figure = kwargs.get('figure', None)
        if figure is None:
            figure = _plotting_convenience_.figure(*_convert_arguments_(args))
        self._figure = figure
        self._valid_groups = None

    @property
    def figure(self):
        """The underlying java Figure object"""
        return self._figure

    @property
    def widget(self):
        """The FigureWidget, if applicable. It will be `None` if .show() has NOT been called."""

        if _is_widget_(self.figure.getClass()):
            return self.figure
        return None

    @property
    def validGroups(self):
        """The collection, (actually java array), of valid users"""
        return _create_java_object_(self._valid_groups)

    @validGroups.setter
    def validGroups(self, groups):
        if groups is None:
            self._valid_groups = None
        elif _isStr(groups):
            self._valid_groups = [groups, ]
        else:
            try:
                self._valid_groups = list(groups)  # any other iterable will become a list
            except Exception as e:
                logging.error("Failed to set validGroups using input {} with exception {}".format(groups, e))

    def show(self):
        """
        Wraps the figure in a figure widget for display
        :return: FigureWrapper with figure attribute set to applicable widget
        """

        return FigureWrapper(figure=self._figure.show())

    def getWidget(self):
        """
        Get figure widget, if applicable. It will be `None` if .show() has NOT been called.
        :return: None or the widget reference
        """

        return self.widget

    def getValidGroups(self):
        """
        Get the collection of valid users
        :return: java array of user id strings
        """

        return self.validGroups

    def setValidGroups(self, groups):
        """
        Set the list of user ids which should have access to this figure wrapper object
        :param groups: None, single user id string, or list of user id strings
        """

        self.validGroups = groups

    @_convertArguments
    def axes(self, *args):
        return FigureWrapper(figure=self.figure.axes(*args))

    @_convertArguments
    def axesRemoveSeries(self, *names):
        return FigureWrapper(figure=self.figure.axesRemoveSeries(*names))

    @_convertArguments
    def axis(self, dim):
        return FigureWrapper(figure=self.figure.axis(dim))

    @_convertArguments
    def axisColor(self, color):
        return FigureWrapper(figure=self.figure.axisColor(color))

    @_convertArguments
    def axisFormat(self, format):
        return FigureWrapper(figure=self.figure.axisFormat(format))

    @_convertArguments
    def axisFormatPattern(self, pattern):
        return FigureWrapper(figure=self.figure.axisFormatPattern(pattern))

    @_convertArguments
    def axisLabel(self, label):
        return FigureWrapper(figure=self.figure.axisLabel(label))

    @_convertArguments
    def axisLabelFont(self, *args):
        return FigureWrapper(figure=self.figure.axisLabelFont(*args))

    @_convertArguments
    def businessTime(self, *args):
        return FigureWrapper(figure=self.figure.businessTime(*args))

    @_convertCatPlotArguments
    def catErrorBar(self, *args):
        return FigureWrapper(figure=self.figure.catErrorBar(*args))

    @_convertArguments
    def catErrorBarBy(self, *args):
        return FigureWrapper(figure=self.figure.catErrorBarBy(*args))

    @_convertArguments
    def catHistPlot(self, *args):
        return FigureWrapper(figure=self.figure.catHistPlot(*args))

    @_convertCatPlotArguments
    def catPlot(self, *args):
        return FigureWrapper(figure=self.figure.catPlot(*args))

    @_convertCatPlot3dArguments
    def catPlot3d(self, *args):
        return FigureWrapper(figure=self.figure.catPlot3d(*args))

    @_convertArguments
    def catPlot3dBy(self, seriesName, t, xCategoriesColumn, zCategoriesColumn, valuesColumn, *byColumns):
        return FigureWrapper(figure=self.figure.catPlot3dBy(seriesName, t, xCategoriesColumn, zCategoriesColumn, valuesColumn, *byColumns))

    @_convertArguments
    def catPlotBy(self, *args):
        return FigureWrapper(figure=self.figure.catPlotBy(*args))

    @_convertArguments
    def chart(self, *args):
        return FigureWrapper(figure=self.figure.chart(*args))

    @_convertArguments
    def chartRemoveSeries(self, *names):
        return FigureWrapper(figure=self.figure.chartRemoveSeries(*names))

    @_convertArguments
    def chartTitle(self, *args):
        return FigureWrapper(figure=self.figure.chartTitle(*args))

    @_convertArguments
    def chartTitleColor(self, color):
        return FigureWrapper(figure=self.figure.chartTitleColor(color))

    @_convertArguments
    def chartTitleFont(self, *args):
        return FigureWrapper(figure=self.figure.chartTitleFont(*args))

    @_convertArguments
    def colSpan(self, n):
        return FigureWrapper(figure=self.figure.colSpan(n))

    @_convertArguments
    def errorBarColor(self, *args):
        return FigureWrapper(figure=self.figure.errorBarColor(*args))

    @_convertArguments
    def errorBarX(self, *args):
        return FigureWrapper(figure=self.figure.errorBarX(*args))

    @_convertArguments
    def errorBarXBy(self, *args):
        return FigureWrapper(figure=self.figure.errorBarXBy(*args))

    @_convertArguments
    def errorBarXY(self, *args):
        return FigureWrapper(figure=self.figure.errorBarXY(*args))

    @_convertArguments
    def errorBarXYBy(self, *args):
        return FigureWrapper(figure=self.figure.errorBarXYBy(*args))

    @_convertArguments
    def errorBarY(self, *args):
        return FigureWrapper(figure=self.figure.errorBarY(*args))

    @_convertArguments
    def errorBarYBy(self, *args):
        return FigureWrapper(figure=self.figure.errorBarYBy(*args))

    @_convertArguments
    def figureRemoveSeries(self, *names):
        return FigureWrapper(figure=self.figure.figureRemoveSeries(*names))

    @_convertArguments
    def figureTitle(self, title):
        return FigureWrapper(figure=self.figure.figureTitle(title))

    @_convertArguments
    def figureTitleColor(self, color):
        return FigureWrapper(figure=self.figure.figureTitleColor(color))

    @_convertArguments
    def figureTitleFont(self, *args):
        return FigureWrapper(figure=self.figure.figureTitleFont(*args))

    @_convertArguments
    def funcNPoints(self, npoints):
        return FigureWrapper(figure=self.figure.funcNPoints(npoints))

    @_convertArguments
    def funcRange(self, *args):
        return FigureWrapper(figure=self.figure.funcRange(*args))

    @_convertArguments
    def gradientVisible(self, *args):
        return FigureWrapper(figure=self.figure.gradientVisible(*args))

    @_convertArguments
    def gridLinesVisible(self, visible):
        return FigureWrapper(figure=self.figure.gridLinesVisible(visible))

    @_convertArguments
    def group(self, *args):
        return FigureWrapper(figure=self.figure.group(*args))

    @_convertArguments
    def histPlot(self, *args):
        return FigureWrapper(figure=self.figure.histPlot(*args))

    @_convertArguments
    def invert(self, *args):
        return FigureWrapper(figure=self.figure.invert(*args))

    @_convertArguments
    def legendColor(self, color):
        return FigureWrapper(figure=self.figure.legendColor(color))

    @_convertArguments
    def legendFont(self, *args):
        return FigureWrapper(figure=self.figure.legendFont(*args))

    @_convertArguments
    def legendVisible(self, visible):
        return FigureWrapper(figure=self.figure.legendVisible(visible))

    @_convertArguments
    def lineColor(self, *args):
        return FigureWrapper(figure=self.figure.lineColor(*args))

    @_convertArguments
    def lineStyle(self, *args):
        return FigureWrapper(figure=self.figure.lineStyle(*args))

    @_convertArguments
    def linesVisible(self, *args):
        return FigureWrapper(figure=self.figure.linesVisible(*args))

    @_convertArguments
    def log(self):
        return FigureWrapper(figure=self.figure.log())

    @_convertArguments
    def max(self, max):
        return FigureWrapper(figure=self.figure.max(max))

    @_convertArguments
    def maxRowsInTitle(self, maxRowsCount):
        return FigureWrapper(figure=self.figure.maxRowsInTitle(maxRowsCount))

    @_convertArguments
    def min(self, min):
        return FigureWrapper(figure=self.figure.min(min))

    @_convertArguments
    def minorTicks(self, count):
        return FigureWrapper(figure=self.figure.minorTicks(count))

    @_convertArguments
    def minorTicksVisible(self, visible):
        return FigureWrapper(figure=self.figure.minorTicksVisible(visible))

    @_convertArguments
    def newAxes(self, *args):
        return FigureWrapper(figure=self.figure.newAxes(*args))

    @_convertArguments
    def newChart(self, *args):
        return FigureWrapper(figure=self.figure.newChart(*args))

    @_convertArguments
    def ohlcPlot(self, *args):
        return FigureWrapper(figure=self.figure.ohlcPlot(*args))

    @_convertArguments
    def ohlcPlotBy(self, *args):
        return FigureWrapper(figure=self.figure.ohlcPlotBy(*args))

    @_convertCatPlotArguments
    def piePlot(self, *args):
        return FigureWrapper(figure=self.figure.piePlot(*args))

    @_convertArguments
    def plot(self, *args):
        return FigureWrapper(figure=self.figure.plot(*args))

    @_convertArguments
    def plot3d(self, *args):
        return FigureWrapper(figure=self.figure.plot3d(*args))

    @_convertArguments
    def plot3dBy(self, seriesName, t, x, y, z, *byColumns):
        return FigureWrapper(figure=self.figure.plot3dBy(seriesName, t, x, y, z, *byColumns))

    @_convertArguments
    def plotBy(self, *args):
        return FigureWrapper(figure=self.figure.plotBy(*args))

    @_convertArguments
    def plotOrientation(self, orientation):
        return FigureWrapper(figure=self.figure.plotOrientation(orientation))

    @_convertArguments
    def plotStyle(self, style):
        return FigureWrapper(figure=self.figure.plotStyle(style))

    @_convertArguments
    def pointColor(self, *args):
        return FigureWrapper(figure=self.figure.pointColor(*args))

    @_convertArguments
    def pointColorByX(self, *args):
        return FigureWrapper(figure=self.figure.pointColorByX(*args))

    @_convertArguments
    def pointColorByY(self, *args):
        return FigureWrapper(figure=self.figure.pointColorByY(*args))

    @_convertArguments
    def pointColorByZ(self, *args):
        return FigureWrapper(figure=self.figure.pointColorByZ(*args))

    @_convertArguments
    def pointColorInteger(self, *args):
        return FigureWrapper(figure=self.figure.pointColorInteger(*args))

    @_convertArguments
    def pointColorIntegerByX(self, *args):
        return FigureWrapper(figure=self.figure.pointColorIntegerByX(*args))

    @_convertArguments
    def pointColorIntegerByZ(self, *args):
        return FigureWrapper(figure=self.figure.pointColorIntegerByZ(*args))

    @_convertArguments
    def pointLabel(self, *args):
        return FigureWrapper(figure=self.figure.pointLabel(*args))

    @_convertArguments
    def pointLabelByX(self, *args):
        return FigureWrapper(figure=self.figure.pointLabelByX(*args))

    @_convertArguments
    def pointLabelByZ(self, *args):
        return FigureWrapper(figure=self.figure.pointLabelByZ(*args))

    @_convertArguments
    def pointLabelFormat(self, *args):
        return FigureWrapper(figure=self.figure.pointLabelFormat(*args))

    @_convertArguments
    def pointShape(self, *args):
        return FigureWrapper(figure=self.figure.pointShape(*args))

    @_convertArguments
    def pointSize(self, *args):
        return FigureWrapper(figure=self.figure.pointSize(*args))

    @_convertArguments
    def pointSizeByX(self, *args):
        return FigureWrapper(figure=self.figure.pointSizeByX(*args))

    @_convertArguments
    def pointSizeByZ(self, *args):
        return FigureWrapper(figure=self.figure.pointSizeByZ(*args))

    @_convertArguments
    def pointsVisible(self, *args):
        return FigureWrapper(figure=self.figure.pointsVisible(*args))

    @_convertArguments
    def range(self, min, max):
        return FigureWrapper(figure=self.figure.range(min, max))

    @_convertArguments
    def removeChart(self, *args):
        return FigureWrapper(figure=self.figure.removeChart(*args))

    @_convertArguments
    def rowSpan(self, n):
        return FigureWrapper(figure=self.figure.rowSpan(n))

    @_convertArguments
    def save(self, *args):
        return FigureWrapper(figure=self.figure.save(*args))

    @_convertArguments
    def series(self, *args):
        return FigureWrapper(figure=self.figure.series(*args))

    @_convertArguments
    def seriesColor(self, *args):
        return FigureWrapper(figure=self.figure.seriesColor(*args))

    @_convertArguments
    def seriesNamingFunction(self, namingFunction):
        return FigureWrapper(figure=self.figure.seriesNamingFunction(namingFunction))

    @_convertArguments
    def span(self, rowSpan, colSpan):
        return FigureWrapper(figure=self.figure.span(rowSpan, colSpan))

    @_convertArguments
    def theme(self, theme):
        return FigureWrapper(figure=self.figure.theme(theme))

    @_convertArguments
    def tickLabelAngle(self, angle):
        return FigureWrapper(figure=self.figure.tickLabelAngle(angle))

    @_convertArguments
    def ticks(self, *args):
        return FigureWrapper(figure=self.figure.ticks(*args))

    @_convertArguments
    def ticksFont(self, *args):
        return FigureWrapper(figure=self.figure.ticksFont(*args))

    @_convertArguments
    def ticksVisible(self, visible):
        return FigureWrapper(figure=self.figure.ticksVisible(visible))

    @_convertArguments
    def toolTipPattern(self, *args):
        return FigureWrapper(figure=self.figure.toolTipPattern(*args))

    @_convertArguments
    def transform(self, transform):
        return FigureWrapper(figure=self.figure.transform(transform))

    @_convertArguments
    def twin(self, *args):
        return FigureWrapper(figure=self.figure.twin(*args))

    @_convertArguments
    def twinX(self, *args):
        return FigureWrapper(figure=self.figure.twinX(*args))

    @_convertArguments
    def twinY(self, *args):
        return FigureWrapper(figure=self.figure.twinY(*args))

    @_convertArguments
    def twinZ(self, *args):
        return FigureWrapper(figure=self.figure.twinZ(*args))

    @_convertArguments
    def updateInterval(self, updateIntervalMillis):
        return FigureWrapper(figure=self.figure.updateInterval(updateIntervalMillis))

    @_convertArguments
    def xAxis(self):
        return FigureWrapper(figure=self.figure.xAxis())

    @_convertArguments
    def xBusinessTime(self, *args):
        return FigureWrapper(figure=self.figure.xBusinessTime(*args))

    @_convertArguments
    def xColor(self, color):
        return FigureWrapper(figure=self.figure.xColor(color))

    @_convertArguments
    def xFormat(self, format):
        return FigureWrapper(figure=self.figure.xFormat(format))

    @_convertArguments
    def xFormatPattern(self, pattern):
        return FigureWrapper(figure=self.figure.xFormatPattern(pattern))

    @_convertArguments
    def xGridLinesVisible(self, visible):
        return FigureWrapper(figure=self.figure.xGridLinesVisible(visible))

    @_convertArguments
    def xInvert(self, *args):
        return FigureWrapper(figure=self.figure.xInvert(*args))

    @_convertArguments
    def xLabel(self, label):
        return FigureWrapper(figure=self.figure.xLabel(label))

    @_convertArguments
    def xLabelFont(self, *args):
        return FigureWrapper(figure=self.figure.xLabelFont(*args))

    @_convertArguments
    def xLog(self):
        return FigureWrapper(figure=self.figure.xLog())

    @_convertArguments
    def xMax(self, max):
        return FigureWrapper(figure=self.figure.xMax(max))

    @_convertArguments
    def xMin(self, min):
        return FigureWrapper(figure=self.figure.xMin(min))

    @_convertArguments
    def xMinorTicks(self, count):
        return FigureWrapper(figure=self.figure.xMinorTicks(count))

    @_convertArguments
    def xMinorTicksVisible(self, visible):
        return FigureWrapper(figure=self.figure.xMinorTicksVisible(visible))

    @_convertArguments
    def xRange(self, min, max):
        return FigureWrapper(figure=self.figure.xRange(min, max))

    @_convertArguments
    def xTickLabelAngle(self, angle):
        return FigureWrapper(figure=self.figure.xTickLabelAngle(angle))

    @_convertArguments
    def xTicks(self, *args):
        return FigureWrapper(figure=self.figure.xTicks(*args))

    @_convertArguments
    def xTicksFont(self, *args):
        return FigureWrapper(figure=self.figure.xTicksFont(*args))

    @_convertArguments
    def xTicksVisible(self, visible):
        return FigureWrapper(figure=self.figure.xTicksVisible(visible))

    @_convertArguments
    def xToolTipPattern(self, *args):
        return FigureWrapper(figure=self.figure.xToolTipPattern(*args))

    @_convertArguments
    def xTransform(self, transform):
        return FigureWrapper(figure=self.figure.xTransform(transform))

    @_convertArguments
    def yAxis(self):
        return FigureWrapper(figure=self.figure.yAxis())

    @_convertArguments
    def yBusinessTime(self, *args):
        return FigureWrapper(figure=self.figure.yBusinessTime(*args))

    @_convertArguments
    def yColor(self, color):
        return FigureWrapper(figure=self.figure.yColor(color))

    @_convertArguments
    def yFormat(self, format):
        return FigureWrapper(figure=self.figure.yFormat(format))

    @_convertArguments
    def yFormatPattern(self, pattern):
        return FigureWrapper(figure=self.figure.yFormatPattern(pattern))

    @_convertArguments
    def yGridLinesVisible(self, visible):
        return FigureWrapper(figure=self.figure.yGridLinesVisible(visible))

    @_convertArguments
    def yInvert(self, *args):
        return FigureWrapper(figure=self.figure.yInvert(*args))

    @_convertArguments
    def yLabel(self, label):
        return FigureWrapper(figure=self.figure.yLabel(label))

    @_convertArguments
    def yLabelFont(self, *args):
        return FigureWrapper(figure=self.figure.yLabelFont(*args))

    @_convertArguments
    def yLog(self):
        return FigureWrapper(figure=self.figure.yLog())

    @_convertArguments
    def yMax(self, max):
        return FigureWrapper(figure=self.figure.yMax(max))

    @_convertArguments
    def yMin(self, min):
        return FigureWrapper(figure=self.figure.yMin(min))

    @_convertArguments
    def yMinorTicks(self, count):
        return FigureWrapper(figure=self.figure.yMinorTicks(count))

    @_convertArguments
    def yMinorTicksVisible(self, visible):
        return FigureWrapper(figure=self.figure.yMinorTicksVisible(visible))

    @_convertArguments
    def yRange(self, min, max):
        return FigureWrapper(figure=self.figure.yRange(min, max))

    @_convertArguments
    def yTickLabelAngle(self, angle):
        return FigureWrapper(figure=self.figure.yTickLabelAngle(angle))

    @_convertArguments
    def yTicks(self, *args):
        return FigureWrapper(figure=self.figure.yTicks(*args))

    @_convertArguments
    def yTicksFont(self, *args):
        return FigureWrapper(figure=self.figure.yTicksFont(*args))

    @_convertArguments
    def yTicksVisible(self, visible):
        return FigureWrapper(figure=self.figure.yTicksVisible(visible))

    @_convertArguments
    def yToolTipPattern(self, *args):
        return FigureWrapper(figure=self.figure.yToolTipPattern(*args))

    @_convertArguments
    def yTransform(self, transform):
        return FigureWrapper(figure=self.figure.yTransform(transform))

    @_convertArguments
    def zAxis(self):
        return FigureWrapper(figure=self.figure.zAxis())

    @_convertArguments
    def zBusinessTime(self, *args):
        return FigureWrapper(figure=self.figure.zBusinessTime(*args))

    @_convertArguments
    def zColor(self, color):
        return FigureWrapper(figure=self.figure.zColor(color))

    @_convertArguments
    def zFormat(self, format):
        return FigureWrapper(figure=self.figure.zFormat(format))

    @_convertArguments
    def zFormatPattern(self, pattern):
        return FigureWrapper(figure=self.figure.zFormatPattern(pattern))

    @_convertArguments
    def zInvert(self, *args):
        return FigureWrapper(figure=self.figure.zInvert(*args))

    @_convertArguments
    def zLabel(self, label):
        return FigureWrapper(figure=self.figure.zLabel(label))

    @_convertArguments
    def zLabelFont(self, *args):
        return FigureWrapper(figure=self.figure.zLabelFont(*args))

    @_convertArguments
    def zLog(self):
        return FigureWrapper(figure=self.figure.zLog())

    @_convertArguments
    def zMax(self, max):
        return FigureWrapper(figure=self.figure.zMax(max))

    @_convertArguments
    def zMin(self, min):
        return FigureWrapper(figure=self.figure.zMin(min))

    @_convertArguments
    def zMinorTicks(self, count):
        return FigureWrapper(figure=self.figure.zMinorTicks(count))

    @_convertArguments
    def zMinorTicksVisible(self, visible):
        return FigureWrapper(figure=self.figure.zMinorTicksVisible(visible))

    @_convertArguments
    def zRange(self, min, max):
        return FigureWrapper(figure=self.figure.zRange(min, max))

    @_convertArguments
    def zTickLabelAngle(self, angle):
        return FigureWrapper(figure=self.figure.zTickLabelAngle(angle))

    @_convertArguments
    def zTicks(self, *args):
        return FigureWrapper(figure=self.figure.zTicks(*args))

    @_convertArguments
    def zTicksFont(self, *args):
        return FigureWrapper(figure=self.figure.zTicksFont(*args))

    @_convertArguments
    def zTicksVisible(self, visible):
        return FigureWrapper(figure=self.figure.zTicksVisible(visible))

    @_convertArguments
    def zToolTipPattern(self, *args):
        return FigureWrapper(figure=self.figure.zToolTipPattern(*args))

    @_convertArguments
    def zTransform(self, transform):
        return FigureWrapper(figure=self.figure.zTransform(transform))
