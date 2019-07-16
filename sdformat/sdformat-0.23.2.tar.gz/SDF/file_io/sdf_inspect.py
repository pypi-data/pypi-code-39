"""
Collection of functions we used for debugging file converters.
------------------------------------------------------------------------------
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
import sys
from ..file_io.sdf_load import *

_tabsize=3
_len_output=76

def create_obj_summary(obj):
    res = _create_separation_line()
    res = res + _create_header_line('PROPERTIES')
    if obj.IsWorkspace():
        res = res + 'WORKSPACE '
        res = res + str(obj.name)
    elif obj.IsDataset():
        res = res +'DATASET '
        res = res + str(obj.name)
        res = res + '  '*_tabsize + 'TYPE = ' + str(obj.value.datatype) + '\n'
    
    else:
        return 'Error: Object is neither DATASET nor WORKSPACE'
        
    if not obj.owner.IsEmpty():
        res = res + str(obj.owner)
    if not obj.date.IsEmpty():
        res = res + str(obj.date)
    if not obj.comment.IsEmpty():
        res = res + str(obj.comment)
    '''
    for sample in obj.sample:
        res = res + str(sample)
    for instrument in obj.instrument:
        res = res + str(instrument)
    '''
    for par in obj.par:
        res = res + 'PARAMETER ' + str(par) + '\n'
    
    res = res + _create_separation_line()
    
    if obj.IsWorkspace():
        res = res + _create_header_line('CONTENT')
        res = res + 'NUMBER OF OBJECTS: ' + str(len(obj.value)) + '\n'
        for i in range(len(obj.value)):
            child=obj.value[i]
            res = res + 'OBJECT '+str(i) + '\n'
            res = res + create_content_summary(child,_tabsize)
            res = res + _create_separation_line()

    res = res + _create_separation_line()
    return res


def create_content_summary(obj,indent=0):

    if obj.IsWorkspace():
        res = ' '*indent + 'WORKSPACE ' + str(obj.name)
        for child in obj.value:
            res = res + create_content_summary(child,indent+_tabsize)
        res = res + ' '*indent + '='*(_len_output-indent) + '\n'

    elif obj.IsDataset():
        res = ' '*indent + 'DATASET ' + str(obj.name) + ' '*_tabsize +'TYPE ' + str(obj.value.datatype) + '\n'
        res = res + ' '*indent + '='*(_len_output-indent) + '\n'
    else:
        return 'Error: Object is neither DATASET nor WORKSPACE'
    
    return res
    



# ====================================================
# ================= helper functions =================
# ====================================================

def _create_output_line_from_str(s,min_length,fill_left,fill_right,start_index,space_left,space_right):
    res = fill_left*start_index
    res = res + ' '*space_left + s + ' '*space_right
    res = res + fill_right * (min_length - len(res)) + '\n'
    return res
    
def _create_header_line(s,tabs=1):
    return _create_output_line_from_str(s,_len_output,'=','=',_tabsize*tabs,1,1)

def _create_separation_line():
    return _create_output_line_from_str('',_len_output,'=','=',0,0,0)



if __name__=="__main__":

    if len(sys.argv)>1:
        fname = sys.argv[-1]
        obj=sdf_load(fname)

    else:
        sys.stderr.write("ERROR: you need at least a sdf file as parameter!\n")
        sys.exit(1)

    print(create_obj_summary(obj))

