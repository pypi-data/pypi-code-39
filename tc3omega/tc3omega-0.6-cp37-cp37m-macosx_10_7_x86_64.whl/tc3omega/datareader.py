#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

"""
This module reads and distributes the measured data stored in '.csv' in the
file 'file_path'. The 'indexer' method allows for lower and upper bounds to be
set on the frequency range. 'indexer' extracts only the datapoints
corresponding to frequencies between 'minfval' and 'maxfval'.
"""

# TODO: include handling of Vsh_1w_o and Vs_3w_o once available


def Data(file_path, minfval=100, maxfval=12000):
    data = np.loadtxt(file_path, delimiter=',',
                      skiprows=1, usecols=range(0, 5), dtype=np.double)
    min_idx, max_idx = indexer(data[:, 0], minfval, maxfval)
    f_all = data[:, 0][min_idx: max_idx + 1]
    Vs_3w = data[:, 1][min_idx: max_idx + 1]
    Vs_1w = data[:, 2][min_idx: max_idx + 1]
    Vs_1w_o = data[:, 3][min_idx: max_idx + 1]
    Vsh_1w = data[:, 4][min_idx: max_idx + 1]
    return {'input_frequencies': f_all,
            'real_sample_V3ω': Vs_3w,
            'real_sample_V1ω': Vs_1w,
            'imag_sample_V1ω': Vs_1w_o,
            'real_shunt_V1ω': Vsh_1w}


def indexer(arr, minfval, maxfval):
    diff1, diff2 = abs(arr - minfval), abs(arr - maxfval)
    idx1 = int(np.where(diff1 == min(diff1))[0])
    idx2 = int(np.where(diff2 == min(diff2))[0])
    return idx1, idx2
