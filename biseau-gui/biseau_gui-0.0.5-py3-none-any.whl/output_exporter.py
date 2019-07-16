"""Interface to choose which output to export.

"""

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class OutputExporterDialog(QDialog):
    """Help user to define the exported data"""


    def __init__(self, parent):
        super().__init__(parent)
        self.pipeline_params = {
            'save in': (QLineEdit, 'out-{tab}.{ext}'),
            'GUI': (QCheckBox, True),
            'output file': (QLineEdit, 'out.png'),
        }
        self._widgets = {}
        self.build_widgets()

    def build_widgets(self):
        "Build widgets of the dialog"
        def make_labelled(label:str, widget:QWidget) -> QHBoxLayout:
            h_layout = QHBoxLayout()
            h_layout.addWidget(QLabel(label, parent=self))
            h_layout.addWidget(widget)
            return h_layout

        # create widgets
        wid_filename = QLineEdit(parent=self, text='out-{tab}')
        wid_png = QCheckBox(self)
        wid_png.setCheckState(Qt.Checked)
        wid_svg = QCheckBox(self)
        wid_svg.setCheckState(Qt.Checked)
        wid_dot = QCheckBox(self)
        wid_dot.setCheckState(Qt.Checked)
        wid_asp = QCheckBox(self)
        wid_asp.setCheckState(Qt.Checked)

        # layout them
        layout = QVBoxLayout()
        widgets = ("save in", wid_filename), ("PNG", wid_png), ("SVG", wid_svg), ("dot", wid_dot), ("asp", wid_asp)
        for name, wid in widgets:
            layout.addLayout(make_labelled(name, wid))
            self._widgets[name] = wid

        # buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.button_box.accepted.connect(self.make_export)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)
        self.setWindowTitle("Output exporter")


    @property
    def out_filename(self) -> str:
            return self._widgets['save in'].text()
    @property
    def out_png(self) -> bool:
            return self._widgets['PNG'].checkState() is Qt.Checked
    @property
    def out_svg(self) -> bool:
            return self._widgets['SVG'].checkState() is Qt.Checked
    @property
    def out_dot(self) -> bool:
            return self._widgets['dot'].checkState() is Qt.Checked
    @property
    def out_asp(self) -> bool:
            return self._widgets['asp'].checkState() is Qt.Checked


    def make_export(self):
        self.parent().export_outputs(self.out_filename, png=self.out_png, svg=self.out_svg, dot=self.out_dot, asp=self.out_asp)
        self.accept()  # close the dialog successfully
