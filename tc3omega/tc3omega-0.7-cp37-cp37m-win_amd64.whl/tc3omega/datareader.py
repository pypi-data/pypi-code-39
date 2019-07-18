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


class DataError(Exception):
    pass


def Data(file_path, row_range=None):
    data = np.loadtxt(file_path, delimiter=',',
                      skiprows=1, usecols=range(0, 5), dtype=np.double)
    if row_range is None:
        f_all = data[:, 0]
        Vs_3w = data[:, 1]
        Vs_1w = data[:, 2]
        Vs_1w_o = data[:, 3]
        Vsh_1w = data[:, 4]
        return {'input_frequencies': f_all,
                'sample_V3w_real': Vs_3w,
                'sample_V1w_real': Vs_1w,
                'sample_V1w_imag': Vs_1w_o,
                'shunt_V1w_real': Vsh_1w}
    else:
        a, b = row_range
        f_all = data[:, 0][a-2:b-1]
        Vs_3w = data[:, 1][a-2:b-1]
        Vs_1w = data[:, 2][a-2:b-1]
        Vs_1w_o = data[:, 3][a-2:b-1]
        Vsh_1w = data[:, 4][a-2:b-1]
        return {'row_range': row_range,
                'input_frequencies': f_all,
                'sample_V3w_real': Vs_3w,
                'sample_V1w_real': Vs_1w,
                'sample_V1w_imag': Vs_1w_o,
                'shunt_V1w_real': Vsh_1w}
