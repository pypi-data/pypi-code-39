"""
Treeview used in SDF browser.
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

from PyQt5.QtWidgets import QTreeView


class CustomTreeView(QTreeView):
    """
    Custom implementation of a QTreeView.
    Main reason for implementation was to get the selectionChanged 
    signal working.

    It is based on question and answer by stackoverflow user bvz
    in the following thread:
    http://stackoverflow.com/questions/4160111/pyqt-qtreeview-trying-to-connect-to-the-selectionchanged-signal
    """
    def __init__(self, parent_browser=None):
        super(CustomTreeView, self).__init__(parent_browser)
        self.parent_browser = parent_browser
            
    def setModel(self, model):
        """
        This is the important part: on call of 
        setModel, the function of QTreeView is called
        unaltered, followed by a connection of the 
        selectionChanged signal using the current selectionModel.
        """
        super(CustomTreeView, self).setModel(model)
        # self.connect(self.selectionModel(),
        #              QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"),
        #              self.selection_changed)

        self.selectionModel().selectionChanged.connect(self.selection_changed)

    def selection_changed(self, newSelection, oldSelection):
        self.parent_browser.summary_widget.\
            display_sdf_object(newSelection.indexes()[0].internalPointer())
        self.parent_browser.data_preview_widget.\
            display_sdf_object(newSelection.indexes()[0].internalPointer())
