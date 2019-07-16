"""
Widget used to show a preview of data in SDF browser.
------------------------------------------------------------------------------
    Copyright (C) 2017-2019 Burkhard Geil, Ilyas Kuhlemann, Filip Savic

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from PyQt5.QtWidgets import (QWidget, QCheckBox,
                             QHBoxLayout, QVBoxLayout)
from ..controller.plot_preview_widget_controller import PlotPreviewWidgetController


class DataPreviewWidget(QWidget):
    """
    Widget to show a preview of the data stored in a dataset.
    """
    def __init__(self):
        """
        Constructor.
        @param parent (Pointer to) Parent widget.
        """
        super(DataPreviewWidget, self).__init__()
        self.show_preview = True
        self.sdf_obj = None
        self.init_ui()

    def init_ui(self):
        """
        Initializes all widgets (buttons, labels, etc.) displayed
        on this widget.
        """
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        hbox_checkbox = QHBoxLayout()
        vbox.addLayout(hbox_checkbox)
        checkbox_data_preview = QCheckBox("Data preview")
        checkbox_data_preview.toggle()
        checkbox_data_preview.stateChanged.connect(self.toggle_show_preview)
        hbox_checkbox.addWidget(checkbox_data_preview)
        hbox_checkbox.addStretch(1)

        ## For now: only ImagePreviewWidget implemented,
        # nothing for single- or multi-column datasets.
        # Will use a static ImagePreviewWidget for now.
        # The idea for later: always create a new 
        # Preview widget when a new dataset is selected.

        ## Pointer to widget displaying the data.
        self.preview_widget = PlotPreviewWidgetController(self)
        vbox.addWidget(self.preview_widget) 

    def toggle_show_preview(self, state):
        raise NotImplementedError("Override in derived class!")
