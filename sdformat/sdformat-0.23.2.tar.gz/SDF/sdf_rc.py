"""
-------------------------------------------------------------------------
Project: SDF: Standard Data Format

Module: sdf_rc.py

Contains all global settings and resources of the SDF Project.
 
bg 11.09.2015 : Completely remodeled class hierarchy
ik 08.06.2016 : Added replacement string for CDATA end sequence 
                in uu encoded strings.
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
# During development, files in the '/home/bg/mfs/prj/fileformats/SDF'
# directory can be executed when the next two lines are un-commented.
#
# Otherwise, when the standard installation of SDF should be used,
# import SDF from the unchanged PYTHONPATH of your environment and
# comment out the next two lines.
import logging 
import SDF

msg = '-' * 80 + "\n"
msg += 'IN sdf_rc:\n'
msg += 'SDF from: %s\n' % SDF.__path__
msg += 'SDF ->   %s\n' % str(dir(SDF))
msg += '-' * 80
logging.info(msg)


#======================================================================

_tabsize = 3   # used for pretty-printing XML files

DEFAULT_DATE_FORMAT = '%Y.%m.%d %H:%M:%S'

XML_encoding = (('&', '&amp;'),   # Attention:
                ('>', '&gt;'),    # The order of this list plays an
                ('<', '&lt;'),    # important role.
                ('"', '&quot;'),  # Thus, it cannot be a dictionary!
                ("'", '&apos;'))

KNOWN_ENCODINGS = ('utf-8',)

#----------------------------------------------------------------------
# The following dictionary translates SDF data-types into Python data
# block classes. 
# key:   (string) SDF name of the datatype
# value: (class name) of the Python data block class (derived from
#                     sdf_data) 
#----------------------------------------------------------------------
"""
KNOWN_DATA_TYPES = {'sc' : SDF.sdf_data_sc,  # a single-column dataset
                    'img': None              # a binary (uuencoded) 
                                             # image file
                   }
"""

#---------------------------------------------------------------------
# A list of known data-value types
#
# byte   :  A7 09 FF 10 2B
# int    :  12 37542 119 2
# float  :  1.09 2.21 2.97
# uucode :  s.34dhf-_w3!s*
# hex    :  23ABEFF21F AC 1E 1FF
#---------------------------------------------------------------------

KNOWN_VALUE_TYPES = ('byte','int','float','uucode','base64code','hex')


#---------------------------------------------------------------------
# A string to replace the CDATA escape sequence ']]>'
# in uu encoded images. 
#---------------------------------------------------------------------
 
_CDATA_REPLACE="gurkensalat"

#---------------------------------------------------------------------
# Dictionary assigning numpy dtype character to exponent to base 2.
#---------------------------------------------------------------------

_GET_NUMPY_EXPONENT={"B":8, ## uint 8
                     "H":16,## uint 16
                 }
