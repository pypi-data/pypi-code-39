"""
@package SDF.GUI.qt_sdf_model

Contains the implementation of a model (to be used by Qt's Model/View system) to make 
sdf_objects (workspaces and datasets) accessible by QTreeView.

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
--------------------------------------------------------------------------------

Large parts of this file copied and adapted from stackoverflow user 
cloudformdesign's example provided in http://stackoverflow.com/a/20085471/5829566 . 
Example file on his github account: 
https://github.com/vitiral/cloudtb/blob/old/extra/PyQt/treeview.py .
"""
from PyQt5 import QtCore


class TreeViewModel(QtCore.QAbstractItemModel):
    """
    This model allows displaying of sdf_objects (workspaces and datasets) in PyQt4's QTreeView.
    
    Reimplementation of QAbstractItemModel, to tell QTreeView what to make of an sdf_object.
    QTreeView uses functions like data, index, parent, to navigate along a tree-like object
    and display the data of nodes. 
    """    
    def __init__(self, root, parent=None):
        """
        Constructor.
        @param root Root node, i.e. empty sdf_object (workspace) pointing to 
        the top-level of a real (not empty) sdf_object.
        @param parent Parent. (? Widget ?)

        @todo Figure out what parent actually is.
        """
        super(TreeViewModel, self).__init__(parent)
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
        """
        Reimplementation of QAbstractItemModel.data.

        This function is called by views (like QTreeView) to access
        data (only strings?) of nodes. 
        Only one role is implemented, QtCore.Qt.DisplayRole. It is 
        used to populate the columns of the QTreeView with text.
        Other roles could be used for tool tips and what not.

        @param index <QModelIndex> Position of given object.
        @param role <int> Specifying what data is to be accessed.
        """
        if role == QtCore.Qt.DisplayRole:            
            if index.column() == 0:
                # return "<b>"+index.internalPointer().name.value+"</b>"
                return index.internalPointer().name.value
            elif index.column() == 1:
                return self.create_sdf_summary(index.internalPointer())
            else:
                return

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
        else:
            # in case of invalid index,
            # root node is considered parent
            parent_node = self.root_node
        try:
            child_item = parent_node.GetChild(row)
        except IndexError:
            child_item = None
        
        # use model's function to create the desired QModelIndex
        index = self.createIndex(row, col, child_item)

        return index

    def parent(self, index):
        """
        Returns index pointing to parent node/sdf_object.
        @param index <QModelIndex> Index of current node/sdf_object.
        @return <QModelIndex> Index of parent node/sdf_object.
        """
        node = self.get_item(index)
        parent_node = node.parent
        
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
        if parent_node.IsWorkspace():
            return len(parent_node.value)
        else:
            return 0

    def columnCount(self, parent):
        """
        Number of columns for children of given parent.
        At the moment, there are only two columns shown
        per sdf_object: the name/type in first column,
        a summary of number of children and parameters
        in second column. --> This function returns 2,
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
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "[type] Name"
            elif section == 1:
                return "Summary"
            return str(section)
        return

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

    def create_sdf_summary(self, sdf_obj):
        """
        Create a summary text of an sdf_object to be displayed 
        in the second column of the QTreeView.
        """
        ret = ''
        if sdf_obj.IsDataset():
            if sdf_obj.value.ID == 'sdf-data-sc':
                ret = ret + 'single-column data of length %i, ' % sdf_obj.value.data.shape[0]
            elif sdf_obj.value.ID == 'sdf-data-mc':
                ret = ret + 'data array of shape ' + str(sdf_obj.value.shape) + ', '
            elif sdf_obj.value.ID == 'sdf-data-img':
                ret = ret + 'image data, '
            
        elif sdf_obj.IsWorkspace():
            n_ws = 0
            n_ds = 0
            for c in sdf_obj.value:
                if c.IsWorkspace():
                    n_ws += 1
                elif c.IsDataset():
                    n_ds += 1
            ret = ret + 'contains %i workspaces, %i datasets, ' % (n_ws, n_ds)

        if len(sdf_obj.instrument) == 1:
            ret = ret + str(len(sdf_obj.instrument)) + ' instrument, '
        elif len(sdf_obj.instrument):
            ret = ret + str(len(sdf_obj.instrument)) + ' instruments, '
        if len(sdf_obj.sample) == 1:
            ret = ret + str(len(sdf_obj.sample)) + ' sample, '
        elif len(sdf_obj.sample):
            ret = ret + str(len(sdf_obj.sample)) + ' samples, '
        if len(sdf_obj.par) == 1:
            ret = ret + str(len(sdf_obj.par)) + ' parameter'
        elif len(sdf_obj.par):
            ret = ret + str(len(sdf_obj.par)) + ' parameters'        
        ret = ret.rstrip()
        ret = ret.rstrip(',')

        return ret    

    def parse_sdf_obj(self, sdf_obj):
        """
        Functions maps a root sdf-object (workspace that
        wraps the complete sdf-file) to the model, 
        to display it with PyQt4's QTreeView.
        @param sdf_obj Root sdf_object.
        """
        self.root_node.AppendObject(sdf_obj)
        self.insertRows(len(self.root_node.value) - 1, 1, QtCore.QModelIndex())
