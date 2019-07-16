"""
-------------------------------------------------------------------------
Project: SDF: Standard Data Format

Module: sdf_base.py

Class sdf_gen_val: The base class of all SDF-objects that can contain a
                   value. 
 
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

from .sdf_base import sdf_base


class sdf_gen_val(sdf_base):

    def __init__(self, val=None):
        """ 
        Create an empty sdf_gen_val object. 
        """
        super(sdf_gen_val, self).__init__()
        self.ID = 'sdf-gen-val'
        self.value = val

    def Set(self, val):
        self.value = val

    def Get(self):
        return self.value
    
    def IsValid(self):
        return (self.value is not None)

    def IsEmpty(self):
        return ((self.value is None) or (self.value == (())) or 
                (self.value == []) or (self.value == {}) or self.value == '')




