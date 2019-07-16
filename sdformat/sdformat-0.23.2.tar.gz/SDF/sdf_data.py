"""
-------------------------------------------------------------------------
Project: SDF: Standard Data Format

Module: sdf_data.py

Class sdf_data: A base class to respresent the data-blocks in SDF-files.
                Its only task is to introduce the 'type' of the data
                block.
 
bg 11.09.2015 : Completely remodeled class hierarchy
bg 15.09.2015 : Concept of this class

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

from .sdf_base import sdf_base
from . import sdf_rc


class sdf_data(sdf_base):
    """
    A base class for all <data> objects in the SDF project.
    
    From this base class the <data> objects only inherit the 'type'
    attribute which must be one of the types defined in sdf_rc.py.
    """    
    # ---------------------------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------------------------
    def __init__(self, datatype='unknown'):
        """
        Create an empty sdf_data object.
        """
        super(sdf_data, self).__init__()
        self.ID = 'sdf-data'
        self.datatype = datatype

    # ---------------------------------------------------------------------------
    # Setter Functions
    # ---------------------------------------------------------------------------
    def Set(self, datatype=None):
        """
        Set values of the sdf_data class

        TODO:   Don't know if this function should be setting the datatype, as in
                classes derived from this one the overwritten Set function sets
                the data.
        """
        self.datatype = datatype
        
    # ---------------------------------------------------------------------------
    # Getter Functions - Need to be overridden
    # ---------------------------------------------------------------------------        
    def __str__(self):
        """
        Printable representation of its contents. 
        """
        res = "TYPE = '%s'" % self.datatype
        res = res + '\n'
        return res

    def Get(self):
        """
        Return a tuple with the contents
        """
        return (self.datatype,)
        
    def GetType(self):
        """
        Return the type of the data-block
        """
        return self.datatype
        
    def AsXML(self, indent=0, lw=1000000):
        raise NotImplementedError()

    def FromXML(self, etree_node):
        """
        Create an sdf_data block from an XML ElementTree node.
        """
        pass 

    # ---------------------------------------------------------------------------
    # Other Stuff - TODO: IsValid 
    # ---------------------------------------------------------------------------        
    def IsValid(self):
        """
        Check if the contents of this class are valid.
        """
        return self.datatype in sdf_rc.KNOWN_DATA_TYPES
        
    def IsEmpty(self):
        """
        Check if this class instance is empty
        """
        pass
