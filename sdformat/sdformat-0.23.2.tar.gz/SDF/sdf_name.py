"""
-------------------------------------------------------------------------
Project: SDF: Standard Data Format

Module: sdf_name.py

Class sdf_name: A class of all SDF <name> objects wich are sibblings
                of the sdf_enc_string class.

bg 11.09.2015 : Completely remodeled class hierarchy

-------------------------------------------------------------------------
    Copyright (C) 2010-2019 Burkhard Geil, Ilyas Kuhlemann, Filip Savic

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

from . import sdf_rc
from .sdf_enc_string import sdf_enc_string


class sdf_name(sdf_enc_string):
    """
    A class for all <name> objects in the SDF project.

    An sdf_name is always an encoded string, that will be enclosed in
    the <name>-tag when exported to XML. 
    """

    def __init__(self, val=None, encoding='utf-8'):
        """ 
        Create an sdf_name object. 
        """
        
        super(sdf_name, self).__init__(val, encoding)
        self.ID = 'sdf-name'

    def __str__(self):
        """
        Printable representation of its contents. 
        """
        res = "NAME = '%s'" % self.value
        res = res + '\n'
        return res

    def AsXML(self, indent=0, lw=1000000):
        ret = ''
        word = ' ' * indent + '<name'
        if self.encoding != 'utf-8':
            word = word + ' encoding="' + self.encoding + '" >'
        else:
            word = word + '>'
        ret = ret + word + '\n'

        ret = ret + (sdf_enc_string.AsXML(self, indent=indent + sdf_rc._tabsize))
        ret = ret + '\n' + ' ' * indent + '</name>'        
        return ret
