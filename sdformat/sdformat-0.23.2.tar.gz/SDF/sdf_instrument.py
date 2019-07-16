"""
-------------------------------------------------------------------------
Project: SDF: Standard Data Format

Module: sdf_instrument.py

Class sdf_instrument: The class for the SDF instrument settings.
 
bg 15.09.2015 : Completely remodeled class hierarchy

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

from .sdf_base import *
from .sdf_name import *
from .sdf_par  import *

class sdf_instrument(sdf_base):

    def __init__(self,name='noname'):
        """ 
        Create an sdf_instrument object. 
        """

        super(sdf_instrument,self).__init__()
        self.ID = 'sdf-instrument'
        self.name = sdf_name(name)  # the sdf_name of the instrument
        self.par = []    # initially an empty list of sdf_pars

    def AppendPar(self, par):
        """
        Append a parameter or a list of parameters to the list
        of the instruments parameters.
        """
        # NOTE: If you change something here, it propably also has to
        #       be changed in the sdf_object.AppendPar() function.  

        if isinstance(par, sdf_par):
            self.par.append(par)
        elif type(par) == type([]):
            self.par = self.par + par # this is Pythons list concatenation
        elif type(par) == type('a'):
            self.par.append(sdf_par(name=par)) # create a new, empty 
                                               # subparameter list 

    def Set(self,name='noname'):
        self.name = sdf_name(name)
        self.par  = []

    def Get(self):
        return ((self.name, self.par))

    def __str__(self):
        """
        Printable representation of its contents. 
        """
        res = 'INSTRUMENT ' + str(self.name) 
        for par in self.par:
            res = res + '       PARAMETER ' + str(par) + '\n'
        return res

    def AsXML(self, indent=0, lw=1000000):
        
        if self.IsEmpty():
            return
        
        ret  = ''
        word = ' '*indent + '<instrument>'
            
        ret = ret + word + '\n'
        
        if not self.name.IsEmpty():
            ret = ret + (self.name.AsXML(indent=indent + sdf_rc._tabsize))
                                         
        ret = ret + '\n'
                                         
        first = True
        for par in self.par:
            if not first:
                ret = ret + '\n'
            ret = ret + (par.AsXML(indent=indent + sdf_rc._tabsize))
            first = False      
        
        ret = ret + '\n' + ' '*indent + '</instrument>'
        
        return ret

    def FromXML(self,etree_node):
        """
        Create an SDF_instrument block from an XML ElementTree node.
        """
        for child in etree_node:
            if child.tag == 'name':
                self.name.FromXML(child)
            if child.tag == 'par':
                self.par.append(sdf_par())
                self.par[-1].FromXML(child)



    def IsValid(self):
        return self.name != 'noname'

    def IsEmpty(self):
        return len(self.par) == 0

    def GetPar(self, key):
        """
        More comfortable way to get a parameter in sdf_object.par either by
        index or name.
        """
        if isinstance(key, int):
            return self.par[key]
        if isinstance(key, str):
            for p in self.par:
                if p.name.value == key:
                    return p
            msg = "No parmeter by name \"{}\" found.".format(key)
            raise KeyError(msg)
        msg = "key needs to be of type int or str"
        raise TypeError(msg)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.par[key]
        if isinstance(key, str):
            return self._get_child_sdf_par_by_name(key)
        raise TypeError("key needs to be of type str or int")

    def _get_child_sdf_par_by_name(self, name):
        for child_par in self.par:
            if child_par.name.value == name:
                return child_par
        raise KeyError("sdf_par by name \"{}\" not found".format(name))
