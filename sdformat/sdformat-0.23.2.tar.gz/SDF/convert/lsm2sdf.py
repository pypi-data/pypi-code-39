"""
Zeiss LSM-File Converter
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

----------
Holds functions to convert Zeiss LSM files to SDF files.

This file gets imported by `sdf-convert-lsm2sdf` of the command
line interface of the SDF module. `sdf-convert-lsm2sdf` is the
normal user's interface to this file's functionalities.

Structure of output sdf file:
-----------------------------
<workspace>
   ...                # parameters  
   <workspace>        # one workspace per series
      <name>
         series_0
      </name>
      ...
      <workspace>     # one workspace per layer
         <name>
            layer_0
         </name>
         ...
         <dataset>    # one dataset per page/image       
            ...
         </dataset>
      </workspace>
   </workspace>
   ...
</workspace>
---------------------------------------------------


Notes
-----
This is the attempt to read all information from any lsm file.
It was created looking only at one example lsm file so far,
so we might have failed to really capture ALL parts of the
lsm file you want to convert. 
Furthermore, I could not figure out an awesome way to structure
comments on how the lsm file is analysed. ... @todo continue
"""

import numpy
import SDF

import scipy.misc as spmisc
import base64

import sys
import os

if SDF.CONFIG.use_system_tifffile:
    import tifffile
else:
    from SDF.extern import tifffile

from ._helper_functions import img_array_to_ascii

## The parameters read from the lsm file lack units.
# The following dictionary assigns a few units to 
# parameters manually. We are not 100% sure they
# are always right, but those were the fixed units
# shown by Zeiss' ZEN software for our examples
# lsm files.
MANUALLY_INSERTED_UNITS = {"plane_spacing": "um",
                           "line_spacing": "um",
                           "sample_spacing": "um",
                           "pinhole_diameter": "um"}  # um == micrometer ... greek mu making trouble


def lsm2sdf(lsmfilename, sdffilename=None, verbose=False, debug=False):
    """
    Read LSM file 'lsmfilename' into an SDF workspace.
    """
    # ------------------------------------------------------
    # load the LSM file into tifffile.TiffFile-Object 'lsm'
    # ------------------------------------------------------
    if debug or verbose:
        print('=' * 80)
        print('lsm2sdf: Reading', lsmfilename)

    lsm = tifffile.TiffFile(lsmfilename)

    if not lsm.is_lsm:
        if debug or verbose:
            print('... [ERROR]')
        return
    else:
        if debug or verbose:
            print('...[OK]')
    if debug or verbose:
        print('Found %d pages (images).' % len(lsm.pages))
    # ---------------------------------------------------------
    # Create workspace ws with name obtained from lsm.filename
    # ---------------------------------------------------------
    ws = SDF.sdf_object('ws')
    if debug or verbose:
        print('Create workspace: ' + lsm.filename.replace('.lsm', ''))
    instrument = SDF.sdf_instrument('Carl Zeiss LSM')
    ws.AppendInstrument(instrument)
    ws.SetName(os.path.split(lsmfilename)[1])
    # ------------------------------------------------------
    # From the first page extract the global parameters:
    # ------------------------------------------------------  
    #    cz_lsm_channel_colors : This is a Nx2 numpy-array.
    #                            I don't know of what.
    #                            Currently IGNORED
    #    cz_lsm_event_list : This is empty in my example
    #                        lsm-file.
    #                        Currently IGNORED
    #    cz_lsm_info : A strange list of numbers and lists.
    #                  Currently IGNORED
    #    cz_lsm_scan_info : Obviously a dictionary with
    #                       instrument parameters 
    #    cz_lsm_time_stamps : A numpy-array with timestamps
    #                         (1/2 as much as pages)
    # ------------------------------------------------------

    p0 = lsm.pages[0]

    # -----------------
    # cz_lsm_scan_info
    # -----------------    
    list_of_elementary_parameter_tuples = parse_parameters(p0.cz_lsm_scan_info)
    solve_nested_lists(list_of_elementary_parameter_tuples)

    for param in list_of_elementary_parameter_tuples:
        new_sdf_par = SDF.sdf_par(*param)
        instrument.AppendPar(new_sdf_par)
    # -------------------
    # cz_lsm_time_stamps
    # -------------------    
    ds_time_stamps = SDF.sdf_object('ds')
    ds_time_stamps.SetName('time-stamps')
    data_block_time_stamps = SDF.sdf_data_sc(p0.cz_lsm_time_stamps, 'float')
    ds_time_stamps.SetData(data_block_time_stamps)
    ws.AppendObject(ds_time_stamps)
    p1_props = [e for e in dir(lsm.pages[1]) if not e.startswith("_")]
    # Comparing both lists shows, cz_lsm_* properties are only present for p0,
    # but not for other pages.
    # All properties in p1_props, seem to be present for every page. Hence, I
    # will include them as parameters for the image datasets or their parent
    # workspace.

    ## There is some problem with these properties ...
    p1_props.pop(p1_props.index('imagej_tags')) 
    p1_props.pop(p1_props.index('uic_tags'))
    ## This is a dictionary of tags that needs some special
    # treatment I guess
    p1_props.pop(p1_props.index('tags'))
    ## This is the image content --> covered in img data blocks
    p1_props.pop(p1_props.index('asarray'))
    ## I don't get why, but this flag is True only for the
    # first page of the first series. --> I think this 
    # property is not helpful at all.
    p1_props.pop(p1_props.index('is_lsm'))
    
    # --------------------------
    # Create ws for each series
    # --------------------------
    for i in range(len(lsm.series)):
        ws_series = SDF.sdf_object('ws')
        ws_series.SetName('series_' + str(i))
        ws.AppendObject(ws_series)        
        s = lsm.series[i]        
        # --------------------------
        # Check whether parameters
        # of all images are 
        # identical.
        # --------------------------
        prop_values = [getattr(s[0], prop) for prop in p1_props]
        identical_props = [p for p in p1_props]
        not_identical_props = []
        for p in range(len(p1_props)):            
            for j in range(len(s)):
                if getattr(s[j], p1_props[p]) != prop_values[p]:
                    not_identical_props.append(identical_props.pop(p - len(not_identical_props)))
                    break                
        ## For those properties containing identical 
        # values for each page of this series,
        # create a parameter at workspace level
        # (not one for each page).
        for id_prop in identical_props:
            new_sdf_par = SDF.sdf_par(id_prop, getattr(p0, id_prop))
            ws_series.AppendPar(new_sdf_par)

        # --------------------------
        # Create ws for each layer
        # --------------------------
        for l in range(s[0].asarray().shape[0]):
            ws_layer = SDF.sdf_object('ws')
            ws_layer.SetName('layer_' + str(l))
            ws_series.AppendObject(ws_layer)
            # ------------------------------
            # Create ds for each image/page
            # ------------------------------
            for j in range(len(s)):
                ds_page = SDF.sdf_object('ds')
                ds_page.SetName('img_' + str(j))
                img_as_ascii = img_array_to_ascii(s[j].asarray()[l, :, :])
                sdf_img = SDF.sdf_data_img(img_as_ascii, 'uint8', 'base64code', cdata=True)
                ds_page.SetData(sdf_img)        
                ## For those properties containing different 
                # values for each page of this series,
                # create a parameter for each dataset/page.
                for non_id_prop in not_identical_props:
                    new_sdf_par = SDF.sdf_par(non_id_prop, getattr(s[j], non_id_prop))
                    ds_page.AppendPar(new_sdf_par)

                ws_layer.AppendObject(ds_page)                
    # =====================================
    # Up to this part, I think all relevant
    # parameters and data were read from 
    # the lsm file.
    # For completeness sake, the following 
    # part adds additional parameters to 
    # the sdf_object, but they appear to 
    # be less relevant
    # =====================================
    lsm_obj_props = [e for e in dir(lsm) if not e.startswith("_")]
    lsm_obj_props.pop(lsm_obj_props.index('byteorder'))  # This messes up xml syntax, since 
                                   # its content is "<". Also, I think
                                   # this is just for lsm file reading,
                                   # but tifffile has handled all of 
                                   # that for us at this point already.    
    for e in lsm_obj_props:
        v = getattr(lsm, e)
        if type(v) == str or type(v) == bool or type(v) == float or type(v) == int:
            new_sdf_par = SDF.sdf_par(e, v)
            ws.AppendPar(new_sdf_par)
        elif v is None:
            new_sdf_par = SDF.sdf_par(e, 'None')
            ws.AppendPar(new_sdf_par)
            
    ## Properties unique to p0 (not present in other pages),
    # and not processed aboce yet: 'cz_lsm_info', 'cz_lsm_channel_colors', 'cz_lsm_event_list'
    ## Event list is empty in example, so I am not sure how to handle that.
    # For now, I will just process the other two.

    ## cz_lsm_info to parameters
    cz_lsm_info = p0.cz_lsm_info
    cz_lsm_info_par_list = []
    for i in range(len(cz_lsm_info)):
        v = cz_lsm_info[i]
        if type(v) == numpy.ndarray:
            if v.any():
                msg = "WARNING, NOT WELL IMPLEMENTED YET! "
                msg += "ARRAY IN cz_lsm_info IS NOT EMPTY!\nWill save array as string for now.\n"            
                sys.stderr.write(msg)
                cz_lsm_info_par_list.append((str(i), "numpy.ndarray: " + str(v).replace("\n", " ")))                        
            else:
                cz_lsm_info_par_list.append((str(i), "EMPTY ARRAY OF SHAPE " + str(v.shape)))
        else:
            cz_lsm_info_par_list.append((str(i), v))
    new_sdf_par = SDF.sdf_par('cz_lsm_info', cz_lsm_info_par_list)
    ws.AppendPar(new_sdf_par)
    ## cz_lsm_channel_colors to multi-column dataset
    ds_channel_colors = SDF.sdf_object('ds')
    ds_channel_colors.SetName('channel colors') 
    data_block_channel_colors = SDF.sdf_data_mc(p0.cz_lsm_channel_colors, 'float')
    ds_channel_colors.SetData(data_block_channel_colors)
    comment = "Extracted from first page's (first image as read by tifffile module) "
    comment += "property `cz_lsm_channel_colors`.\nWe are not sure "
    comment += "what this array of channel colors represents, but included it for completeness."
    ds_channel_colors.SetComment(comment)
    ws.AppendObject(ds_channel_colors)    
    # ---------------------------------
    # If requested, save the workspace
    # ---------------------------------
    if sdffilename:
        ws.Save(sdffilename)
        if debug or verbose:
            print('Wrote: ' + sdffilename)
    return ws, lsm, list_of_elementary_parameter_tuples

############################################################################
### helper functions #######################################################
############################################################################


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
    @param parameter General structure containing parameters.
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
        if type(parameters[0]) == str:
            if is_elementary_non_list(parameters):
                if parameters[0] in MANUALLY_INSERTED_UNITS.keys():
                    parameters = tuple(list(parameters) + [MANUALLY_INSERTED_UNITS[parameters[0]]])
                return parameters
            else:
                # in this case, the tuple is not considered elementary (and non-list), 
                # due to being too long or not containing the right type as value/unit
                if len(parameters) == 2:
                    elementary_list_tuple = (parameters[0], parse_parameters(parameters[1]))
                    return elementary_list_tuple
                else:
                    msg = "ERROR: Can't parse possible parameters "
                    msg += str(parameters) + ":\n\t -> CASE NOT CONSIDERED YET!\n"
                    raise RuntimeError(msg)
        else:
            msg = "ERROR: Can't parse possible parameters " + str(parameters)
            msg += ":\n\t -> does not contain a string (keyword/name) as first entry.\n"
            raise RuntimeError(msg)
        
    elif type(parameters) == list:        
        for item in parameters:
            list_of_elementary_parameters.append(parse_parameters(item))
        return list_of_elementary_parameters

    elif type(parameters) == dict or type(parameters) == tifffile.Record:        
        tuple_list = parameters.items()
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
    if not type(parameter_tuple[0]) == str:        
        return -1
    if len(parameter_tuple) == 2:  # or len(parameter_tuple)==3:
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

if __name__ == '__main__':    
    ws, lsm, list_of_elementary_parameters = lsm2sdf(*sys.argv[1:])
