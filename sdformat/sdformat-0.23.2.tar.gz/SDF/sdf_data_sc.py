"""
-------------------------------------------------------------------------
Project: SDF: Standard Data Format

Module: sdf_data_sc.py

Class sdf_data_sc: A class to respresent a single-column data-block in 
                   SDF-files.
 
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

import numpy
import sys
from .sdf_data import sdf_data
from . import sdf_rc
from . import sdf_utils


class sdf_data_sc(sdf_data):
    """
    A class for single-column datasets in the SDF project.
    """    
    # ---------------------------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------------------------
    def __init__(self, data=[], dtype='float', multiplier=None, offset=None):
        """
        Create an empty sdf_data_sc object.
        """

        # Init of base class
        super(sdf_data_sc, self).__init__('sc')

        # Set general stuff.
        self.ID = 'sdf-data-sc'
        # Set data and associates.
        self.Set(data, dtype, multiplier, offset)

    # ---------------------------------------------------------------------------
    # Setter Functions
    # ---------------------------------------------------------------------------
    def Set(self, data=[], dtype=None, multiplier=None, offset=None):
        """
        Set values of the sdf_data_sc class

        If dtype is not given, current dtype is kept. This will not be
        a problem for the initialization where this function is used 
        too, as there always is a default dtype.

        1) Mainly three different dtypes possible here:
           float, int, hex. Make sure that the datatype is always
           matching.
        """

        # Check if datatype is valid.
        if dtype is not None:
            if (dtype not in sdf_rc.KNOWN_VALUE_TYPES):
                print("Error of sdf_data_sc.Set, unknown data type:")
                print(dtype)
                sys.exit()
        else:
            dtype = self.dtype

        # Convert to numpy array, if necessary
        if not isinstance(data, numpy.ndarray):
            data = numpy.array(data)

        # Check what to do.
        if (dtype == "float") or (dtype == "int"):

            # Nothing dramatic happening. Just set.
            self.dtype      = dtype
            self.data       = numpy.array(data).astype(dtype)
            self.numvals    = len(self.data)
            self.multiplier = multiplier
            self.offset     = offset

        elif dtype == "hex":

            # Perform the conversion again, even if it is already
            # done to be sure.

            data_scaled = self._linear_transformation(data, multiplier, offset)
            data_scaled, mp, ofs, suc = sdf_utils.convert_to_int(data_scaled)

            if suc:
                # Everything worked fine. Set.
                self.dtype      = "hex"
                self.data       = numpy.array(data_scaled).astype(int)
                self.numvals    = len(self.data)
                self.multiplier = mp
                self.offset     = ofs

            else:
                # Conversion failed. Leave it as it was, fall back
                # float
                self.dtype      = "float"
                self.data       = numpy.array(data).astype(float)
                self.numvals    = len(self.data)
                self.multiplier = multiplier
                self.offset     = offset


    def Get(self):
        """
        Return a tuple with the contents, i.e. the data and its dtype
        """
        data = self._linear_transformation(self.data,
                                           self.multiplier,
                                           self.offset)

        return (data, self.dtype)


    def GetScaling(self):
        """
        Return the multiplier and the offset.
        """
        return self.multiplier, self.offset
    
    
    def SetDtype(self, dtype):
        """
        Set the dtype of the contained data. Check if it's a valid type
        referenced in the sdf_rc file. If it is, check and perform
        necessary conversions. If not, raise ValueError.

        In this kind of dataset, we would expect int, float or hex.

        :param dtype: string, new datatype
        :return: None
        """

        # Check if dtype is valid:
        if (dtype not in sdf_rc.KNOWN_VALUE_TYPES):
            print("Error in sdf_data_sc.SetDtype: Datatype not valid")
            print(dtype)
            sys.exit()

        # Check if datatype is the same, then do nothing
        if dtype == self.dtype:
            print("Warning in sdf_data_sc.SetDtype. Datatype requested"
                  " already set in class: %s" % dtype)
            return

        # Use self.Set to do the rest.
        self.Set(self.data, dtype, self.multiplier, self.offset)


    # ---------------------------------------------------------------------------
    # Getter Functions - Need to be overridden
    # ---------------------------------------------------------------------------        
    def __str__(self):
        """
        Printable representation of its contents. 
        """
        res = "DATA TYPE = %s, (%s)" % (self.datatype, self.dtype)
        res = res + " NUM-VALUES = %d\n" % self.numvals
        res = res + "MULTIPLIER = %s, OFFSET = %s\n" % (self.multiplier, self.offset)
        if self.numvals > 1:
            res = res + '     [%s ... %s]\n' % (str(self.data[0]), 
                                                str(self.data[-1]))
        elif self.numvals == 1:
            res = res + '     [%s]\n' % str(self.data[0])
        else:
            res = res + '     [-]\n'
        return res

    def AsXML(self, indent=0):
        
        ret = ' ' * indent + "<data cols='%d' rows='1' type='%s' " % \
              (self.numvals, self.dtype)

        if self.multiplier is not None:
            ret = ret + "multiplier='%s' " % self.multiplier
            
        if self.offset is not None:
            ret = ret + "offset='%s' " % self.offset

        ret = ret + ">\n"
            
        textblock = ''

        if self.dtype == "hex":
            data_to_write = sdf_utils.int_to_hex_list(self.data)
        else:
            data_to_write = self.data

        for d in data_to_write:
            textblock = textblock + ' ' + str(d)

        ret = ret + ' ' * (indent + sdf_rc._tabsize) + textblock + '\n'
        ret = ret + ' ' * indent + '</data>'        
        return ret


    def FromXML(self, etree_node):
        """
        Create an sdf_data_sc block from an XML ElementTree node.
        """
        if 'cols' in etree_node.attrib:
            cols = etree_node.attrib['cols']

        if 'rows' in etree_node.attrib:
            rows = etree_node.attrib['rows']

        if 'type' in etree_node.attrib:
            # this is one of the sdf_rc.KNOWN_VALUE_TYPES:
            # ('byte', 'int', 'float')
            self.dtype = etree_node.attrib['type']

        if 'multiplier' in etree_node.attrib:
            self.multiplier = float(etree_node.attrib['multiplier'])
        else:
            self.multiplier = None

        if 'offset' in etree_node.attrib:
            self.offset = float(etree_node.attrib['offset'])
        else:
            self.offset = None

        if int(rows) == 1:
            self.numvals = int(cols)
        else:
            self.numvals = int(rows)

        words = etree_node.text.split()

        if self.dtype == 'float':
            self.data = numpy.zeros(self.numvals, dtype='float')
            
            for counter in range(len(words)):
                self.data[counter] = float(words[counter])

        elif self.dtype == 'int':
            self.data = numpy.zeros(self.numvals, dtype='int')
            
            for counter in range(len(words)):
                self.data[counter] = int(words[counter])

        elif self.dtype == 'hex':
            self.data = numpy.zeros(self.numvals, dtype='int')

            for counter in range(len(words)):
                self.data[counter] = int(words[counter], base=16)

        else:
            print('Error: data type "%s" in "%s" files not (yet) supported.'\
                % (self.dtype, self.datatype))

    def GetType(self):
        """
        Return the type of the data-block
        """
        return self.dtype


    # ---------------------------------------------------------------------------
    # Helper functions dealing with conversions and stuff.
    # ---------------------------------------------------------------------------
    @staticmethod
    def _linear_transformation(data, multiplier, offset):
        """
        Given data, a multiplier and the offset, return the
        data transformed with those values by:

        data' = data * multiplier + offset

        Parameter:
        
            data (array-like):
               Array of numerical values, either int or float
            multiplier (float, int or None):
               Number to multiply the data with. None is taken
               as an implicit 1.0
            offset (float, int or None):
               Number of offset the values with. None is taken
               as an implicit 0.0

        Returns:
         
            scaled_data (array-like):
               Result scaled.
        """
        if multiplier is None:
            multiplier = 1
        if offset is None:
            offset = 0

        return data * multiplier + offset


    def _remove_linear_transformation(self):
        """
        If data in this class is given as float or int, this function
        removes any linear transformation by setting the multiplier to 1 (None)
        and the offset to 0 (None) and rescaling the data.
        """

        data, dtype = self.Get()
        if (dtype == "float") or (dtype == "int"):
            self.data = data
            self.multiplier = None
            self.offset = None
        else:
            print("Warning in sdf_data_sc._remove_linear_transformation:"
                  " Cannot remove transformation for non-int and non-float"
                  " data.")
            return 


    # ---------------------------------------------------------------------------
    # Other Stuff - TODO: IsValid 
    # ---------------------------------------------------------------------------

    def IsValid(self):
        """
        Check if the contents of this class are valid.
        """
        raise NotImplementedError

        

    def IsEmpty(self):
        """
        Check if this class instance is empty
        """
        pass        
