"""Implementation of a generalist image viewer"""
import os
import tempfile
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSvg import *

from graphviz import Source


class ImageView(QGraphicsView):
    def __init__(self, parent, dot_engine:str='dot'):
        super().__init__(parent)
        self.setScene(QGraphicsScene())
        self.dot_engine = dot_engine

        self.setBackgroundBrush(QBrush(Qt.white))
        # It appears that Qt can handle gif:
        #  https://stackoverflow.com/questions/41709464/python-pyqt-add-background-gif
        # so is biseau.gif_from_filenames and derivatives

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        # creation of a temporary file to play with
        # with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.svg') as fd:
            # self.__tempname = fd.name

    # def __del__(self):
        # if self.__tempname:
            # os.unlink(self.__tempname)


    def wheelEvent(self, event):
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())

        # Zoom
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.scale(zoomFactor, zoomFactor)

        # Get the new position
        newPos = self.mapToScene(event.pos())

        # Move scene to old position
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())


    def set_dot(self, dot):
        self.source = Source(dot, format='svg', engine=self.dot_engine)
        self.source.render('tmp')
        self.render()

    def render(self):
        self.dot_item = QGraphicsSvgItem('tmp.svg')
        # print(self.__tempname[:-4])
        # print(self.__tempname)
        # s.render(self.__tempname[:-4])
        # self.dot_item = QGraphicsSvgItem(self.__tempname)
        # self.dot_item.renderer().setViewBox(QRect(0,0,1000,1000))

        # Fixed svg bug... Don't understand why this is required.
        # The renderer.viewBox is small and doesn't fit the itemBoundingRect which is the repaint area.
        self.dot_item.renderer().setViewBox(self.dot_item.boundingRect())

        self.scene().clear()
        self.scene().addItem(self.dot_item)

        # rect.setWidth(rect.width())
        # rect.setHeight(rect.height())

        # Center the view on dot_item
        self.scene().setSceneRect(self.dot_item.sceneBoundingRect())


class ImageViewer(QWidget):

    # exemple signals
    ToggleMultishotMode = Signal()

    def __init__(self, parent, dot_engine_getter:callable):
        super().__init__(parent)
        self.dot_engine_getter = dot_engine_getter
        self.setWindowTitle("Graph")
        self.tool_bar = QToolBar()
        self.tab_widget = QTabWidget()

        _layout = QVBoxLayout()
        _layout.addWidget(self.tool_bar)
        _layout.addWidget(self.tab_widget)
        _layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(_layout)
        self._setup_toolbar()


    def _setup_toolbar(self):
        "Populate the toolbar"
        # example connection simple
        but = self.tool_bar.addAction("Multishot mode")
        but.setCheckable(True)
        but.triggered.connect(self.ToggleMultishotMode.emit)


    def set_dot(self, source: str):
        self.set_dots([source])

    def set_dots(self, sources:[str]):
        self.sources = tuple(sources)
        self._setup_main_tabs()

    def _setup_main_tabs(self):
        "Destroy existing tabs, rebuild them"
        # remove existing tabs
        while self.tab_widget.count():
            view = self.tab_widget.currentIndex()
            self.tab_widget.widget(view).deleteLater()
            self.tab_widget.removeTab(view)

        # for each source, create the view
        self.images_ref = []
        for idx, source in enumerate(self.sources, start=1):
            view = ImageView(self.tab_widget, self.current_dot_engine())
            view.set_dot(source)
            self.images_ref.append(view.source)
            self.tab_widget.addTab(view, str(idx))
        self.tab_widget.setCurrentWidget(self.tab_widget.widget(0))

    def current_dot_engine(self) -> str:
        return self.dot_engine_getter()

    def images_sources(self) -> [str]:
        "Yield current Source objects"
        yield from self.images_ref
