"""
-------------------------------------------------------------------------
Project: SDF: Standard Data Format

Module: sdf_enc_string.py

Class sdf_string: The base class of all SDF string-objects that
                  will be used as 'normalized strings' and that 
                  have a specified encoding. 

!!! At the moment this class is a fake since it does not implement the
!!! string encoding. It serves as a placeholder in the SDF class 
!!! hierachy only.
 
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
from . import sdf_utils
from .sdf_string import sdf_string


class sdf_enc_string(sdf_string):
    """
    Base class for all encoded-string objects in the SDF project.

    An sdf_enc_string is always a 'normalized' string with all
    line breaks removed, all unnecessary white spaces removed, and
    that has a defined encoding.
    """    
    def __init__(self, val=None, encoding='utf-8'):
        """ 
        Create an sdf_enc_string object. 
        """
        if encoding not in sdf_rc.KNOWN_ENCODINGS:
            print('Error in sdf_enc_string construction:')
            print('   unknown encoding:', encoding)
            exit(-1)

        super(sdf_enc_string, self).__init__(val)
        self.ID = 'sdf-enc-string'
        self.encoding = encoding        

    def __str__(self):
        return self.value

    def __add__(self, obj):
        return self.value + ' ' + sdf_enc_string(obj).value

    def Set(self, val, encoding='utf-8'):
        """
        Set the value of an sdf_enc_string. 

        Creates self.value as an (normalized) sdf_string and
        sets the encoding of this string. 
        """
        if not val:
            self.value = None
            self.encoding = 'utf-8'
        elif encoding not in sdf_rc.KNOWN_ENCODINGS:
            print('Error in sdf_enc_string Set():')
            print('   unknown encoding:', encoding)
            return
        else:
            # 'normalize' the input string and set encoding:
            super(sdf_enc_string, self).Set(val)
            self.encoding = encoding

    def Append(self, text):
        """
        Append text.
        """
        # TODO: check that both encodings are the same or perform
        #       a translation.
        self.value = self.value + ' ' + sdf_enc_string(text).value

    def IsValid(self):
        """
        Check validity of an sdf_enc_string object. It is invalid
        if it is not a normalized string or if the encoding is not
        known.
        """
        if ((not isinstance(self.value, str)) or
            ('  ' in self.value) or 
            ('\n' in self.value)):
            return False
        if self.encoding not in sdf_rc.KNOWN_ENCODINGS:
            return False
        return True

    def FromXML(self, etree_node):
        """
        Create an sdf_enc_string from an XML ElementTree node.
        """
        if 'encoding' in etree_node.attrib:
            self.encoding = etree_node.attrib['encoding']
        else:
            self.encoding = 'utf-8'
        self.value = sdf_utils.NormalizeWhiteSpace(etree_node.text)

    
