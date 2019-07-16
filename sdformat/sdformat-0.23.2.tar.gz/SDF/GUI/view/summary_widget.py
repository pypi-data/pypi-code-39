"""
Widget to display a few details of any sdf_object.
------------------------------------------------------------------------------
    Copyright (C) 2016-2019 Burkhard Geil, Ilyas Kuhlemann, Filip Savic

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

from PyQt5.QtWidgets import (QWidget, QLabel,
                             QCheckBox, QPushButton,
                             QVBoxLayout, QHBoxLayout)


class SummaryWidget(QWidget):
    """
    Widget to display a few details of any sdf_object.
    """
    def __init__(self):
        """
        Constructor.
        @param parent (Pointer to) Parent widget, on which this widget is to be displayed.
        """
        super(SummaryWidget, self).__init__()

        self.sdf_obj = None
        self.par_popups = []
        self.init_ui()
        self.parameters_clickable = False

    def init_ui(self):
        """
        Initializes all widgets (buttons, labels, etc.) displayed
        on this widget.
        """
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        ## ------------------------------------
        #      first row: checkbox to turn 
        #      summary on/off
        ## ------------------------------------
        hbox_checkbox = QHBoxLayout()
        vbox.addLayout(hbox_checkbox)

        checkbox_on_off = QCheckBox("Summary")
        hbox_checkbox.addWidget(checkbox_on_off)
        hbox_checkbox.addStretch(1)
        ## ------------------------------------
        ## ------------------------------------
        #      second row: name 
        ## ------------------------------------
        hbox_name = QHBoxLayout()
        vbox.addLayout(hbox_name)
        
        lbl_name = QLabel("Name: ")
        self.sdf_name = QLabel("")
        
        hbox_name.addWidget(lbl_name)
        hbox_name.addWidget(self.sdf_name)
        hbox_name.addStretch(1)
        ## ------------------------------------
        ## ------------------------------------
        #      third row: parameters
        ## ------------------------------------

        hbox_parameters = QHBoxLayout()
        vbox.addLayout(hbox_parameters)        
        btn_parameters = QPushButton("Parameters")
        btn_parameters.clicked.connect(self._popup_parameter_widget)
        lbl_colon = QLabel(":")
        self.sdf_parameters = QLabel("")        
        hbox_parameters.addWidget(btn_parameters)
        hbox_parameters.addWidget(lbl_colon)
        hbox_parameters.addWidget(self.sdf_parameters)
        hbox_parameters.addStretch(1)
        ## ------------------------------------
        ## ------------------------------------
        #      fourth row: instruments and samples
        ## ------------------------------------
        hbox_instruments_and_samples = QHBoxLayout()
        vbox.addLayout(hbox_instruments_and_samples)
        
        btn_instruments = QPushButton("Instruments")
        btn_instruments.clicked.connect(self._popup_instrument_widget)
        lbl_colon_instruments = QLabel(":")
        self.sdf_instruments = QLabel("")
        
        hbox_instruments_and_samples.addWidget(btn_instruments)
        hbox_instruments_and_samples.addWidget(lbl_colon_instruments)
        hbox_instruments_and_samples.addWidget(self.sdf_instruments)
        ## ------------------------------------
        btn_samples = QPushButton("Samples")
        btn_samples.clicked.connect(self._popup_sample_widget)
        lbl_colon_samples = QLabel(":")
        self.sdf_samples = QLabel("")

        hbox_instruments_and_samples.addWidget(btn_samples)
        hbox_instruments_and_samples.addWidget(lbl_colon_samples)
        hbox_instruments_and_samples.addWidget(self.sdf_samples)
        hbox_instruments_and_samples.addStretch(1)
        ## ------------------------------------
        vbox.addStretch(1)
