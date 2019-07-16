"""
-------------------------------------------------------------------------
Project: SDF: Standard Data Format

Module: sdf_comment.py

Class sdf_comment: A class for SDF <comment> objects wich are sibblings
                of the sdf_enc_string class.

bg 14.09.2015 : Completely remodeled class hierarchy

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
from .sdf_enc_string import *


class sdf_comment(sdf_enc_string):
    """
    A class for all <comment> objects in the SDF project.

    An sdf_comment is always an encoded string, that will be enclosed in
    the <comment>-tag when exported to XML. 
    """

    def __init__(self,val=None, encoding='utf-8'):
        """ 
        Create an sdf_comment object. 
        """
        super(sdf_comment,self).__init__(val, encoding)
        self.ID = 'sdf-comment'

    def __str__(self):
        """
        Printable representation of its contents. 
        """
        res = "COMMENT = '%s'" % self.value
        res = res + '\n'
        return res


    def Append(self,text):
        """
        Append text to a comment creating a new "paragraph".
        """
        self.value = self.value + ' <p/>'    # avoid encoding here!
        super(sdf_comment,self).Append(text) # this is encoded again.

    def AsXML(self, indent=0, lw=1000000):

        ret = ''
        word = ' '*indent + '<comment'
        if self.encoding != 'utf-8':
            word = word + ' encoding="' + encoding + '" >'
        else:
            word = word + '>'
        ret = ret + word + '\n'

        ctext =  super(sdf_comment, self).AsXML(indent=indent + sdf_rc._tabsize)
        ctext = ctext.replace('<br/>', '<br/>\n')
        ctext = ctext.replace('<p/>', '\n<p/>\n')
        
        lines = ctext.split('\n')
        for line in lines:
            
            ret = ret + ' '*(indent+sdf_rc._tabsize) \
                  + line.strip() + '\n' 
        ret = ret + ' '*indent + '</comment>' 
        
        return ret

    
