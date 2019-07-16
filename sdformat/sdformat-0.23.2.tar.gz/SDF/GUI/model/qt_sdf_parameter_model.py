## @author Ilyas Kuhlemann
# @contact ilyasp.ku@gmail.com
# @date 08.08.16

"""
@package SDF.GUI.qt_sdf_parameters_model
THIS IS NOT REALLY WORKING YET, IT IS MORE LIKE A DRAFT 
OR AN IDEA FOR NOW. IT STILL THROWS A LOT OF ERRORS ...

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
-----------------------------------------------------------------------------------

Contains the implementation of a model (to be used by Qt's Model/View system) to make 
sdf_par instances of sdf_objects (workspaces and datasets) accessible by QTreeView.

This is to be used in SDF.GUI.sdf_parameters_browser, where the QTreeView widget gets implemented.
"""
from PyQt5 import QtCore
import logging


class ParameterTreeViewModel(QtCore.QAbstractItemModel):
    def __init__(self, root, parent=None):
        super(ParameterTreeViewModel, self).__init__(parent)
        self.is_editable = False
        self.is_selectable = True
        self.is_enabled = True
        self.root_node = root

    #############################################################
    # This section contains functions overwriting standard 
    # functions of QtCore.QAbstractItemModel.
    # Most of them are internally called to update the content
    # visible in a QtGui.QTreeView.
    #############################################################
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not role == QtCore.Qt.DisplayRole:
            return
        if index.column() == 0:
            return index.internalPointer().name.value
        elif index.column() == 1:
            if type(index.internalPointer().value) == list:
                return "parameter block"
            else:
                return index.internalPointer().value
        else:
            return

    def index(self, row, col, parent):
        """
        Get index of an item.
        Item is identfied by (row,col) coordinate and its parent.

        This function is called internally by views whenever
        something changes (expanding of tree node, etc.).
        @param row <int> Row of item.
        @param col <int> Column of item.
        @param parent <QModelIndex> Index of item's parent.
        @return <QModelIndex> Index of specified item.
        """
        if parent.isValid():
            parent_node = parent.internalPointer()
            logging.debug("parent valid")
        else:
            # in case of invalid index,
            # root node is considered parent
            parent_node = self.root_node
            logging.debug("parent NOT valid")            
        msg = "row = %i, len(parent_node.value) = %i" % (row, len(parent_node.value))
        logging.debug(msg)
        
        child_item = parent_node.value[row]
        # use model's function to create the desired QModelIndex
        index = self.createIndex(row, col, child_item)
        return index

    def parent(self, index):
        """
        Returns index pointing to parent node/sdf_par.
        @param index <QModelIndex> Index of current node/sdf_par.
        @return <QModelIndex> Index of parent node/sdf_par.
        """
        node = self.get_item(index)
        parent_node = node.parent_par
        if parent_node == self.root_node or parent_node is None:
            return QtCore.QModelIndex()
        else:
            return self.createIndex(parent_node.value.index(node), 0, parent_node)

    def rowCount(self, parent):
        """
        Get number of rows belonging to this parent, i.e. number
        of children of given parent.
        @param parent <QModelIndex> Index of parent.
        """
        if parent.isValid():
            parent_node = parent.internalPointer()
        else:
            parent_node = self.root_node

        if type(parent_node.value) == list:
            return len(parent_node.value)
        else:
            return 0

    def columnCount(self, parent):
        """
        Number of columns for children of given parent.
        At the moment, there are only two columns shown
        per sdf_par: the name/key in first column,
        the value in the second column 
        --> This function returns 2,
        i.e. number of columns displayed.
        """
        return 2

    def insertRows(self, position, n_nodes, parent_index):
        """
        Insert items into the Model, as children of given parent.

        As I understand it, this function merely adds the appropriate
        indices as valid indices to the model.

        @param position <int> Starting index where to insert the
        number of nodes (in my model: there is no difference
        where you start, as long as position is a valid index,
        i.e. it does not exceed the number of already added
        child items).
        @param n_nodes <int> Number of children to add.
        @param parent_index <QModelIndex> Index pointing to item
        that is parent of the items to be added.
        """
        self.beginInsertRows(parent_index, position, position + n_nodes - 1)
        self.endInsertRows()
        return 1

    def headerData(self, section, orientation, role):
        if not role == QtCore.Qt.DisplayRole:
            return
        if section == 0:
            return "Key"
        elif section == 1:
            return "Value"
        return str(section)

    #############################################################
    # Here begins the section of custom functions, that do not
    # overwrite functions present in QtCore.QAbstractItemModel.
    #############################################################
    def get_item(self, index):
        """
        Function to get the item pointed to by given index.
        @param index <QModelIndex> Index pointing to desired node.
        """
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self.root_node

    def parse_list_of_sdf_par(self, list_of_sdf_par):
        """
        Functions maps a root sdf_par list to the model, 
        to display it with PyQt's QTreeView.
        @param sdf_obj Root sdf_object.
        """
        import numpy as np
        name = str(np.random.rand())
        name = "root"
        self.root_node.Set(name, list_of_sdf_par, None, self.root_node.parent_par)
        self.insertRows(len(self.root_node.value) - 1, 1, QtCore.QModelIndex())        
        logging.debug("Number of values under root: %i", len(self.root_node.value))
