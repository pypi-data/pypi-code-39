"""
-------------------------------------------------------------------------
Project: SDF: Standard Data Format

Module: sdf_par.py

Class sdf_par: The class for  SDF parameter and parameter-list objects.
 
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
import logging
from . import sdf_rc
from .sdf_gen_val import sdf_gen_val
from .sdf_string import sdf_string


class sdf_par(sdf_gen_val):
    """
    A class for parameters and parameter-lists in the SDF project.
    """    
    def __init__(self, name='noname', val=None, unit=None, parent_par=None): 
        """ 
        Create an sdf_par object. 
        """
        if val is None:  # start an empty list of parameters
            unit = None
            val = []
        elif type(val) == list:
            val = self.ParseParameterList(val)
        elif type(val) == str:
            val = val.replace('"', "'")
        super(sdf_par, self).__init__(val)
        self.ID = 'sdf-par'
        self.name = sdf_string(name)
        self.unit = unit      # sdf_string(unit)
        self.parent_par = parent_par
        
    def __str__(self):
        """
        Return a printable representation of the parameter.
        """
        if isinstance(self.value, list):
            return_string = str(self.name) + ":\n"
            for value in self.value:
                return_string += "  " + str(value) + "\n"
            return return_string
        if self.unit:
            return '%s = %s [%s]' % (str(self.name), 
                                     str(self.value), 
                                     str(self.unit))        
        return '%s = %s' % (str(self.name), str(self.value)) 
            
    def ParseParameterList(self, param_list):
        """
        In case this object is initiated with a list of values,
        these values need to be converted to individual sdf_par objects;
        that's what this function is used for.
        @param param_list List of elementary parameter tuples.
        """
        val = []
        for param in param_list:
            if isinstance(param, sdf_par):
                val.append(param)
                param.parent_par = self
                continue
            if type(param[1]) == str:
                param = list(param)
                param[1] = param[1].replace('"', "'")
            parent_par_packed_in_dict = {"parent_par": self} 
            val.append(sdf_par(*param, **parent_par_packed_in_dict))
        return val

    def Set(self, name='noname', val=None, unit=None, parent_par=None):
        """
        Set the values of an sdf_par. 
        """
        if val is None:  # start an empty list of parameters
            unit = None
            val = []
        elif type(val) == list:
            val = self.ParseParameterList(val)
        elif type(val) == str:
            val = val.replace('"', "'")
        self.value = val
        self.name = sdf_string(name)
        self.unit = unit
        self.parent_par = parent_par

    def AppendPar(self, sdf_par_instance):
        if not self.IsParmeterSet():
            msg = "Attempt to use sdf_par.AppendPar for single-value sdf_par, "
            msg += "but this method is only available if your sdf_par "
            msg += "is a parameter set (i.e. it's value is a list)."
            raise RuntimeError(msg)
        if not isinstance(sdf_par_instance, sdf_par):
            raise TypeError("Can only append instances of sdf_par.")        
        self.value.append(sdf_par_instance)
        sdf_par_instance.parent_par = self

    def Get(self):
        """
        Return a tuple with the values as strings or Nones.
        """
        n = str(self.name)
        if self.unit is None:
            u = None
        else:
            u = str(self.unit)
        if isinstance(self.value, list):
            v = None
        else:
            v = str(self.value)
        return ((n, u, v))

    def GetChild(self, name=None):
        """
        Returns a list of children when name == None, or the child with
        name == 'name', or None. 
        """
        if not name:
            if isinstance(self.value, list):
                return self.value
        else:
            for e in self.value:
                if str(e.name) == name:
                    return e
        return None

    def AsXML(self, indent=0, lw=1000000):
        """
        Return the XML code of the parameter.
        """
        need_end_tag = True
        ret = ''
        word = ' ' * indent + '<par name="' + self.name.AsXML() + '" '
        if not isinstance(self.value, list):
            word = word + ' value="' + str(self.value) + '" '
            if self.unit is not None:
                word = word + ' unit="' + str(self.unit) + '" '
            word = word + '/>'
            need_end_tag = False
        else:
            word = word + '>'
        ret = ret + word

        if isinstance(self.value, list):  # assume it's a list of parameters
            for e in self.value:
                ret = ret + '\n' + e.AsXML(indent=indent + sdf_rc._tabsize)
        if need_end_tag:
            ret = ret + '\n' + ' ' * indent + '</par>'
        return ret

    def FromXML(self, etree_node):
        """
        Create an sdf_par instance from an XML ElementTree node.
        @todo does not support multi-line syntax as self.AsXML() .
        @TODO: we might want to convert certain values for value
               into appropriate types, like 'None' to python None
               and things that can be floats to floats.
        """
        if 'name' in etree_node.attrib:
            self.name = sdf_string(etree_node.attrib['name'])
        if 'value' in etree_node.attrib:
            self.value = etree_node.attrib['value']
        else:
            for child in etree_node:
                par = sdf_par()
                par.FromXML(child)
                par.parent_par = self
                self.value.append(par)
                
        if 'unit' in etree_node.attrib:
            self.unit = etree_node.attrib['unit']

    def IsValid(self):
        """
        Check validity of an sdf_par object.
        """
        msg = "sdf_par.IsValid(): Not yet implemented"
        msg += "\n--> is always considered valid"
        logging.warning(msg)
        return True

    def IsParmeterSet(self):
        return isinstance(self.value, list)

    def __getitem__(self, key):
        if not self.IsParmeterSet():
            msg = "This sdf_par (\"{}\") is not a parameter set.\n".format(self.name.value)
            msg += "Get a value of a single parameter by accessing sdf_par.value."
            raise RuntimeError(msg)
        if isinstance(key, int):
            return self.value[key]
        if isinstance(key, str):
            return self._get_child_sdf_par_by_name(key)
        raise TypeError("key needs to be of type str or int.")

    def _get_child_sdf_par_by_name(self, name):
        for child_par in self.value:
            if child_par.name.value == name:
                return child_par
        raise KeyError("sdf_par by name \"{}\" not found!".format(name))
