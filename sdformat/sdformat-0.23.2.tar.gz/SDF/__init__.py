"""
-------------------------------------------------------------------------

Project: SDF: Standard Data Format

Module: __init__.py

Make the contents of this directory importable as a module
 
bg 26.05.2010
fs 06.04.2013
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

from .sdf_rc import *
from .sdf_utils import *
from .sdf_base import *
from .sdf_gen_val import *
from .sdf_string import *
from .sdf_enc_string import *
from .sdf_name import *
from .sdf_owner import *
from .sdf_comment import *
from .sdf_date import *
from .sdf_par import *
from .sdf_sample import *
from .sdf_instrument import *
from .sdf_object import *

from .sdf_data import *
from .sdf_data_sc import *
from .sdf_data_mc import *
from .sdf_data_img import *

from . import convert
from . import file_io

from .sdf_wrapper import sdf_force

from .config_loader import CONFIG

__version__ = '0.23.2'
