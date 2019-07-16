"""
Load SDF files.
------------------------------------------------------------------------------
    Copyright (C) 2015-2019 Burkhard Geil, Ilyas Kuhlemann, Filip Savic

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
import xml.etree.ElementTree as ET
from .. import SDF


def sdf_load(fname):
    parser = ET.XMLParser(encoding="utf-8")
    tree = ET.parse(fname, parser=parser)
    root = tree.getroot()
    if root.tag == 'workspace':
        root_obj = SDF.sdf_object('ws')
    elif root.tag == 'dataset':
        root_obj = SDF.sdf_object('ds')
    else:
        msg = "can't extract object type (workspace or dataset) from root of ElementTree!"
        raise RuntimeError(msg)
    root_obj.FromXML(root)    
    return root_obj
