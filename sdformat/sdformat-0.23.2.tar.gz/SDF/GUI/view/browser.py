## @author Ilyas Kuhlemann
# @mail ilyasp.ku@gmail.com
# @date 18.07.16

"""
@package SDF.GUI.browser

A GUI to browse SDF files.

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
-------------------------------------------------------------------------------

The class SDFBrowser is a widget separated in three areas:
#############################################################
#                             #                             #
#   A custom implementation   #      A widget displaying    #
#   of Qt's QTreeView.        #      a bit more detailed    #
#   It displays SDF files     #      information on the     #
#   (or rather: workspaces)   #      selected object.       #
#   in its tree structure.    #                             #
#                             ###############################
#   You can select any line   #                             #
#   to display more infos     #      A widget to display    #
#   on the widgets to the     #      a preview of a data-   #
#   right.                    #      set's data. Currently  #
#                             #      only works for images. #
#                             #                             #
#                             #                             #
#############################################################

The TreeView on the left is mainly implemented in this module.
The model it is based on, however, can be found in the module
SDF.GUI.qt_sdf_model .
Both widgets on the right are implemented in module 
SDF.GUI.sdf_details_widgets .
"""
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout)
import pickle
import os

# from htmldelegate import HTMLDelegate
from .styles import style_sheet
from .customtreeview import CustomTreeView
from ..controller.summary_widget_controller import SummaryWidgetController
from ..controller.data_preview_widget_controller import DataPreviewWidgetController
from ..model import qt_sdf_model
from ... import sdf_object

HERE = os.path.dirname(os.path.abspath(__file__))
HOME = os.path.expanduser("~")


class SDFBrowser(QWidget):
    """
    Widget to browse through any sdf file, displayed in a tree view.
    Also displays some detailed information and image data previews.
    """
    def __init__(self, sdf_obj=None):
        """
        Constructor.
        @param sdf_obj Can be initialized with a sdf_object as parameter.
        """
        super(SDFBrowser, self).__init__()
        try:
            with open(HOME + "/.sdf/browserdefaults.pkl", 'rb') as f:
                self.values = pickle.load(f)
        except FileNotFoundError:
            with open(HERE + "/../browserdefaults.pkl", 'rb') as f:
                self.values = pickle.load(f)
        self.init_model(sdf_obj)
        self.setStyleSheet(style_sheet)
        self.initUI()

    def initUI(self):
        """
        Initializes all widgets (buttons, labels, etc.) displayed
        on this widget.
        """        
        # load size and position of last usage
        rect = QtCore.QRect(*self.values['display']['geometry'])
        self.setGeometry(rect)
        self.move(rect.topLeft())
        # set title bar
        self.setWindowTitle('SDFBrowser')
        # self.setWindowIcon(QtGui.QIcon('/home/ikuhlemann/Downloads/Zombie.png'))
        
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox.addLayout(vbox)
        self.setLayout(hbox)

        self.treeview = CustomTreeView(self)

        self.treeview.setModel(self.model)
        ## enable HTML syntax for styling of visible text:
        # self.treeview.setItemDelegate(HTMLDelegate(self))
        
        # self.treeview.selectionChanged.connect(self.handle_selection)
        # self.treeview.connect(self.treeview,
        # QtCore.SIGNAL("selectionChanged(QItemSelection&, QItemSelection&)"),
        # self.handle_selection)
        vbox.addWidget(self.treeview)

        hbox_open = QHBoxLayout()
        btn_open_sdf = QPushButton("open sdf")
        btn_open_sdf.clicked.connect(self.do_open)
        hbox_open.addWidget(btn_open_sdf)
        hbox_open.addStretch(1)
        vbox.addLayout(hbox_open)

        vbox_details = QVBoxLayout()
        hbox.addLayout(vbox_details)
        ## ------------------------------------
        #      Summary widget
        ## ------------------------------------
        self.summary_widget = SummaryWidgetController()
        vbox_details.addWidget(self.summary_widget)

        ## ------------------------------------
        #      Data preview widget
        ## ------------------------------------
        self.data_preview_widget = DataPreviewWidgetController()
        vbox_details.addWidget(self.data_preview_widget)

    def init_model(self, sdf_obj):
        """
        Initializes the model.
        Creates the TreeViewModel and an empty root node (workspace).
        @param sdf_obj Initial sdf_object or None.
        """
        root_node = sdf_object('ws')
        root_node.SetName("root")
        self.model = qt_sdf_model.TreeViewModel(root_node)
        if sdf_obj:
            self.model.parse_sdf_obj(sdf_obj)

    def do_open(self):
        raise NotImplementedError("needs to be implemented in inheriting class")
