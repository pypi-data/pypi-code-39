
"""
Functions to convert a SDF file containing force distance curves into
a special force.sdf format.
------------------------------------------------------------------------------
    Copyright (C) 2019 Burkhard Geil, Ilyas Kuhlemann, Filip Savic

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

from typing import List, Tuple, Dict
import os
from warnings import warn
import numpy as np
from ..file_io.sdf_load import sdf_load
from ..sdf_wrapper.sdf_par_source import sdf_par_source
from .. import __version__
from ..sdf_object import sdf_object
from ..sdf_par import sdf_par
from ..sdf_instrument import sdf_instrument
from ..sdf_data_sc import sdf_data_sc


JPK_CHANNELS_OF_INTEREST = {'height': 'height',
                            'vDeflection': 'vDeflection',
                            'hDeflection': 'hDeflection',
                            'measuredHeight': 'measuredHeight',
                            'strainGaugeHeight': 'measuredHeight',
                            'headHeight': 'headHeight'}

MFP_CHANNELS_OF_INTEREST = {'Defl': 'vDeflection'}
REQUIRED_CHANNELS_MFP = ['Defl']

REQUIRED_CHANNELS = ['height', 'vDeflection', 'measuredHeight']


def sdf2forcesdf(sdffile: str, forcesdffile: str=None, use_hex: bool=True) -> sdf_object:
    """
    Converts a SDF file originating from a force distance curve to a SDF
    with a special Force SDF layout. The goal is to have force distance curves
    in a unified structure, to make using SDF files for analyses more convenient,
    regardless of the original file format of the force distance curve.

    :param sdffile: Path to input SDF file.
    :param forcesdffile: Path to output Force SDF file, should have extension .force.sdf.
    :param use_hex: Will use dtype hex for sdf_data objects if True.
    :return: Returns the resulting Force SDF as sdf_object.
    """
    sdf = sdf_load(sdffile)
    src_type = sdf.GetPar('source-of-sdf-file')['source-file-type'].value

    par_source = sdf_par_source()
    par_source.FillDefaultSystemParameters()
    par_source.SetConverter('sdf2forcesdf')
    par_source.SetSourceFile(os.path.abspath(sdffile))
    if src_type == 'jpk-force':
        ws = _jpk_force_sdf2forcesdf(sdf, use_hex)
        par_source.SetSourceFileType('converted-jpk-force')
    elif src_type == 'mfp-file':
        ws = _mfp_file_sdf2forcesdf(sdf, use_hex)
        par_source.SetSourceFileType('converted-mfp-file')
    else:
        msg = f"Invalid source file type '{src_type}' to convert to force.sdf!"
        raise RuntimeError(msg)

    ws.AppendPar(par_source)

    if forcesdffile:
        ws.Save(forcesdffile)

    return ws


def _mfp_file_sdf2forcesdf(sdf: sdf_object, use_hex: bool) -> sdf_object:
    msg = 'sdf does not contain a force distance curve, or was not correctly converted '
    msg += 'by mfp2sdf.'
    assert _is_mfp_force_distance_curve(sdf), msg
    ws = sdf_object('ws')
    ws.SetName('ForceSDF ' + sdf.name.value)
    instrument, segment_indices = _parse_instrument_parameters_mfp(
        sdf.GetInstrument(0)['mfp-parameters'])
    ws.AppendInstrument(instrument)

    channel_data = {}
    for ch in REQUIRED_CHANNELS_MFP:
        channel_data[ch] = sdf['Data'][ch].value.data

    for i in range(len(segment_indices)-1):
        start = segment_indices[i]
        end = segment_indices[i+1]
        ws_seg = sdf_object('ws')
        ws_seg.SetName('segment {}'.format(i))

        datasets = _create_datasets_for_segment(channel_data, start, end, use_hex)
        for ds in datasets:
            ws_seg.AppendObject(ds)

        instrument_seg = _parse_segment_instrument_parameters_mfp()
        ws_seg.AppendInstrument(instrument_seg)
        ws.AppendObject(ws_seg)
    raise NotImplementedError
    return ws

def _create_datasets_for_segment(channel_data: Dict[str, np.ndarray],
                                 start: int, end: int, use_hex: bool) -> List[sdf_object]:
    datasets = []
    for ch in channel_data:
        ds = sdf_object('ds')
        ds.SetName(MFP_CHANNELS_OF_INTEREST[ch])
        if use_hex:
            data = sdf_data_sc(channel_data[ch][start:end], dtype='hex')
        else:
            data = sdf_data_sc(channel_data[ch][start:end])
        ds.SetData(data)
        datasets.append(ds)
    return datasets


def _parse_segment_instrument_parameters_mfp():
    raise NotImplementedError

def _parse_instrument_parameters_mfp(mfp_par: sdf_par) -> Tuple[sdf_instrument, List[int]]:
    instr = sdf_instrument('parameters')
    par_sensitivity = sdf_par('sensitivity', mfp_par['InvOLS'].value)
    par_spring_const = sdf_par('spring_constant', mfp_par['SpringConstant'].value)
    instr.AppendPar(par_sensitivity)
    instr.AppendPar(par_spring_const)
    segment_indices = [int(i) for i in mfp_par['Indexes'].value.split(',')]
    return instr, segment_indices


def _is_mfp_force_distance_curve(sdf: sdf_object) -> bool:
    ws_data = sdf['Data']
    for ch in REQUIRED_CHANNELS_MFP:
        if ch not in ws_data:
            return False
    return True


def _determine_channels_to_be_used_jpk(segment: sdf_object) -> List[str]:
    channels = []
    for ds in segment.value:
        if ds.name.value not in JPK_CHANNELS_OF_INTEREST:
            continue
        channels.append(ds.name.value)
    if 'measuredHeight' in channels:
        if 'strainGaugeHeight' in channels:
            channels.remove('strainGaugeHeight')
        if 'capacitiveSensorHeight' in channels:
            channels.remove('capacitiveSensorHeight')

    channels_for_validation = [JPK_CHANNELS_OF_INTEREST[ch] for ch in channels]

    for ch in REQUIRED_CHANNELS:
        if ch not in channels_for_validation:
            msg = "channel '{}' or equivalent not found in segment '{}'"
            raise RuntimeError(msg.format(ch, segment.name.value))
    return channels


def _jpk_force_sdf2forcesdf(sdf: sdf_object, use_hex: bool) -> sdf_object:
    """
    Converts an SDF file containing a force distance curve converted with
    jpk2sdf to a SDF file of the Force SDF layout.

    :param sdf: sdf_object of the source SDF file.
    :param use_hex: Will set dtype of data arrays to hex if True.
    :return: The converted SDF of special Force SDF layout.
    """
    ws = sdf_object('ws')
    ws.SetName('ForceSDF ' + sdf.name.value)

    for jpk_seg in sdf.value:
        seg, i = str(jpk_seg.name.value).split()
        if seg != 'segment':
            raise RuntimeError('workspace in sdf file is not a jpk force segment')
        i = int(i)
        channels = _determine_channels_to_be_used_jpk(jpk_seg)

        ws_seg = sdf_object('ws')
        ws_seg.SetName('segment {}'.format(i))

        channel_parameters = jpk_seg.GetInstrument('original-parameters').\
            GetPar('channel')

        data_sets = _parse_datasets(jpk_seg.value, channels, channel_parameters, use_hex)

        for ds in data_sets:
            ws_seg.AppendObject(ds)

        instrument_seg = _parse_segment_instrument_parameters(jpk_seg)
        ws_seg.AppendInstrument(instrument_seg)

        ws.AppendObject(ws_seg)

    instrument = _parse_instrument_parameters_jpk(
        sdf.value[0].GetInstrument('original-parameters'))

    ws.AppendInstrument(instrument)

    return ws


def _parse_instrument_parameters_jpk(jpk_instrument: sdf_instrument) -> sdf_instrument:
    instrument = sdf_instrument('parameters')

    vDeflection_parameters = jpk_instrument['channel']['vDeflection']
    conv_parameters = vDeflection_parameters['conversion-set']['conversion']

    par_sensitivity = sdf_par('sensitivity',
                              conv_parameters['distance']['scaling']['multiplier'].value)
    par_spring_constant = sdf_par('spring_constant',
                                  conv_parameters['force']['scaling']['multiplier'].value)

    instrument.AppendPar(par_sensitivity)
    instrument.AppendPar(par_spring_constant)

    return instrument


def _parse_segment_instrument_parameters(segment: sdf_object) -> sdf_instrument:
    instrument = sdf_instrument('segment-parameters')
    instr_segment = segment.GetInstrument(0)
    seg_settings = instr_segment['force-segment-header']['settings']['segment-settings']

    par_duration = sdf_par('duration', seg_settings['duration'].value)
    par_direction = sdf_par('direction', seg_settings['type'].value)
    instrument.AppendPar(par_duration)
    instrument.AppendPar(par_direction)

    try:
        pos_map = instr_segment['force-segment-header']['environment']['xy-scanner-position-map']
        par_pos_index = sdf_par('position_index', pos_map['xy-scanners']['position-index'].value)
        par_pos_x = sdf_par('x', pos_map['xy-scanner']['tip-scanner']['start-position']['x'].value)
        par_pos_y = sdf_par('y', pos_map['xy-scanner']['tip-scanner']['start-position']['y'].value)
    except KeyError:
        warn('can\'t parse position parameters, will set them to none!')
        par_pos_index = sdf_par('position_index', 'None')
        par_pos_x = sdf_par('x', 'None')
        par_pos_y = sdf_par('y', 'None')

    instrument.AppendPar(par_pos_index)
    instrument.AppendPar(par_pos_x)
    instrument.AppendPar(par_pos_y)

    return instrument


def _parse_datasets(datasets_sdf: List[sdf_object], channels: List[str],
                    channel_parameters: sdf_par, use_hex: bool) -> List[sdf_object]:
    datasets = []
    for ds_sdf in datasets_sdf:
        if ds_sdf.name.value not in channels:
            continue
        ds = _parse_dataset(ds_sdf, channel_parameters, use_hex)
        datasets.append(ds)

    return datasets


def _parse_dataset(ds_sdf: sdf_object, channel_parameters: sdf_par,
                   use_hex: bool) -> sdf_object:
    ds = sdf_object('ds')

    ds.SetName(JPK_CHANNELS_OF_INTEREST[ds_sdf.name.value])
    current_ds_par = channel_parameters.GetChild(ds_sdf.name.value)

    multiplier, offset = _extract_conversion_parameters(current_ds_par)

    if use_hex:
        data = sdf_data_sc(ds_sdf.value.data, dtype='hex',
                           multiplier=multiplier, offset=offset)
    else:
        data = sdf_data_sc(ds_sdf.value.data, dtype='int',
                           multiplier=multiplier, offset=offset)

    ds.SetData(data)

    return ds


def _extract_conversion_parameters(par: sdf_par) -> Tuple[float, float]:
    conv_set = par['conversion-set']
    try:
        encoder = par['data']['encoder']['scaling']
    except KeyError:
        encoder = par['encoder']['scaling']
    mult = float(encoder['multiplier'].value)
    offs = float(encoder['offset'].value)

    conversions = _determine_conversions(conv_set)

    for conv in conversions:
        m = float(conv_set['conversion'][conv]['scaling']['multiplier'].value)
        b = float(conv_set['conversion'][conv]['scaling']['offset'].value)

        mult *= m
        offs = m*offs + b

    return mult, offs


def _determine_conversions(conv_set: sdf_par) -> List[str]:
    conversions = [conv_set['conversions']['default'].value]
    raw_name = conv_set['conversions']['base'].value

    chain_complete = False

    if conversions[0] == raw_name:
        chain_complete = True
        conversions = []
    while not chain_complete:
        key = conversions[-1]
        previous_conversion = conv_set['conversion'][key]['base-calibration-slot'].value
        if previous_conversion == raw_name:
            chain_complete = True
        else:
            conversions.append(previous_conversion)

    conversions.reverse()
    return conversions
