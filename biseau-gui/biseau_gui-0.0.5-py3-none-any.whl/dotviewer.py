from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class DotViewer(QWidget):
    def __init__(self, image_viewer):
        super().__init__()
        self.setWindowTitle("Dot")

        self._image_viewer = image_viewer
        self.tool_bar = QToolBar()
        self.tool_bar.addAction('render', lambda: self.set_dots(self.get_dots()))
        self.tab_widget = QTabWidget()
        _layout = QVBoxLayout()
        _layout.addWidget(self.tool_bar)
        _layout.addWidget(self.tab_widget)
        _layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(_layout)
        self.set_dot('')

    def _setup_toolbar(self):
        "Populate the toolbar"

    def set_dot(self, source:str, compile_and_send=True):
        self.set_dots([source], compile_and_send=compile_and_send)

    def set_dots(self, sources:[str], compile_and_send=True):
        # self.sources = tuple(map('\n'.join, sources))
        self.sources = tuple(sources)
        self._setup_main_tabs()
        if compile_and_send:
            self._image_viewer.set_dots(self.sources)

    def _setup_main_tabs(self):
        "Destroy existing tabs, rebuild them"
        # remove existing tabs
        while self.tab_widget.count():
            view = self.tab_widget.currentIndex()
            self.tab_widget.widget(view).deleteLater()
            self.tab_widget.removeTab(view)

        # for each source, create the view
        for idx, source in enumerate(self.sources, start=1):
            edit = QTextEdit(parent=self)
            edit.setText(source)
            self.tab_widget.addTab(edit, str(idx))

    def get_dots(self) -> [str]:
        for idx in range(self.tab_widget.count()):
            edit = self.tab_widget.widget(idx)
            yield edit.toPlainText()
