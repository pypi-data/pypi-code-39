"""Interface allowing user to export current pipeline.
"""

import biseau as bs
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class ScriptExporterDialog(QDialog):
    """Help user to define the exported pipeline"""


    def __init__(self, parent, scripts:[bs.Script]):
        super().__init__(parent)
        self.scripts = tuple(scripts)
        self.pipeline_options = bs.export.get_pipeline_options(scripts)
        self.pipeline_params = {
            'name': (QLineEdit, 'Standalone script'),
            'save in': (QLineEdit, 'standalone_script.py'),
            'GUI': (QCheckBox, True),
            'output file': (QLineEdit, 'out.png'),
        }
        self.build_widgets()

    def build_widgets(self):
        "Build widgets of the dialog"
        def make_labelled(label:str, widget:QWidget) -> QHBoxLayout:
            h_layout = QHBoxLayout()
            h_layout.addWidget(QLabel(label, parent=self))
            h_layout.addWidget(widget)
            return h_layout

        layout = QVBoxLayout()
        # Script/pipeline options widgets lists
        option_layout = QVBoxLayout()
        self.__options_checkbox = {}  # option name -> associated checkbox
        for option_name, totake in self.pipeline_options.items():
            chkbox = QCheckBox(self)
            chkbox.setCheckState(Qt.Checked if totake else Qt.Unchecked)
            self.__options_checkbox[option_name] = chkbox
            option_layout.addLayout(make_labelled(option_name, chkbox))
        # Pipeline general parameters

        params_layout = QVBoxLayout()
        self.__params_widget = {}  # param name -> associated widget
        for param, (widget, value) in self.pipeline_params.items():
            if widget is QLineEdit:
                widget = QLineEdit(parent=self, text=value)
            elif widget is QCheckBox:
                widget = QCheckBox(self)
                widget.setCheckState(Qt.Checked if value else Qt.Unchecked)
            else:
                assert False, f"not handled: {widget}"
            self.__params_widget[param] = widget
            params_layout.addLayout(make_labelled(param, widget))

        # Update savein depending of name
        self.__params_widget['name'].textChanged.connect(
            lambda newtext: self.__params_widget['save in'].setText(newtext.lower().replace(' ', '_') + '.py')
        )

        # assembly (set frames around each sub layout)
        frame = QFrame()
        frame.setLineWidth(1)
        frame.setFrameShape(QFrame.Box)
        frame.setLayout(option_layout)
        layout.addWidget(frame)

        frame = QFrame()
        frame.setLineWidth(2)
        frame.setFrameShape(QFrame.Box)
        frame.setLayout(params_layout)
        layout.addWidget(frame)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.button_box.accepted.connect(self.make_export)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self.setLayout(layout)
        self.setWindowTitle("Script exporter")


    def get_pipeline_options(self):
        "Return {option: to take}, based on "
        return {
            option: chkbox.checkState() is Qt.Checked
            for option, chkbox in self.__options_checkbox.items()
        }

    @property
    def pipeline_name(self) -> str:
            return self.__params_widget['name'].text()
    @property
    def pipeline_savein(self) -> str:
            return self.__params_widget['save in'].text()
    @property
    def pipeline_hasGUI(self) -> bool:
            return self.__params_widget['GUI'].checkState() is Qt.Checked
    @property
    def pipeline_outfile(self) -> str:
            return self.__params_widget['output file'].text()


    def make_export(self):
        fullcode = bs.standalone_export_pipeline(self.scripts, options=self.get_pipeline_options(), name=self.pipeline_name, metarg_withgui=self.pipeline_hasGUI, metarg_outfile=self.pipeline_outfile)
        with open(self.pipeline_savein, 'w') as fd:
            fd.write(fullcode)
        self.accept()  # close the dialog successfully
