"""Definition of the ASP viewer"""
import biseau as bs
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class ASPViewer(QWidget):
    """A view on ASP code, able to transmit dot to another widget"""
    def __init__(self, next_viewer):
        super().__init__()
        self.setWindowTitle("ASP")

        self._next_viewer = next_viewer
        self.tool_bar = QToolBar()
        self.tool_bar.addAction('Compile to dot/models',
                                lambda: self.set_asp(self.get_asp()))
        self.edit = QTextEdit()
        self.edit.setFont('Monospace')
        _layout = QVBoxLayout()
        _layout.addWidget(self.tool_bar)
        _layout.addWidget(self.edit)
        _layout.setContentsMargins(0, 0, 0, 0)
        self.set_asp('')
        self.setLayout(_layout)

    def _setup_toolbar(self):
        "Populate the toolbar"

    def set_asp(self, source, compile_and_send=True):
        self.edit.setText(source)
        if compile_and_send:
            if hasattr(self._next_viewer, 'set_dot'):
                dot = bs.compile_context_to_dot(source)
                self._next_viewer.set_dot(dot)
            elif hasattr(self._next_viewer, 'set_models'):
                models = bs.script.solve_context(source)
                self._next_viewer.set_models(models)
            else:
                raise NotImplementedError(f"Behavior for next_viewer {self._next_viewer}")

    def get_asp(self):
        return self.edit.toPlainText()
