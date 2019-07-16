"""
-------------------------------------------------------------------------
Project: SDF: Standard Data Format

Module: sdf_data_mc.py

Class sdf_data_sc: A class to respresent a multi-column data-block in 
                   SDF-files.
 
ik 23.06.2016 : copied sdf_data_sc into this file and modified contents
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

import numpy as np
from .sdf_data import *
from . import sdf_rc
from . import sdf_utils

class sdf_data_mc(sdf_data):
    """
    A class for multi-column datasets in the SDF project.
    """
    
    #---------------------------------------------------------------------------
    # Constructor
    #---------------------------------------------------------------------------
    def __init__(self, data=np.array([]), dtype='float'):
        """
        Create an empty sdf_data_sc object.
        """
        if dtype not in sdf_rc.KNOWN_VALUE_TYPES:
            print('Error in sdf_data_sc constructor: unknown data type:', end='')
            print(dtype)
            exit -1

        super(sdf_data_mc,self).__init__('mc')
        self.ID = 'sdf-data-mc'
        self.data = np.array(data)  # array with values
        self.shape = data.shape   # number of values
        self.dtype = dtype         # type of the data values (see sdf_rc.py)

    #---------------------------------------------------------------------------
    # Setter Functions
    #---------------------------------------------------------------------------
    def Set(self, data=np.array([]), dtype='float'):
        """
        Set values of the sdf_data_mc class
        """
        self.data = np.array(data)  # array with values
        self.shape = data.shape   # number of values
        self.dtype = dtype         # type of the data values (see sdf_rc.py)


        
    #---------------------------------------------------------------------------
    # Getter Functions - Need to be overridden
    #---------------------------------------------------------------------------        
    def __str__(self):
        """
        Printable representation of its contents. 
        """
        res = "DATA TYPE = %s, (%s)" % (self.datatype, self.dtype)
        res = res + " shape = " +str(self.shape) + "\n"
        res = res + str(self.data)
        return res

    def AsXML(self, indent=0, lw=1000000):
        
        ret = ' '*indent + "<data shape='"+str(self.shape)+"' type='%s' >" % self.dtype + '\n'
            
        textblock = ' ' * (indent + sdf_rc._tabsize)
        
        if len(self.shape) == 2:
            for i in range(self.shape[0]):
                for j in range(self.shape[1]):
                    textblock = textblock + ' ' + str(self.data[i,j])
                textblock = textblock + '\n' + ' ' * (indent + sdf_rc._tabsize)
            textblock = textblock.rstrip() + "\n"
            ret = ret + textblock

        else:
            for d in self.data.flat:
                textblock = textblock + ' ' + str(d)
            ret = ret + ' '*(indent+sdf_rc._tabsize) + textblock + '\n'
                                                 
        ret = ret + ' '*indent + '</data>'
        
        return ret

    def FromXML(self, etree_node):
        """
        Create an sdf_data_mc block from an XML ElementTree node.
        @todo This is still as copied from single-column data!
        """
        
        namespace = {}
        sshape = etree_node.attrib['shape']
        sshape = sshape.replace('L', '')
        exec("shape = "+sshape, namespace)
        self.shape = namespace['shape']

        if 'dtype' in etree_node.attrib:
            # this is one of the sdf_rc.KNOWN_VALUE_TYPES:
            # ('byte', 'int', 'float')
            self.dtype = etree_node.attrib['dtype']
    
        words = etree_node.text.split()

        if self.dtype == 'float':
            self.data = np.zeros(self.shape, dtype='float')
            
            for counter in range(len(words)):
                self.data.flat[counter] = float(words[counter])

        elif self.dtype == 'int':
            self.data = np.zeros(self.shape, dtype='int')
            
            for counter in range(len(words)):
                self.data.flat[counter] = int(words[counter])

        else:
            print('Error: data type "%s" in "%s" files not (yet) supported.'\
                % (self.dtype, self.datatype))
            return
        

    def Get(self):
        """
        Return a tuple with the contents
        """
        return (self.data, self.dtype)
        
    def GetType(self):
        """
        Return the type of the data-block
        """
        return self.dtype
        
    #---------------------------------------------------------------------------
    # Other Stuff - TODO: IsValid 
    #---------------------------------------------------------------------------

    def IsValid(self):
        """
        Check if the contents of this class are valid.
        """
        pass
        
    def IsEmpty(self):
        """
        Check if this class instance is empty
        """
        pass

        
