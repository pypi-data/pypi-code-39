"""
@package SDF.GUI.sdf_parameters_browser
THIS IS NOT REALLY WORKING YET, IT IS MORE LIKE A DRAFT OR AN IDEA FOR NOW.

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
------------------------------------------------------------------------------

The idea is to pop up a parameter browser for the selected workspace/dataset from the main GUI.
In this parameter browser, the user can then get information on parameters. Searching through 
parameters would be a very nice feature!
"""

from PyQt5.QtWidgets import (QWidget, QTreeView,
                             QVBoxLayout)
import os
HERE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser("~")
from ..model import qt_sdf_parameter_model
from ... import sdf_par


class SDFParameterPopup(QWidget):
    """
    The main widget popping up when the `parameters` button is clicked.
    """
    
    def __init__(self, parent_widget, name_of_parent_sdf_object="", list_of_sdf_par=None):
        super(SDFParameterPopup, self).__init__()
        self.parent_widget = parent_widget
        self.init_model(list_of_sdf_par)
        self.init_ui(name_of_parent_sdf_object)

    def init_ui(self, name_of_parent_sdf_object):
        self.setWindowTitle("Parameters of sdf_object '%s'" % name_of_parent_sdf_object)
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        self.treeview = QTreeView(self)
        self.treeview.setModel(self.model)
        vbox.addWidget(self.treeview)

    def init_model(self, list_of_sdf_par):        
        root_node = sdf_par("root")
        self.model = qt_sdf_parameter_model.ParameterTreeViewModel(root_node)
        if list_of_sdf_par:
            self.model.parse_list_of_sdf_par(list_of_sdf_par)
        
    def parse_list_of_sdf_par(self, list_of_sdf_par):
        self.model.parse_list_of_sdf_par(list_of_sdf_par)

    def closeEvent(self, event):
        self.parent_widget.par_popups.pop(self.parent_widget.par_popups.index(self))
        event.accept()
        
