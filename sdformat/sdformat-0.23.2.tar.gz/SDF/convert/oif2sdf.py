"""
Olympus OIF-File Converter
------------------------------------------------------------------------------
    Copyright (C) 2017-2019 Burkhard Geil, Ilyas Kuhlemann, Filip Savic

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

----------
Defines functions to convert Olympus OIF files to SDF files.

This file gets imported by `sdf-convert-oif2sdf` of the command
line interface of the SDF module. `sdf-convert-oif2sdf` is the
regular user's interface to this file's functionalities.

"""
import sys
import os
import shutil

from ._helper_functions import img_array_to_ascii
from .. import sdf_object, sdf_instrument, sdf_par, sdf_data_img
from SDF import CONFIG
if CONFIG.use_system_oiffile:
    import oiffile
else:
    from SDF.extern import oiffile


def oib2sdf(oibfilename, sdffilename=None, verbose=False, debug=False):
    folder, fname = os.path.split(oibfilename)
    if folder:
        tmp_folder = folder + "/.tmp_oif"
    else:
        tmp_folder = ".tmp_oif"
    tmp_ifname = tmp_folder + "/" + fname.rsplit('.')[0] + ".oif"

    if verbose or debug:
        print("creating temporary oif file and tiff images in '%s'") % tmp_folder

    os.mkdir(tmp_folder)
    oiffile.oib2oif(oibfilename, tmp_folder + "/")

    if verbose or debug:
        print("converting %s to sdf file" % tmp_ifname)
    oif, list_of_elementary_parameters, ws = oif2sdf(tmp_ifname, sdffilename, verbose, debug)
    shutil.rmtree(tmp_folder)
    if verbose or debug:
        print("removed temporary folder '%s'" % tmp_folder)
    return oif, list_of_elementary_parameters, ws


def oif2sdf(oiffilename, sdffilename=None, verbose=False, debug=False):
    oif = oiffile.OifFile(oiffilename)
    path = os.path.abspath(os.path.dirname(oiffilename)) + "/"
    ws = sdf_object("ws")
    if debug or verbose:
        print('Create workspace: ' + oiffilename.replace('.oif', ''))
    instrument = sdf_instrument(
        str(oif.mainfile['Acquisition Parameters Common']['Acquisition Device']))
    ws.AppendInstrument(instrument)
    ws.SetName(os.path.split(oiffilename)[1])
    date = str(oif.mainfile['Acquisition Parameters Common']['ImageCaputreDate'])
    ## --> parse date string to sdf accepted format?
    date = date.replace('-', '.')  # this should convert it to default format '%Y.%m.%d %H:%M:%S'
    ws.SetDate(date)
    ws.SetOwner(str(oif.mainfile['File Info']['UserName']))
    if verbose:
        print("Set owner to '%s'" % ws.owner.value)
    
    list_of_elementary_tuples = parse_parameters(oif.mainfile)
    solve_nested_lists(list_of_elementary_tuples)

    for param in list_of_elementary_tuples:
        new_sdf_par = sdf_par(*param)
        instrument.AppendPar(new_sdf_par)
    l_files = oif.tiffs.files[:]
    l_files.sort()

    current_channel = 0
    current_channel_ws = None

    if verbose:
        print("Found %i tiff images" % len(l_files))

    for f in l_files:
        if debug:
            print(f)
        fname = f.rsplit('.', 1)[0].rsplit('/', 1)[1]
        try:
            channel, ind = fname.split('C')[1].split('Z')
        except ValueError:
            channel, ind = fname.split('C')[1].split('T')
        channel = int(channel)  # channel number
        ind = int(ind)  # image index 
    
        if channel != current_channel:
            current_channel = channel
            current_channel_ws = sdf_object('ws')
            current_channel_ws.SetName("channel " + str(channel))
            ws.AppendObject(current_channel_ws)
        image_ds = sdf_object('ds')
        image_ds.SetName("image " + str(ind))
        current_channel_ws.AppendObject(image_ds)
        for param in parse_pty_to_param_tuples(path + f.rsplit('.', 1)[0] + ".pty"):
            new_par = sdf_par(*param)
            image_ds.AppendPar(new_par)
        img = oif.tiffs.imread(f)
        base64_encoded = img_array_to_ascii(img)
        ## @todo Here: dtype is fixed to uint16. Better: make it more flexible
        # using a dictionary assigning strings to numpy dtypes.
        sdf_img = sdf_data_img(base64_encoded, 'uint16', 'base64code', cdata=True)
        image_ds.SetData(sdf_img)

    # ---------------------------------
    # If requested, save the workspace
    # ---------------------------------
    if sdffilename:
        ws.Save(sdffilename)
        if debug or verbose:
            print('Wrote: ' + sdffilename)
    return oif, list_of_elementary_tuples, ws


def parse_pty_to_param_tuples(pty_fname):
    f = open(pty_fname, 'rb')
    content = f.read()
    lines = content.decode('utf-16').splitlines()
    ret_list = []
    #l = lines[0][2:].replace("\x00", "").strip().lstrip()
    l = lines[0][2:].replace("[", "").replace("]", "")
    current_param_tuple = (l, [])
    ret_list.append(current_param_tuple)
    for line in lines[1:]:        
        #s = line.replace("\x00", "").strip().lstrip()
        s = line.strip().lstrip()
        if s:
            if s[0] == "[" and s[-1] == "]":
                s = s.replace("[", "").replace("]", "")
                current_param_tuple = (s, [])
                ret_list.append(current_param_tuple)
            else:
                key, value = s.split("=")
                current_param_tuple[1].append((key, value.replace('"', '')))
    return ret_list


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
                # if MANUALLY_INSERTED_UNITS.keys().count(parameters[0]):
                # parameters=tuple(list(parameters)+[MANUALLY_INSERTED_UNITS[parameters[0]]])
                return parameters
            else:
                # in this case, the tuple is not considered elementary (and non-list), 
                # due to being too long or not containing the right type as value/unit
                if len(parameters) == 2:
                    elementary_list_tuple = (str(parameters[0]), parse_parameters(parameters[1]))
                    return elementary_list_tuple
                else:
                    msg = "ERROR: Can't parse possible parameters " + str(parameters)
                    msg += ":\n\t -> CASE NOT CONSIDERED YET!\n"
                    raise RuntimeError(msg)
        else:
            msg = "ERROR: Can't parse possible parameters " + str(parameters)
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
        msg = "ERROR: Can't parse possible parameters " + str(parameters)
        msg += ":\n\t -> Not of expected type list, dict (=tifffile.Record), or tuple.\n"
        msg += "type=" + str(type(parameters))
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
                    

if __name__ == "__main__":    
    oif, l_params, ws = oif2sdf(*sys.argv[1:])
