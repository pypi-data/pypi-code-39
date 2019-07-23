from __future__ import print_function

from matplotlib.backend_bases import FigureCanvasBase, TimerBase
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib import cbook

from xmlstore.qt_compat import QtGui,QtCore,QtWidgets,qt4_backend

DEBUG = False

class TimerQT(TimerBase):
    '''
    Subclass of :class:`backend_bases.TimerBase` that uses Qt4 timer events.

    Attributes:
    * interval: The time between timer events in milliseconds. Default
        is 1000 ms.
    * single_shot: Boolean flag indicating whether this timer should
        operate as single shot (run once and then stop). Defaults to False.
    * callbacks: Stores list of (func, args) tuples that will be called
        upon timer events. This list can be manipulated directly, or the
        functions add_callback and remove_callback can be used.
    '''
    def __init__(self, *args, **kwargs):
        TimerBase.__init__(self, *args, **kwargs)

        # Create a new timer and connect the timeout() signal to the
        # _on_timer method.
        self._timer = QtCore.QTimer()
        QtCore.QObject.connect(self._timer, QtCore.SIGNAL('timeout()'),
            self._on_timer)

    def __del__(self):
        # Probably not necessary in practice, but is good behavior to disconnect
        TimerBase.__del__(self)
        QtCore.QObject.disconnect(self._timer , QtCore.SIGNAL('timeout()'),
            self._on_timer)

    def _timer_set_single_shot(self):
        self._timer.setSingleShot(self._single)

    def _timer_set_interval(self):
        self._timer.setInterval(self._interval)

    def _timer_start(self):
        self._timer.start()

    def _timer_stop(self):
        self._timer.stop()


class FigureCanvasQT(FigureCanvasBase, QtWidgets.QWidget):

    # map Qt button codes to MouseEvent's ones:
    buttond = {QtCore.Qt.LeftButton: 1,
               QtCore.Qt.MidButton: 2,
               QtCore.Qt.RightButton: 3,
               # QtCore.Qt.XButton1: None,
               # QtCore.Qt.XButton2: None,
               }

    def __init__(self, figure):
        _create_qApp()
        QtWidgets.QWidget.__init__( self )
        FigureCanvasBase.__init__( self, figure )

        self.figure = figure
        # We don't want to scale up the figure DPI more than once.
        # Note, we don't handle a signal for changing DPI yet.
        figure._original_dpi = figure.dpi
        self._update_figure_dpi()
        # In cases with mixed resolution displays, we need to be careful if the
        # dpi_ratio changes - in this case we need to resize the canvas
        # accordingly. We could watch for screenChanged events from Qt, but
        # the issue is that we can't guarantee this will be emitted *before*
        # the first paintEvent for the canvas, so instead we keep track of the
        # dpi_ratio value here and in paintEvent we resize the canvas if
        # needed.
        self._dpi_ratio_prev = None

        self._draw_pending = False
        self._erase_before_paint = False
        self._is_drawing = False
        self._draw_rect_callback = lambda painter: None

        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)
        self.setMouseTracking(True)
        self.resize(*self.get_width_height())
        # Key auto-repeat enabled by default
        self._keyautorepeat = True

        palette = QtGui.QPalette(QtCore.Qt.white)
        self.setPalette(palette)

    def _update_figure_dpi(self):
        dpi = self._dpi_ratio * self.figure._original_dpi
        self.figure._set_dpi(dpi, forward=False)

    @property
    def _dpi_ratio(self):
        # Not available on Qt4 or some older Qt5.
        try:
            # self.devicePixelRatio() returns 0 in rare cases
            return self.devicePixelRatio() or 1
        except AttributeError:
            return 1

    def _update_dpi(self):
        # As described in __init__ above, we need to be careful in cases with
        # mixed resolution displays if dpi_ratio is changing between painting
        # events.
        # Return whether we triggered a resizeEvent (and thus a paintEvent)
        # from within this function.
        if self._dpi_ratio != self._dpi_ratio_prev:
            # We need to update the figure DPI.
            self._update_figure_dpi()
            self._dpi_ratio_prev = self._dpi_ratio
            # The easiest way to resize the canvas is to emit a resizeEvent
            # since we implement all the logic for resizing the canvas for
            # that event.
            event = QtGui.QResizeEvent(self.size(), self.size())
            self.resizeEvent(event)
            # resizeEvent triggers a paintEvent itself, so we exit this one
            # (after making sure that the event is immediately handled).
            return True
        return False

    def get_width_height(self):
        w, h = FigureCanvasBase.get_width_height(self)
        return int(w / self._dpi_ratio), int(h / self._dpi_ratio)

    def enterEvent(self, event):
        try:
            x, y = self.mouseEventCoords(event.pos())
        except AttributeError:
            # the event from PyQt4 does not include the position
            x = y = None
        FigureCanvasBase.enter_notify_event(self, guiEvent=event, xy=(x, y))

    def leaveEvent(self, event):
        QtWidgets.QApplication.restoreOverrideCursor()
        FigureCanvasBase.leave_notify_event(self, guiEvent=event)

    def mouseEventCoords(self, pos):
        """Calculate mouse coordinates in physical pixels

        Qt5 use logical pixels, but the figure is scaled to physical
        pixels for rendering.   Transform to physical pixels so that
        all of the down-stream transforms work as expected.

        Also, the origin is different and needs to be corrected.

        """
        dpi_ratio = self._dpi_ratio
        x = pos.x()
        # flip y so y=0 is bottom of canvas
        y = self.figure.bbox.height / dpi_ratio - pos.y()
        return x * dpi_ratio, y * dpi_ratio

    def mousePressEvent(self, event):
        x, y = self.mouseEventCoords(event.pos())
        button = self.buttond.get(event.button())
        if button is not None:
            FigureCanvasBase.button_press_event(self, x, y, button,
                                                guiEvent=event)

    def mouseDoubleClickEvent(self, event):
        x, y = self.mouseEventCoords(event.pos())
        button = self.buttond.get(event.button())
        if button is not None:
            FigureCanvasBase.button_press_event(self, x, y,
                                                button, dblclick=True,
                                                guiEvent=event)

    def mouseMoveEvent(self, event):
        x, y = self.mouseEventCoords(event)
        FigureCanvasBase.motion_notify_event(self, x, y, guiEvent=event)

    def mouseReleaseEvent(self, event):
        x, y = self.mouseEventCoords(event)
        button = self.buttond.get(event.button())
        if button is not None:
            FigureCanvasBase.button_release_event(self, x, y, button,
                                                  guiEvent=event)

    if qt4_backend == 'PyQt5':
        def wheelEvent(self, event):
            x, y = self.mouseEventCoords(event)
            # from QWheelEvent::delta doc
            if event.pixelDelta().x() == 0 and event.pixelDelta().y() == 0:
                steps = event.angleDelta().y() / 120
            else:
                steps = event.pixelDelta().y()
            if steps:
                FigureCanvasBase.scroll_event(
                    self, x, y, steps, guiEvent=event)
    else:
        def wheelEvent(self, event):
            x = event.x()
            # flipy so y=0 is bottom of canvas
            y = self.figure.bbox.height - event.y()
            # from QWheelEvent::delta doc
            steps = event.delta() / 120
            if event.orientation() == QtCore.Qt.Vertical:
                FigureCanvasBase.scroll_event(
                    self, x, y, steps, guiEvent=event)

    def keyPressEvent(self, event):
        key = self._get_key(event)
        if key is not None:
            FigureCanvasBase.key_press_event(self, key, guiEvent=event)

    def keyReleaseEvent(self, event):
        key = self._get_key(event)
        if key is not None:
            FigureCanvasBase.key_release_event(self, key, guiEvent=event)

    @property
    @cbook.deprecated("3.0", "Manually check `event.guiEvent.isAutoRepeat()` "
                      "in the event handler.")
    def keyAutoRepeat(self):
        """
        If True, enable auto-repeat for key events.
        """
        return self._keyautorepeat

    @keyAutoRepeat.setter
    @cbook.deprecated("3.0", "Manually check `event.guiEvent.isAutoRepeat()` "
                      "in the event handler.")
    def keyAutoRepeat(self, val):
        self._keyautorepeat = bool(val)

    def resizeEvent(self, event):
        # _dpi_ratio_prev will be set the first time the canvas is painted, and
        # the rendered buffer is useless before anyways.
        if self._dpi_ratio_prev is None:
            return
        w = event.size().width() * self._dpi_ratio
        h = event.size().height() * self._dpi_ratio
        dpival = self.figure.dpi
        winch = w / dpival
        hinch = h / dpival
        self.figure.set_size_inches(winch, hinch, forward=False)
        # pass back into Qt to let it finish
        QtWidgets.QWidget.resizeEvent(self, event)
        # emit our resize events
        FigureCanvasBase.resize_event(self)

    def sizeHint(self):
        w, h = self.get_width_height()
        return QtCore.QSize(w, h)

    def minumumSizeHint(self):
        return QtCore.QSize(10, 10)

    def _get_key(self, event):
        if not self._keyautorepeat and event.isAutoRepeat():
            return None

        event_key = event.key()
        event_mods = int(event.modifiers())  # actually a bitmask

        # get names of the pressed modifier keys
        # bit twiddling to pick out modifier keys from event_mods bitmask,
        # if event_key is a MODIFIER, it should not be duplicated in mods
        mods = [name for name, mod_key, qt_key in MODIFIER_KEYS
                if event_key != qt_key and (event_mods & mod_key) == mod_key]
        try:
            # for certain keys (enter, left, backspace, etc) use a word for the
            # key, rather than unicode
            key = SPECIAL_KEYS[event_key]
        except KeyError:
            # unicode defines code points up to 0x0010ffff
            # QT will use Key_Codes larger than that for keyboard keys that are
            # are not unicode characters (like multimedia keys)
            # skip these
            # if you really want them, you should add them to SPECIAL_KEYS
            MAX_UNICODE = 0x10ffff
            if event_key > MAX_UNICODE:
                return None

            key = chr(event_key)
            # qt delivers capitalized letters.  fix capitalization
            # note that capslock is ignored
            if 'shift' in mods:
                mods.remove('shift')
            else:
                key = key.lower()

        mods.reverse()
        return '+'.join(mods + [key])

    def new_timer(self, *args, **kwargs):
        """
        Creates a new backend-specific subclass of
        :class:`backend_bases.Timer`.  This is useful for getting
        periodic events through the backend's native event
        loop. Implemented only for backends with GUIs.

        Other Parameters
        ----------------
        interval : scalar
            Timer interval in milliseconds

        callbacks : list
            Sequence of (func, args, kwargs) where ``func(*args, **kwargs)``
            will be executed by the timer every *interval*.

        """
        return TimerQT(*args, **kwargs)

    def flush_events(self):
        QtWidgets.qApp.processEvents()

    def start_event_loop(self, timeout=0):
        if hasattr(self, "_event_loop") and self._event_loop.isRunning():
            raise RuntimeError("Event loop already running")
        self._event_loop = event_loop = QtCore.QEventLoop()
        if timeout:
            timer = QtCore.QTimer.singleShot(timeout * 1000, event_loop.quit)
        event_loop.exec_()

    def stop_event_loop(self, event=None):
        if hasattr(self, "_event_loop"):
            self._event_loop.quit()

    def draw(self):
        """Render the figure, and queue a request for a Qt draw.
        """
        # The renderer draw is done here; delaying causes problems with code
        # that uses the result of the draw() to update plot elements.
        if self._is_drawing:
            return
        with cbook._setattr_cm(self, _is_drawing=True):
            super().draw()
        self._erase_before_paint = True
        self.update()

    def draw_idle(self):
        """Queue redraw of the Agg buffer and request Qt paintEvent.
        """
        # The Agg draw needs to be handled by the same thread matplotlib
        # modifies the scene graph from. Post Agg draw request to the
        # current event loop in order to ensure thread affinity and to
        # accumulate multiple draw requests from event handling.
        # TODO: queued signal connection might be safer than singleShot
        if not (self._draw_pending or self._is_drawing):
            self._draw_pending = True
            QtCore.QTimer.singleShot(0, self._draw_idle)

    def _draw_idle(self):
        if self.height() < 0 or self.width() < 0:
            self._draw_pending = False
        if not self._draw_pending:
            return
        try:
            self.draw()
        except Exception:
            # Uncaught exceptions are fatal for PyQt5, so catch them instead.
            traceback.print_exc()
        finally:
            self._draw_pending = False

    def drawRectangle(self, rect):
        # Draw the zoom rectangle to the QPainter.  _draw_rect_callback needs
        # to be called at the end of paintEvent.
        if rect is not None:
            def _draw_rect_callback(painter):
                pen = QtGui.QPen(QtCore.Qt.black, 1 / self._dpi_ratio,
                                 QtCore.Qt.DotLine)
                painter.setPen(pen)
                painter.drawRect(*(pt / self._dpi_ratio for pt in rect))
        else:
            def _draw_rect_callback(painter):
                return
        self._draw_rect_callback = _draw_rect_callback
        self.update()

class FigureCanvasQTAgg(FigureCanvasAgg, FigureCanvasQT):

    # JB: added "afterResize" signal
    afterResize = QtCore.Signal()

    def __init__(self, figure):
        # Must pass 'figure' as kwarg to Qt base class.
        FigureCanvasQT.__init__( self, figure )
        FigureCanvasAgg.__init__( self, figure )

        # JB: do NOT set QtCore.Qt.WA_OpaquePaintEvent because part of the figure is transparent.
        #self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

        # JB: added "animating" flag.
        self.animating = False

    def paintEvent(self, event):
        """Copy the image from the Agg canvas to the qt.drawable.

        In Qt, all drawing should be done inside of here when a widget is
        shown onscreen.
        """
        if self._update_dpi():
            # The dpi update triggered its own paintEvent.
            return
        self._draw_idle()  # Only does something if a draw is pending.

        # if the canvas does not have a renderer, then give up and wait for
        # FigureCanvasAgg.draw(self) to be called
        if not hasattr(self, 'renderer'):
            return

        painter = QtGui.QPainter(self)

        if self._erase_before_paint:
            painter.eraseRect(self.rect())
            self._erase_before_paint = False

        rect = event.rect()
        left = rect.left()
        top = rect.top()
        width = rect.width()
        height = rect.height()
        # See documentation of QRect: bottom() and right() are off by 1, so use
        # left() + width() and top() + height().
        bbox = Bbox(
            [[left, self.renderer.height - (top + height * self._dpi_ratio)],
             [left + width * self._dpi_ratio, self.renderer.height - top]])
        reg = self.copy_from_bbox(bbox)
        buf = cbook._unmultiplied_rgba8888_to_premultiplied_argb32(
            memoryview(reg))
        qimage = QtGui.QImage(buf, buf.shape[1], buf.shape[0],
                              QtGui.QImage.Format_ARGB32_Premultiplied)
        if hasattr(qimage, 'setDevicePixelRatio'):
            # Not available on Qt4 or some older Qt5.
            qimage.setDevicePixelRatio(self._dpi_ratio)
        origin = QtCore.QPoint(left, top)
        painter.drawImage(origin / self._dpi_ratio, qimage)
        # Adjust the buf reference count to work around a memory
        # leak bug in QImage under PySide on Python 3.
        if QT_API in ('PySide', 'PySide2'):
            ctypes.c_long.from_address(id(buf)).value = 1

        self._draw_rect_callback(painter)

        painter.end()

    def draw( self ):
        """
        Draw the figure when xwindows is ready for the update
        """

        if DEBUG: print("FigureCanvasQtAgg.draw", self)
        self.replot = True

        # JB: Part of the figure will be transparent (everything outside the axes region),
        # so here we explicitly clear the Agg canvas. If we do not do that, parts of the original
        # figure will "shine through" in the transparent regions.
        self.get_renderer().clear()

        # JB: either repaint or update based on state of "animating" flag
        #self.update()
        if self.animating:
            # Force an immediate repaint. If we'd call update instead, multiple updates might only result 
            # in a single (delayed) repaint, thus losing the animation effect.
            self.repaint()
        else:
            self.update()

    def blit(self, bbox=None):
        """Blit the region in bbox.
        """
        # If bbox is None, blit the entire canvas. Otherwise
        # blit only the area defined by the bbox.
        if bbox is None and self.figure:
            bbox = self.figure.bbox

        # repaint uses logical pixels, not physical pixels like the renderer.
        l, b, w, h = [pt / self._dpi_ratio for pt in bbox.bounds]
        t = b + h
        self.repaint(l, self.renderer.height / self._dpi_ratio - t, w, h)

    def print_figure(self, *args, **kwargs):
        FigureCanvasAgg.print_figure(self, *args, **kwargs)
        self.draw()

    # JB: emit afterResize event after resizing.
    def resizeEvent( self, e ):
        FigureCanvasQT.resizeEvent( self, e )
        self.afterResize.emit()

