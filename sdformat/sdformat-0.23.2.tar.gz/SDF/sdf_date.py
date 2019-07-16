"""
-------------------------------------------------------------------------
Project: SDF: Standard Data Format

Module: sdf_date.py

Class sdf_date: The class for  SDF date-objects.
 
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
import datetime
from . import sdf_rc
from . import sdf_utils
from .sdf_string import *


class sdf_date(sdf_string):
    """
    A class for date objects in the SDF project.
    """
    
    def __init__(self,datestring=None,format=sdf_rc.DEFAULT_DATE_FORMAT):
        """ 
        Create an sdf_date object. 
        """
        super(sdf_date,self).__init__(datestring)
        self.ID ='sdf-date'
        self.format = format

    def __str__(self):
        """
        Printable representation of its contents. 
        """
        res = "DATE = '%s'" % self.value
        res = res + '\n'
        return res



    def Set(self,datestring=None, format=sdf_rc.DEFAULT_DATE_FORMAT):
        """
        Set the value and/or the format-string of an sdf_date. 
        """
        self.value = datestring
        self.format = format

    def Append(self,text):
        """
        Does not exist for instances of sdf_date.
        """
        print('Warning: An instance of sdf_date has no Append()-function.')


    def AsXML(self, indent=0, lw=1000000):
        """
        Return the value of the date-object.
        """
        ret = ''
        word = ' '*indent + '<date'
        if self.format != sdf_rc.DEFAULT_DATE_FORMAT :
            word = word + ' format="' + self.format + '" >'
        else:
            word = word + '>'
        ret = ret + word + '\n'
        ret = ret + sdf_string.AsXML(self,
                                     indent=indent+sdf_rc._tabsize)
        ret = ret + '\n' + ' '*indent + '</date>'

        return ret


    def FromXML(self,etree_node):
        """
        Create an sdf_date instance from an XML ElementTree node.
        """
        if 'format' in etree_node.attrib:
            self.format = etree_node.attrib['format']
        else:
            self.format = sdf_rc.DEFAULT_DATE_FORMAT

        self.value = sdf_utils.NormalizeWhiteSpace(etree_node.text)
    


    def IsValid(self):
        """
        Check validity of an sdf_date object.
        """
        result = True
        try:
            a = datetime.strptime(self.value,self.format)
        except ValueError:
            result = False
        return result


    
