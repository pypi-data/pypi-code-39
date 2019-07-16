"""
Collection of utility funcions to help convert data files to SDF.
------------------------------------------------------------------------------
    Copyright (C) 2016-2019 Burkhard Geil, Ilyas Kuhlemann, Filip Savic

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
from PIL import Image
import base64
import os

from SDF import CONFIG
if CONFIG.use_system_oiffile:
    import oiffile
else:
    from SDF.extern import oiffile


def parse_parameters(parameters):
    """
    Function to parse a general structure containing parameters (like tuple, 
    list, dictionary, or a mixture of all) into elementary tuples of the 
    form:
        * (name, value)
       or
        * (name, value, unit)
       or
        * (name, list_of_elementary_tuples)
    Note, that the last elementary tuple can be used recursively, to hold 
    more elementary tuples, even more layers of recursive ones.
    @param parameters General structure containing parameters.
    @return List of elementary parameter tuples.

    @note This does not parse all parameters of cz_lsm_scan_info to elementary 
    tuples of the form defined above. Instead, some have the form
       * (name, [list_of_elementary_tuples_0,list_of_elementary_tuples_1,...]),
    i.e., the second item is a nested list. 
    For now, I will write another helper function, that transforms this 
    nested list into the desired `list_of_elementary_tuples`. 
    See function `solve_nested_lists`.
    """
    list_of_elementary_parameters = []
    if type(parameters) == tuple:
        if type(parameters[0]) == str or type(parameters[0]) == unicode:
            if is_elementary_non_list(parameters):                
                return parameters
            else:
                # in this case, the tuple is not considered elementary (and non-list), 
                # due to being too long or not containing the right type as value/unit
                if len(parameters) == 2:
                    elementary_list_tuple = (str(parameters[0]), parse_parameters(parameters[1]))
                    return elementary_list_tuple
                else:
                    msg = "ERROR in SDF.convert._helper_functions.parse_parameters:\n"
                    msg += "Can't parse possible parameters " + str(parameters)
                    msg += ":\n\t -> CASE NOT CONSIDERED YET!\n"
                    raise RuntimeError(msg)
        else:
            msg = "ERROR in SDF.convert._helper_functions.parse_parameters:\n " 
            msg += " Can't parse possible parameters " + str(parameters)
            msg += ":\n\t -> does not contain a string (keyword/name) as first entry.\n"
            raise RuntimeError(msg)            
    elif type(parameters) == list:        
        for item in parameters:
            list_of_elementary_parameters.append(parse_parameters(item))
        return list_of_elementary_parameters
    elif type(parameters) == dict or type(parameters) == oiffile.SettingsFile:
        tuple_list = sorted(parameters.items())
        for item in tuple_list:
            list_of_elementary_parameters.append(parse_parameters(item))
        return list_of_elementary_parameters
    else:
        msg = "ERROR in SDF.convert._helper_functions.parse_parameters:\n "
        msg += "Can't parse possible parameters " + str(parameters) + ":\n"
        msg += "\t -> Not of expected type list, dict (=tifffile.Record), or tuple.\n"
        raise RuntimeError(msg)

    
def is_elementary_non_list(parameter_tuple):
    """
    Checks a parameter_tuple candidate, whether it's elementary and not a list or not.
    @param parameter_tuple Tuple that is possibly elementary.
    @return 1 if considered elementary, 0 if considered not completely parsed, 
    -1 if considered non-parsable.
    """
    ## Might be better to test this case before calling this function?
    # Because this is the only criteria to discard the tuple and return -1.
    if not (type(parameter_tuple[0]) == str or type(parameter_tuple[0]) == unicode):        
        return -1
    if len(parameter_tuple) == 2:
        if type(parameter_tuple[1]) == dict:
            return 0
        if type(parameter_tuple[1]) == list:
            return 0
        if type(parameter_tuple[1]) == tuple:
            return 0
        return 1
    elif len(parameter_tuple) == 3:
        if type(parameter_tuple[1]) == dict:
            return 0
        if type(parameter_tuple[1]) == list:
            return 0
        if type(parameter_tuple) == tuple:
            return 0
        if type(parameter_tuple[2]) != str:
            return 0
        return 1
    else:        
        return 0


def solve_nested_lists(parameter_list):
    """
    Function to help solving the issue with nested lists after recursive
    processing with function `parse_parameters`.
    @note Not a stable solution, due to not being recursive. What happens
    if nested lists are in a deeper level, let's say in 
    `parameter_list[0][1][0][1]`??
    """
    ## search for nested lists:
    for i in range(len(parameter_list)):
        param = parameter_list[i]
        if type(param[1]) == list:
            for j in range(len(param[1])):                
                if type(param[1][j]) == list:                    
                    solve_nested_lists(param[1][j])
                    t = (param[0] + "_subparam_" + str(j), param[1][j])                    
                    parameter_list[i][1][j] = t

                    
def img_array_to_ascii(array):
    """
    Converts an array containing an image to a string of ASCII characters.
    @param array Numpy array containing image data.
    @return String containing image data encoded as ASCII characters.
    """
    # 1. Create temporary PNG file.
    if array.dtype == np.uint8:
        im = Image.fromarray(array, 'L')
    elif array.dtype == np.uint16:
        im = Image.new('I', array.T.shape)        
        im.frombytes(array.tobytes(), 'raw', 'I;16')
    else:
        raise ValueError("Supports only conversion of UINT8 or UINT16 images!")
    im.save('.tmp_img.png')        
    # 2. Transform PNG file to temporary text file.
    base64.encode(open('.tmp_img.png', 'rb'), open('.tmp_img.txt', 'wb'))
    # 3. Read text from file.
    f = open('.tmp_img.txt', 'rt')
    txt = f.read()
    # 3.1 Replace CDATA escape sequence in string
    # WAS ONLY NECESSARY FOR uu.encode, NOT FOR base64.encode
    # txt=txt.replace(']]>',SDF.sdf_rc._CDATA_REPLACE)
    # 4. Remove temporary files.
    os.remove('.tmp_img.txt')
    #os.remove('.tmp_img.png')
    return txt
