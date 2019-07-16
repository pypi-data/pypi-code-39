"""
-------------------------------------------------------------------------
Project: SDF: Standard Data Format

Module: sdf_string.py

Class sdf_string: The base class of all SDF string-objects that
                  will be used as 'normalized strings'. 
 
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
from .sdf_gen_val import sdf_gen_val


class sdf_string(sdf_gen_val):
    """
    Base class for all string objects in the SDF project.

    An sdf_string is always a 'normalized' string with all
    line breaks removed and all unnecessary white spaces
    removed.
    """
    def __init__(self, val=None):
        """ 
        Create an sdf_string object. 
        """
        nval = sdf_utils.NormalizeWhiteSpace(val)
        super(sdf_string, self).__init__(nval)
        self.ID = 'sdf-string'

    def __str__(self):
        return self.value

    def __add__(self, obj):
        return self.value + ' ' + sdf_string(obj).value

    def Set(self, val):
        """
        Set the value of an sdf_string. 

        'Normalize' the input string 'val' by removing all
        line breaks and reducing multiple white space to a
        single white space.
        """
        self.value = sdf_utils.NormalizeWhiteSpace(val)

    def Append(self, text):
        """
        Append 'text' (which must be a string).
        """
        self.value = self.value + ' ' + sdf_utils.NormalizeWhiteSpace(text)

    def AsXML(self, indent=0, lw=1000000):
        """
        Return the value of the sdf_string object with all
        letters reserved for XML (& < > " ') replaced by 
        their XML entities (&amp; &gt; &lt; &quot; &apos).

        Use the sdf_string.Get() function to obtain the 'raw'
        sdf_string.
        """
        lines = self.value.splitlines()
        ret = ''
        first_line = True
        for line in lines:
            line = sdf_utils.xml_encode(line)
            if not first_line:
                ret = ret + '\n'
            ret = ret + ' ' * indent + line
            if first_line:
                first_line = False
        return ret

    def FromXML(self, XMLtext):
        """
        Import a string from XML encoding. This is the opposite
        of the AsXML() function. It replaces all entities
        (&amp; &gt; &lt; &quot; &apos) with (& < > " ').

        Use the sdf_string.Set() function if you want to avoid 
        this translation.
        """
        temp = sdf_utils.xml_decode(XMLtext)
        # use Set() to perform an optional normalization:
        self.Set(temp)

    def IsValid(self):
        """
        Check validity of an sdf_string object. It is invalid
        if it is not a normalized string.
        """
        if not isinstance(self.value, str):
            return False
        if ('  ' in self.value):
            return False
        if ('\n' in self.value):
            return False
        return True
