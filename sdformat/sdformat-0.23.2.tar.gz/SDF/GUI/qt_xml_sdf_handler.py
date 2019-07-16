"""
Required for Qt XML Tree
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
from PyQt4 import QtXml

class SDFHandler(QtXml.QXmlDefaultHandler):
    
    def __init__(self,root):

        QtXml.QXmlDefaultHandler.__init__(self)
        
        self._root = root
        self._item = None
        self._text = ''
        self._error = ''

