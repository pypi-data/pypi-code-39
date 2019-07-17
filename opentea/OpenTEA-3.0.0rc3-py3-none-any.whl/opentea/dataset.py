#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""dataset.py

Implementation of the Dataset class to hold the TCL/Tk memory in the Python
memory.

Created Nov 2016 by COOP team
"""



__all__ = ["Dataset"]

import os
import codecs
import logging
import warnings


from collections import OrderedDict
from xml.parsers.expat import ExpatError
from xml.dom.minidom import parse

from .path_tools import PathTools
from .exceptions import (OTNoNodeException, OTTooManyNodesException,
                         OTException)


class Dataset():
    """Holder class for the interface memory

    This class holds the TCL/Tk memory in Python memory, for reading and
    writing by the OpenTEA python library.  The exchange format with the TCL
    engine is XML, and therefore this class also implements parsing from XML
    and dumping to it.
    """

    def __init__(self, xmlfile):
        self.log = logging.getLogger(__name__)
        self._xml_file = xmlfile
        try:
            self._dom = parse(self._xml_file)
        except IOError as err:
            self.log.error("Could not parse XML file.")
            self.log.error("%s couldn't be read", xmlfile)
            self.log.error(err)
            raise IOError(err)
        except ExpatError as err:
            self.log.error(err)
            xml_file_id = open(self._xml_file, "r").read().split("\n")
            self.log.error("--> %s", xml_file_id[err.lineno + 1])
            self.log.error(" " * (4 + err.offset) + "^")
            self.log.error("%s from c3sm wasn't correct xml"
                           "Remark : check that you have enough "
                           "free space or permission. ", xmlfile)
            raise ExpatError(err)
        self._root = self._dom.documentElement
        self._current_node = self._root

    def __repr__(self):
        return self._printNode()

    def _printNode(self, sep=''):
        """Recursive private method to describe the content of the dataset for
        debugging purposes
        """
        desc = ""
        node = self._current_node
        if node.nodeType == 1:
            desc += sep + node.nodeName + ' >> '
            for _, valeur in list(node.attributes.items()):
                desc += ' ' + valeur + '   '
            desc += "\n"
        for child in node.childNodes:
            self._current_node = child
            desc += self._printNode(sep + '   ')
            self._current_node = node
        return desc

    def _getTags(self, tag_list):
        node = self._current_node
        if node.nodeType == 1:
            tag_list.append(node.nodeName)
        for child in node.childNodes:
            self._current_node = child
            tag_list = self._getTags(tag_list)
            self._current_node = node
        return tag_list

    def _getNode(self, key, *path):
        try:
            return self._searchNode(key, *path)
        except OTTooManyNodesException:
            solver_node = self.getValue("callingAddress", "action", "meta")
            solver_node = solver_node.split(".")[1]
            return self._searchNode(key, solver_node, *path)

    def _searchNode(self, key, *path):
        """ This private method needs a key to search a node with name=key
        If no node is found, an Exception is raisen
        If one node is found, an Element is returned
        If more than one node is, the most relevant one (according to path) is
        chosen and returned as an Element

        path is a list of keyword"""

        result = self._dom.getElementsByTagName(key)
        if result.length == 0:
            raise OTNoNodeException(
                "OTError : no node found with key " +
                str(key) +
                " and path containing " +
                str(path))
        else:
            result_to_del = []
            for i, elt in enumerate(result):
                address = self._getAddress(elt)
                for elt_path in path:
                    if elt_path not in address:
                        result_to_del.append(i)
                        break
            # Now, the result should be exactly one item long
            # Raising OTNoNodeException or OTTooManyNodesException
            result_to_del.sort(reverse=True)
            for i in result_to_del:
                del result[i]

            if result.length == 1:
                return result[0]

            if result.length == 0:
                raise OTNoNodeException(
                    "OTError : no node found with key " +
                    str(key) +
                    " and path containing " +
                    str(path))

            # several addresses matches. If the address
            # is comprehesive, OK, else, exception
            # print "!! Several node matches, search for a perfect match "
            pathkey = list(path)
            pathkey.append(key)
            for elt in result:
                address = self._getAddress(elt)
                # print ">>> looking for ",pathkey ," .vs.", address
                test = True
                for node1, node2 in zip(pathkey, address):
                    if node1 != node2:
                        test = False

                if test is True:
                    # print ">>> match found"
                    return elt

            err_msg = ("OTError :"
                       + str(result.length)
                       + " nodes found with key '"
                       + str(key)
                       + "' and path "
                       + str(path)
                       + " :\n")

            for elt in result:
                err_msg += str(self._getAddress(elt)) + "\n"
            raise OTTooManyNodesException(err_msg)

    @staticmethod
    def _getAddress(node):
        """ This private method constructs the address of a node in the DOM"""
        parents = []

        security = 100
        while node.nodeName != '#document':
            security -= 1
            if security == 0:
                raise OTException(
                    "Infinite loop while searching for all the parents ...")

            parents.insert(0, node.nodeName)
            node = node.parentNode
        return parents

    def addChild(self, nodeName, value, fatherName, *path):
        """Add new child node nodeName to node fatherName
        Raise error if child already exists
        (use removeNode is this is a problem)
        Return createdNode
        """
        if self.nodeExists(nodeName, fatherName, *path):
            self.log.error("Node %s already exists. addChild "
                           "only adds new nodes.", nodeName)
            raise OTException

        father_node = self._getNode(fatherName, *path)
        new_node = self._dom.createElement(str(nodeName))

        new_node = father_node.appendChild(new_node)
        if value != "":
            new_node.setAttribute("value", value)
        return new_node

    def nodeExists(self, nodeName, *path):
        """This method tests if the node exists"""
        try:
            self._getNode(nodeName, *path)
            return True
        except OTNoNodeException:
            return False

    def getValue(self, nodeName, *path):
        """
        Search for the node "nodeName" with elements of "path"
        in its path and return its value
        If node doesn't exist, OTNoNodeException will be raised

        It would be cleaner to use "path" as a list, instead of "*path",
        but this would change all the geValue calls :(
        To be evaluated later
        """
        node = self._getNode(nodeName, *path)
        return node.getAttribute("value")#.encode("utf-8")

    def tryGetValue(self, default, nodeName, *path):
        """getValue for nodeName if it exists, otherwise default"""
        return self.getValue(
            nodeName, *path) if self.nodeExists(nodeName, *path) else default

    def getListValue(self, key, *path):
        """Get value and return as list"""
        result = self.getValue(key, *path).split(';')
        return [] if (result == [""]) else result

    def getListDict(self, key, *path):
        """Extract a list value and return as dict"""
        list_dict = self.getListValue(key, *path)
        return dict(list(zip(list_dict[::2], list_dict[1::2])))

    def addToUniqList(self, element, key, *path):
        """Add an element to a list with unique occurrences"""
        element_list = set(self.getListValue(key, *path))
        element_list.add(element)
        self.setValue(";".join(element_list), key, *path)

    @staticmethod
    def getFileList(path, filter_search="", output="listonly"):
        """Backwards compat. See issue #38"""
        warnings.warn("getFileList should be called from PathTools",
                      DeprecationWarning)
        ptl = PathTools()
        return ptl.get_file_list(path, filter_search, output)

    def getSelection(self, key, *path):
        """Get selected values of a `selection` block"""
        selection_list = self.getValue(key, *path).split(';')
        sel_dict = dict(list(zip(
            selection_list[::2],
            [int(float(x)) for x in selection_list[1::2]])))
        return [k for k in sel_dict if sel_dict[k] == 1]

    def setValue(self, value, nodeName, *path):
        """
        This method searches for the node "nodeName" with
        elements of "path" in its path and change its value to "value"
        If the value is a python list, it's converted into a Tcl list
        """
        if isinstance(value, list):
            value2 = []
            for elt in value:
                value2.append(str(elt).strip())
            value = ";".join(value2)

        try:
            node = self._getNode(nodeName, *path)
            node.setAttribute("value", str(value))
        except OTException:
            self.log.warning(
                "Note : Could not find node %s for path %s. Skipping "
                "setValue", nodeName, str(path))

    def getChildrenName(self, nodeName, *path):
        """
        This method returns a list of the name
        of all the children of the node named "nodeName".
        If more than one node has the same name,
        parts of its path can be specified as for the getValue method
        """
        try:
            node = self._getNode(nodeName, *path)
        except OTNoNodeException:
            return ""

        # result=list()
        result = [
            child.nodeName for child in node.childNodes if child.nodeType == 1]
        # result.append(child.nodeName)

        return result

    def getMultipleDicts(self, nodeName, *path):
        """
        Get dictionaries associating patch names and identifier in a multiple
        """
        items = OrderedDict()
        names = OrderedDict()
        for child in sorted(self.getChildrenName(nodeName, *path)):
            items[self.getValue(child, nodeName, *path)] = child
            names[child] = self.getValue(child, nodeName, *path)
        return items, names

    def get_multiple(self, nodeName, *path):
        """Get a list of """
        return Multiple(self, nodeName, *path)

    def removeNode(self, nodeName, *path):
        """
        Remove the node named "nodeName".  If more than one node has the same
        name, parts of its path can be specified as for the getValue method
        """
        node = self._getNode(nodeName, *path)
        parent = node.parentNode
        parent.removeChild(node)

    def save2file(self, fileName):
        """
        Save the dataset to an XML file in the OpenTEA format
        """
        try:
            fid = codecs.open(fileName, "w", "utf-8")
            self._dom.writexml(fid, addindent="  ", encoding="utf-8")
            fid.close()
        except IOError:
            self.log.error(
                "Could not save XML content to file %s from %s.\n"
                "Check path, permissions and disk space",
                fileName, os.getcwd())


class Multiple():
    """Container class for `multiple` widget data"""
    def __init__(self, dataset, node_name, *path):
        self.dts = dataset
        self.ids = self.dts.getChildrenName(node_name, *path)
        assert all([node[:5] == "item_" for node in self.ids]), (
            "Node " + node_name + " does not seem to be a multiple")
        self.headers = []
        self.rows = []
        self._read_headers()
        self._read_rows()

    def _read_headers(self):
        """Read headers from the first line found in the multiple"""
        self.headers = ["label"] + self.dts.getChildrenName(self.ids[0])

    def _read_rows(self):
        """Read full data from multiple"""
        for identifier in self.ids:
            entry = [self.dts.getValue(identifier)]
            entry += [self.dts.getValue(header, identifier)
                      for header in self.headers[1:]]
            self.rows.append(entry)

    @property
    def _columns_widths(self):
        """Widths of all columns for pretty printing"""
        lengths = []
        for i, col in enumerate(self.columns):
            lengths.append(max(len(entry)
                               for entry in [self.headers[i]] + col))
        return lengths

    def _format_line(self, line):
        """Format a line according to max column lengths"""
        formatters = ["{0:" + str(wid) + "}" for wid in self._columns_widths]
        return " | ".join(formatters[i].format(entry)
                          for i, entry in enumerate(line))

    @property
    def columns(self):
        """Transposed view of self.rows"""
        return [list(l) for l in zip(*self.rows)]

    def keys(self):
        """List of available keys for mul["label"]-like access"""
        return self.headers + self.columns[0]

    def __str__(self):
        """What is shown when `print` is called"""
        out = [self._format_line(self.headers),
               "---".join("-"*i for i in self._columns_widths)]
        out += [self._format_line(line) for line in self.rows]
        return "\n".join(out)

    def __getitem__(self, key):
        """Smart overload of __getitem__

        mul["my_label"] should give the line with Label `my_label`
        mul["label"] should give the matching column
        """
        key = key.lower()
        if key in self.headers:
            index = self.headers.index(key)
            return self.columns[index]
        if key in self.columns[0]:
            index = self.columns[0].index(key)
            return self.rows[index]
        raise KeyError(key)

    def order_by(self, header):
        """Reorder lines using a header"""
        header = header.lower()
        assert header in self.headers
        column = self.columns[self.headers.index(header)]
        new_order = sorted(list(range(len(column))), key=column.__getitem__)
        self.ids = [self.ids[i] for i in new_order]
        self.rows = [self.rows[i] for i in new_order]
