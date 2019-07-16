"""
-------------------------------------------------------------------------
Project: SDF: Standard Data Format

Module: sdf_sample.py

Class sdf_sample: Class that respresents the sample-tag in SDF-files
                  Contains an instance of the name and comment class of SDF.
 
bg 11.09.2015 : Completely remodeled class hierarchy
fs 14.09.2015 : Written draft of sdf_sample-class

-------------------------------------------------------------------------
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

from .sdf_base import *
from .sdf_name import *
from .sdf_comment import *
from .sdf_rc import *

class sdf_sample(sdf_base):
    """
    A class for all <sample> objects in the SDF project.
    
    A sample contains a <name> object and possibly multiple <comment> objects
    (Not yet implemented), that will be enclosed in <sample>-tags when exported
    as XML.
    """
    
    #---------------------------------------------------------------------------
    # Constructor
    #---------------------------------------------------------------------------
    def __init__(self, name=None, comment=None, encoding='utf-8'):
        """
        Create an empty sdf_sample object.
        """
        super(sdf_sample,self).__init__()
        self.ID = 'sdf-sample'
        self.name    = sdf_name(val=name, encoding=encoding)
        self.comment = sdf_comment(val=comment, encoding=encoding)

    #---------------------------------------------------------------------------
    # Setter Functions
    #---------------------------------------------------------------------------
    def Set(self, name=None, comment=None, encoding='utf-8'):
        """
        Set the comment and name together
        """
        self.name.Set(name, encoding)
        self.comment.Set(comment, encoding)
        
    def SetName(self, name=None, encoding='utf-8'):
        """
        Set the name independently
        """
        self.name.Set(name, encoding)
        
    def SetComment(self, comment=None, encoding='utf-8'):
        """
        Set the comment independently
        """
        self.comment.Set(comment, encoding)

    #---------------------------------------------------------------------------
    # Getter Functions - Need to be overridden
    #---------------------------------------------------------------------------

    def __str__(self):
        """
        Printable representation of its contents. 
        """
        res = 'SAMPLE ' + str(self.name)
        res = res + '       ' + str(self.comment)
        return res

        
    def Get(self):
        """
        Return the name and comment in this class
        """
        return (self.name.Get(), self.comment.Get())
        
    def GetName(self):
        """
        Return the content of name, calling the Get-Function of the name
        """
        return self.name.Get()
        
    def GetComment(self):
        """
        Return the content of comment, calling the Get-Function of the comment
        """
        return self.comment.Get()

    #---------------------------------------------------------------------------
    # Other Stuff - TODO: IsValid 
    #---------------------------------------------------------------------------        
    def IsValid(self):
        """
        Check if the contents of this class are valid.
        """
        print("Error: Not yet implemented.")
        exit -1
        
    def IsEmpty(self):
        """
        Check if this class is empty, i.e. that name and comment are None.
        """
        return (self.name.Get() is None) and (self.comment.Get() is None)

        
    def Contains(self, string):
        """
        Check if either name or comment contain the given string.
        This function has to check first if either or both of them are
        empty, i.e. None
        """
        if self.IsEmpty():
            print("Error: sdf_sample is empty.")
            return
            
        elif self.name.Get() is None:
            return string in self.comment.Get()
            
        elif self.comment.Get() is None:
            return string in self.name.Get()
            
        return (string in self.name.Get()) or (string in self.comment.Get())

    #---------------------------------------------------------------------------
    # XML Output
    #---------------------------------------------------------------------------            
    def AsXML(self, indent=0, lw=1000000):
        
        if self.IsEmpty():
            return
        
        ret  = ''
        word = ' '*indent + '<sample>'
            
        ret = ret + word + '\n'
        
        if self.name.Get() is not None:
            ret = ret + (self.name.AsXML(indent=indent + sdf_rc._tabsize))
                                         
        ret = ret + '\n'
                                         
        if self.comment.Get() is not None:
            ret = ret + (self.comment.AsXML(indent=indent + sdf_rc._tabsize))
        
        ret = ret + '\n' + ' '*indent + '</sample>'
        
        return ret


    def FromXML(self,etree_node):
        """
        Create an sdf_sample instance from an XML ElementTree node.
        """
        for child in etree_node:
            if child.tag == 'name':
                self.name.FromXML(child)
            if child.tag == 'comment':
                self.comment.FromXML(child)


