"""
-------------------------------------------------------------------------
Project: SDF: Standard Data Format

Module: sdf_owner.py

Class sdf_owner: A class for SDF <owner> objects wich are sibblings
                of the sdf_enc_string class.

bg 14.09.2015 : Completely remodeled class hierarchy

-------------------------------------------------------------------------
    Copyright (C) 2010-2015 Burkhard Geil, Ilyas Kuhlemann, Filip Savic

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
from .sdf_enc_string import *


class sdf_owner(sdf_enc_string):
    """
    A class for all <owner> objects in the SDF project.

    An sdf_owner is always an encoded string, that will be enclosed in
    the <owner>-tag when exported to XML. 
    """

    def __init__(self,val=None, encoding='utf-8'):
        """ 
        Create an sdf_owner object. 
        """
        super(sdf_owner,self).__init__(val, encoding)
        self.ID = 'sdf-owner'

    def __str__(self):
        """
        Printable representation of its contents. 
        """
        res = "OWNER = '%s'" % self.value
        res = res + '\n'
        return res



    def AsXML(self, indent=0, lw=1000000):

        ret = ''
        word = ' '*indent + '<owner'
        if self.encoding != 'utf-8':
            word = word + ' encoding="' + self.encoding + '" >'
        else:
            word = word + '>'
        ret = ret + word + '\n'

        ret = ret + (sdf_enc_string.AsXML(self, indent=indent+sdf_rc._tabsize))

        ret = ret + '\n' + ' '*indent + '</owner>'
        
        return ret

    
