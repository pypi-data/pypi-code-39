"""
Functions to convert data recorded with JPK instruments to SDF.
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

import sys
import os

from ._helper_functions import parse_parameters

import SDF
from SDF.sdf_wrapper.sdf_par_source import sdf_par_source

if SDF.CONFIG.use_system_jpkfile:
    import jpkfile
else:
    from SDF.extern import jpkfile

from .sdf2forcesdf import sdf2forcesdf
from .forcesdf2mat import forcesdf2mat
from ..sdf_utils import numpy_dtype_to_sdf_dtype


def jpk2sdf(jpkfilename, sdffilename='', create_force_sdf=False,
            create_mat=False, verbose=False, debug=False):
    if verbose:
        print("going to convert {} to {}".format(jpkfilename, sdffilename))
    extension = jpkfilename.split('.')[-1]
    par_source = sdf_par_source()
    par_source.FillDefaultSystemParameters()
    par_source.SetConverter("jpk2sdf")
    par_source.SetSourceFile(jpkfilename)
    if extension[-3:] == 'map':
        if debug or verbose:
            print("JPK archive is treated as map")
        par_source.SetSourceFileType('jpk-force-map')
        create_force_sdf = False
        jpk = jpkfile.JPKMap(jpkfilename)
        ws = _jpkmap2sdf(jpk, verbose, debug)
        ws.SetName("JPKMap " + jpkfilename.split('/')[-1])

        if debug or verbose:
            print("Converted map archive to SDF")

    else:
        if debug or verbose:
            msg = "JPK file is treated as regular jpk archive"
            msg += "(single atomic force or tweezer recording)"
            print(msg)
        if extension.count("nt-force"):
            par_source.SetSourceFileType("jpk-nt-force")
            create_force_sdf = False
        else:
            par_source.SetSourceFileType("jpk-force")
        jpk = jpkfile.JPKFile(jpkfilename)
        ws = _jpkfile2sdf(jpk, verbose, debug, label=jpkfilename.split('/')[-1])
        if debug or verbose:
            print("Converted force archive to SDF")

    ws.AppendPar(par_source)

    if not sdffilename:
        sdffilename = os.path.splitext(jpkfilename)[0] + '.sdf'

    if debug or verbose:
        print("saving SDF workspace to file")
    ws.Save(sdffilename)
    if debug or verbose:
        print('Wrote: ' + sdffilename)

    if create_force_sdf:
        force_sdffilename = os.path.splitext(sdffilename)[0] + '.force.sdf'
        sdf2forcesdf(sdffilename, force_sdffilename, use_hex=True)

        if create_mat:
            matfilename = os.path.splitext(sdffilename)[0] + '.mat'
            forcesdf2mat(force_sdffilename, matfilename)

    return ws, jpk


def _jpkmap2sdf(jpkmap, verbose=False, debug=False):

    ws_root = SDF.sdf_object('ws')
    instrument_original_parameters = SDF.sdf_instrument("original-parameters")
    ws_root.AppendInstrument(instrument_original_parameters)

    list_of_elementary_tuples = parse_parameters(jpkmap.parameters)
    
    for param in list_of_elementary_tuples:
        new_sdf_par = SDF.sdf_par(*param)
        instrument_original_parameters.AppendPar(new_sdf_par)

    ## How to include parameters from shared header?
    #  ---------------------------------------------
    # First version: add a parameter block at top level (ws_root).
    #    But I'm not sure about that, it's not easy readable.
    #    Maybe a hard copy of all shared parameters is nicer
    #    for readability of sdf files. Better yet, I include
    #    both versions. Otherwise, something might get lost
    #    when converting to sdf, e.g. when there is a link
    #    to the shared header of which I did not know it could
    #    exist.
    if jpkmap.has_shared_header:
        shared_parameters_elementary_tuples = parse_parameters(jpkmap.shared_parameters)    
        new_sdf_par = SDF.sdf_par("shared_parameters", shared_parameters_elementary_tuples)
        instrument_original_parameters.AppendPar(new_sdf_par)
    
    # Second version: (Has to be done in a for loop going
    #    through all pixels of the map) Look at local
    #    parameters and replace links to shared header
    #    with copy of shared header content.
    
    if verbose:
        sys.stdout.write("converting single force measurements (pixels of map) one by one ...")
    for i in range(len(jpkmap.flat_indices)):
        jpk = jpkmap.flat_indices[i]
        ws_single_jpk = _jpkfile2sdf(jpk, False, debug,
                                     "pixel " + str(i) + " in flattened map",
                                     jpkmap.has_shared_header)
        ws_root.AppendObject(ws_single_jpk)
    if verbose:
        sys.stdout.write(" [OK]\n")

    return ws_root


def _jpkfile2sdf(jpk, verbose=False, debug=False,
                 label='', shared_parameters_already_saved_in_parent_workspace=False):
    ws_root = SDF.sdf_object('ws')
    instrument_original_parameters = SDF.sdf_instrument("original-parameters")
    ws_root.AppendInstrument(instrument_original_parameters)

    if label:
        ws_root.SetName("JPKFile " + label)
    if verbose:
        print("Created workspace: %s\n" % ws_root.name.value)

    list_of_elementary_tuples = parse_parameters(jpk.parameters)

    for param in list_of_elementary_tuples:
        new_sdf_par = SDF.sdf_par(*param)
        instrument_original_parameters.AppendPar(new_sdf_par)

    ## How to include parameters from shared header?
    #  ---------------------------------------------
    # First version: add a parameter block at top level (ws_root).
    #    But I'm not sure about that, it's not easy readable.
    #    Maybe a hard copy of all shared parameters is nicer
    #    for readability of sdf files. Better yet, I include
    #    both versions. Otherwise, something might get lost
    #    when converting to sdf, e.g. when there is a link
    #    to the shared header of which I did not know it could
    #    exist.
    if jpk.has_shared_header and not shared_parameters_already_saved_in_parent_workspace:
        shared_parameters_elementary_tuples = parse_parameters(jpk.shared_parameters)
        new_sdf_par = SDF.sdf_par("shared_parameters", shared_parameters_elementary_tuples)
        instrument_original_parameters.AppendPar(new_sdf_par)
    # Second version: (Has to be done in a for loop going
    #    through all segments of the archive) Look at local
    #    parameters and replace links to shared header
    #    with copy of shared header content.

    for s in range(len(jpk.segments)):
        ws_single_segment = _jpksegment2sdf(jpk.segments[s], verbose,
                                            debug, label="segment " + str(s))
        ws_root.AppendObject(ws_single_segment)
    return ws_root


def _jpksegment2sdf(segment, verbose=False, debug=False, label=''):

    ws_segment = SDF.sdf_object('ws')
    instrument_original_parameters = SDF.sdf_instrument("original-parameters")
    ws_segment.AppendInstrument(instrument_original_parameters)
    
    if label:
        ws_segment.SetName(label)
    if verbose:
        if label:
            print("Created workspace for segment: %s\n" % ws_segment.name.value)
        else:
            print("Created workspace for segment")

    list_of_elementary_tuples = parse_parameters(segment.parameters)
    
    for param in list_of_elementary_tuples:
        new_sdf_par = SDF.sdf_par(*param)
        instrument_original_parameters.AppendPar(new_sdf_par)
    keys = list(segment.data.keys())
    keys.pop(keys.index('t'))

    for channel in keys:
        ds = SDF.sdf_object('ds')
        ds.SetName(channel)
        if debug:
            print("+" * 8)
            print(segment.data[channel][0].shape)
            print("+" * 8)
        data = segment.data[channel][0]
        dtype = numpy_dtype_to_sdf_dtype(data.dtype)
        data_block = SDF.sdf_data_sc(np.reshape(data,
                                                (data.shape[0],),), dtype)
        conv = SDF.sdf_par('converted', 'False')
        ds.AppendPar(conv)
        ds.SetData(data_block)

        ws_segment.AppendObject(ds)            
    return ws_segment


def replace_links_to_shared_parameters_with_hard_copy(local_parameters, shared_parameters):
    raise NotImplementedError()


if __name__ == "__main__":

    debug = False

    jpkfilename = sys.argv[1]

    sdffilename = ''
    if len(sys.argv) > 2:
        sdffilename = sys.argv[2]
    ws, jpk = jpk2sdf(jpkfilename, sdffilename, debug=debug)
