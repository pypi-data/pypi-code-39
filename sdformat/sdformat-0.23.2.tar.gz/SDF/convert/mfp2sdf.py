"""
Functions to convert data recorded with a MFP device to SDF.
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

from typing import Tuple, List
import os
import logging
from ._helper_functions import parse_parameters, img_array_to_ascii
from .. import __version__
from .. import sdf_object, sdf_par, sdf_data_sc, sdf_data_mc
from .. import CONFIG
from ..sdf_wrapper.sdf_par_source import sdf_par_source
from ..sdf_instrument import sdf_instrument

if CONFIG.use_system_mfpfile:
    from mfpfile import MFPFile
else:
    from ..extern.mfpfile import MFPFile


def mfp2sdf(ibw_file_name, sdf_file_name="", verbose=False, debug=False):
    if verbose:
        print("going to convert {} to {}".format(ibw_file_name, sdf_file_name))
    mfp = MFPFile(ibw_file_name)
    ibw_file = mfp.ibw
    if verbose:
        print("loaded {}".format(ibw_file_name))

    folder, file_name = os.path.split(ibw_file_name)
    
    work_space_root = sdf_object("ws")
    work_space_root.SetName("ibw file \"%s\"" % file_name)
    version = sdf_par("version-in-ibw-file", ibw_file["version"])
    work_space_root.AppendPar(version)

    par_source = sdf_par_source()
    par_source.SetUserName(os.environ['USER'])
    par_source.SetComputerName(os.uname().nodename)
    par_source.SetSDFVersion(__version__)
    par_source.SetConverter('mfp2sdf')
    par_source.SetSourceFile(os.path.abspath(ibw_file_name))
    par_source.SetSourceFileType('mfp-file')

    work_space_root.AppendPar(par_source)

    _wave = ibw_file["wave"]
    data_array = _wave["wData"]
    instr, labels_list = _read_parameters(mfp, _wave, data_array)

    work_space_root.AppendInstrument(instr)

    work_space_data = _write_data_to_work_space(_wave, labels_list)
    work_space_data.SetName("Data")
    work_space_root.AppendObject(work_space_data)

    if verbose:
        print("sdf workspace {} generated".format(work_space_root.name.value))
    
    if sdf_file_name:
        if verbose:
            msg = "writing workspace to sdf file"
            print(msg)
        work_space_root.Save(sdf_file_name)
        if verbose:            
            print("wrote \"{}\"".format(sdf_file_name))
    return work_space_root, ibw_file


def _write_data_to_work_space(wave_dictionary, labels_list):
    data_array = wave_dictionary["wData"]
    data_work_space = sdf_object("ws")
    shape = data_array.shape
    if len(shape) > 3:
        msg = "shape of data array has more than 3 entries, can not handle that!"
        raise RuntimeError(msg)
    if len(shape) == 1:
        dataset = sdf_object("ds")
        dataset.SetName("data")
        data = sdf_data_sc(data_array)
        dataset.SetData(data)
        data_work_space.AppendObject(dataset)
        return data_work_space
    if len(shape) == 3:
        datasets = generate_heightmap_datasets(data_array, shape)
    if len(shape) == 2:
        datasets = generate_single_column_data_sets(data_array, shape)
    if len(datasets) != len(labels_list):
        msg = "found less labels than datasets!"
        raise RuntimeError(msg)
    for i in range(len(datasets)):
        dataset = datasets[i]
        dataset.SetName(labels_list[i])
        data_work_space.AppendObject(dataset)
    return data_work_space


def generate_single_column_data_sets(data_array, shape):
    datasets = []
    for i in range(shape[1]):
        single_column_dataset = sdf_object("ds")
        data_object = sdf_data_sc(data_array[:, i])
        single_column_dataset.SetData(data_object)
        datasets.append(single_column_dataset)
    return datasets


def generate_heightmap_datasets(data_array, shape):
    datasets = []
    for i in range(shape[2]):
        hm_dataset = sdf_object("ds")
        hm_data = sdf_data_mc(data_array[:, :, i])
        hm_dataset.SetData(hm_data)
        datasets.append(hm_dataset)
    return datasets


def _read_parameters(mfp: MFPFile, _wave, data_array) -> Tuple[sdf_instrument, List[str]]:
    data_shape = data_array.shape
    instrument = sdf_instrument('original-parameters')
    if (len(data_shape) > 1):
        labels_par, labels_list = _parse_labels_to_sdf_par(_wave["labels"], data_shape[-1])
    else:
        labels_par, labels_list = _parse_labels_to_sdf_par(_wave["labels"], 0)
    instrument.AppendPar(labels_par)

    if _wave["wave_header"]["kindBits"] == "\x00":
        msg = "replacing HEX 0 bit at field \"kindBits\" in wave header"
        msg += "\n(causes trouble with ascii or XML apparently)"
        logging.warning(msg)
        _wave["wave_header"]["kindBits"] = "HEX 0"
    if _wave["wave_header"]["useBits"] == "\x00":
        msg = "replacing HEX 0 bit at field \"useBits\" in wave header"
        msg += "\n(causes trouble with ascii or XML apparently)"
        logging.warning(msg)
        _wave["wave_header"]["useBits"] = "HEX 0"

    header_elementary_parameter_tuples = parse_parameters(_wave["wave_header"])
    for param in header_elementary_parameter_tuples:
        new_sdf_par = sdf_par(*param)
        instrument.AppendPar(new_sdf_par)

    note_par = sdf_par("mfp-parameters")
    for k in mfp.parameters:
        par_k = sdf_par(k, mfp.parameters[k])
        note_par.AppendPar(par_k)
    instrument.AppendPar(note_par)

    bin_header_parameter_list = parse_parameters(_wave["bin_header"])
    bin_header_par = sdf_par("bin_header", bin_header_parameter_list)
    instrument.AppendPar(bin_header_par)

    formula_par = sdf_par("formula", _wave["formula"])
    instrument.AppendPar(formula_par)

    s_indices_par = sdf_par("sIndices", _wave["sIndices"])
    instrument.AppendPar(s_indices_par)

    data_units_par = sdf_par("data_units", _wave["data_units"])
    instrument.AppendPar(data_units_par)

    dimension_units_par = sdf_par("dimension_units", _wave["dimension_units"])
    instrument.AppendPar(dimension_units_par)

    return instrument, labels_list


def _parse_labels_to_sdf_par(
        labels, expected_number_of_labels) -> Tuple[sdf_par, List[str]]:
    param_list = []
    labels_list = []
    count = 0
    for _list in labels:        
        if len(_list) == 0:
            continue        
        for value in _list:
            if not value:
                continue
            value = value.decode()
            single_label_par = sdf_par("label%i" % (count + 1), value)
            labels_list.append(value)
            param_list.append(single_label_par)
            count += 1
    if len(param_list) != expected_number_of_labels:
        msg = "expected to find %i labels in list,\n" % expected_number_of_labels
        msg += "found %i instead!" % len(param_list) 
        raise RuntimeError(msg)
    labels_par = sdf_par("labels", param_list)
    return labels_par, labels_list
