"""
-------------------------------------------------------------------------
Project: SDF: Standard Data Format

Module: sdf_base.py

Class sdf_base: The base class of ALL SDF-objects. This is the least
                common interface of all SDF-objects, containing an ID
                and the IsValid()-verification.
 
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


class sdf_base(object):

    def __init__(self):
        """ Create an empty sdf_base object. """
        self.ID = 'sdf-base'
    
    def IsValid(self):
        return False

    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        return self.__str__()