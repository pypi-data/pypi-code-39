import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import scipy

from datetime import datetime, timedelta
from PyEMD import EMD
import pywt as pywt


def daily_values(
                 data,
                 inter_method='akima',
                 mirroring=2,
                 noise_removal=False,
                 IMF_removal=0
                ):

    """
    Interpolation of incomplete timeseries towards daily using Emperical Mode
    Decomposition (EMD) from the library pyEMD.

    Arguments:
        data {pd.DataFrame} -- Pandas DataFrame in the format:
        pd.DataFrame({'date': date, 'area': area})

    Keyword Arguments:
        inter_method {str} -- Interpolation method for spline signal.
        'akima', 'slinear' or 'cubic'. (default: {'akima'})

        mirroring {int} -- Number of extrema used in boundary mirroring.
        (default: {2})

        noise_removal {str} -- True or False, whether IMF's will set to zero
        in order to remove noise (default: {False})

        IMF_removal {int} -- if noise_removal is True, number or IMF's which
        will be removed (default: {0})

    Returns:
        ts_day {pd.DataFrame} -- Daily timeseries. Pandas DataFrame with dates
        as index and areas in column 0.
    """

    # Create a date and area array for daily data (all areas are set to NaN)
    length = len(data.index)
    dates = np.arange(data.index.values[0],
                      data.index.values[length-1] +
                      timedelta(days=1),
                      dtype='datetime64[D]')
    areas = np.full(len(dates), np.NaN)

    # Fill dates and areas with data from datasource
    j0 = 0

    for i in range(length):
        for j in range(j0, len(dates)):
            # if date source equals date array:
            # fill areas with area from datasource
            if data.index[i] == dates[j]:
                areas[j] = data.water_area_filled.values[i]
                j0 = j
                break

    # Create a DataFrame (pandas) from arrays
    df = pd.DataFrame({'date': dates, 'area': areas})

    # Make a array withouth the NaN values (index values stay the same)
    dfn = df.copy()
    dfn.dropna(axis=0, inplace=True)

    # The interpolation is based on the IMF (Intristic Mode Functions) which is
    # determined by the Emperical Mode Decomposition (EMD)
    IMF = EMD().emd(S=dfn.area.values, T=dfn.index.values)

    # Interpolation is done with the spline function.
    # After this, all IMF's are summed together with 'signal' as output
    IMFnew = np.zeros((len(IMF), len(dates)))

    for aa in range(len(IMFnew)):
        extr = np.zeros((2, len(IMF[aa])))
        extr[0] = dfn.index.values
        extr[1] = IMF[aa]
        IMFnew[aa] = EMD(spline_kind=inter_method,
                         nbsym=mirroring).spline_points(T=df.index.values,
                                                        extrema=extr)[1]
        # if noise reduction is applied, set IMF to zeros
        if aa <= IMF_removal and noise_removal is True:
            IMFnew[aa] = np.zeros_like(IMFnew[aa])

    signal = sum(IMFnew, 0)

    # new dataframe with signal as input and resampled to desired timeframe
    ts_day = pd.DataFrame({'date': dates,
                           'area': signal})

    ts_day.set_index('date', inplace=True)
    ts_day.index = [i.date() for i in ts_day.index]

    return ts_day


def savitzky_golay(
                   data,
                   window_length=201,
                   polyorder=4
                  ):

    """
    Apply a Savitzky-Golay filter to a pd.DataFrame.

    Arguments:
        data {pd.DataFrame} -- Output of reservoir_series.daily_values()

    Keyword Arguments:
        window_length {int} -- The length of the filter window (i.e. the
        number of coefficients). Window_length must be a positive odd integer.
        (default: {201})

        polyorder {int} -- The order of the polynomial used to fit the samples.
        polyorder must be less than window_length. (default: {4})

    Returns:
        savgol {pd.DataFrame} -- Daily timeseries based on the Savitzky-Golay
        filter
    """

    areas = scipy.signal.savgol_filter(x=data.area,
                                       window_length=window_length,
                                       polyorder=polyorder)
    savgol = pd.DataFrame({'date': data.index,
                           'area': areas})
    savgol.set_index('date', inplace=True)

    return savgol


def min_max(
            data,
            order=100
           ):

    """
    Find valleys and peaks of a dataset.

    Arguments:
        data {pd.DataFrame} -- pd.DataFrame

    Keyword Arguments:
        order {int} -- How many points on each side to use for the comparison
        to consider a point a valley or peak. (default: {100})

    Returns:
        valleys {pd.DataFrame} -- DataFrame with valley locations (datestring)
        and corresponding values.

        peaks {pd.DataFrame} -- DataFrame with peak locations (datestring)
        and corresponding values.
    """

    # determine locations valleys and peaks
    valley_indexes = scipy.signal.argrelmin(data.area.values, order=order)[0]
    peak_indexes = scipy.signal.argrelmax(data.area.values, order=order)[0]

    # find corresponding areas
    valleys = pd.DataFrame()
    peaks = pd.DataFrame()

    dd = 0
    for cc in valley_indexes:
        valleys.at[dd, 'date'] = data.index[cc]
        valleys.at[dd, 'area'] = data.area[cc]
        dd += 1

    ff = 0
    for ee in peak_indexes:
        peaks.at[ff, 'date'] = data.index[ee]
        peaks.at[ff, 'area'] = data.area[ee]
        ff += 1

    valleys.set_index('date', inplace=True)
    peaks.set_index('date', inplace=True)

    return valleys, peaks


def wavelets(
             data,
             wave_name='db25',
             level=8,
             level_output=1
            ):
    """
    Wavelet approximation of a dataset using PyWavelets.

    Arguments:
        data {pd.DataFrame} -- pd.DataFrame. Usualy result of
        reservoir_series.daily_values()

    Keyword Arguments:
        wave_name {str} -- Wavelet to use. (default: {'db25'}) Possible
        waveletfamilies are 'bior', 'coif', 'db', 'dmey', 'haar', 'rbio'
        and 'sym'

        level {int} -- Decomposition level (must be >= 0). If level is
        None then it will be calculated using the dwt_max_level function.
        (default: {8})

        level_output {int} -- level of recomposed signal. (default: {1})

    Returns:
        df_wl {pd.DataFrame} -- Pandas DataFrame with dates as index and
        areas in column 0.
    """
    wave = pywt.Wavelet(wave_name)
    coeffs = pywt.wavedec(data.area, wavelet=wave, level=level)

    L = len(data.index)

    wl = pywt.waverec(coeffs[:-(level-level_output+1)] +
                      [None]*(level-level_output+1),
                      wave)[:L]

    df_wl = pd.DataFrame({'date': data.index, 'area': wl})
    df_wl.set_index('date', inplace=True)

    return df_wl


def steps(
          data,
          window=365,
          threshold=0.5
         ):
    """[summary]

    Arguments:
        data {pd.DataFrame} -- Pandas Dataframe with indexname 'date' and
        columnname 'area' containing areas. Usually the output of the
        smoothing function.

    Keyword Arguments:
        window {int} -- [description] (default: {365})
        threshold {float} -- [description] (default: {0.5})

    Returns:
        [type] -- [description]
    """
    d_max = data.rolling(window=window, min_periods=1, center=True).max()
    d_min = data.rolling(window=window, min_periods=1, center=True).min()
    d_dif = d_max.copy(deep=True)
    d_dif.area = d_max.area-d_min.area

    w_range = max(data.area)-min(data.area)
    thres = w_range*threshold
    steps_index = scipy.signal.find_peaks(d_dif.area.values,
                                          height=thres,
                                          plateau_size=[0, window])[0]

    gradient = np.gradient(data.area.values)
    win = 100
    ret = np.cumsum(gradient, dtype=float)
    ret[win:] = ret[win:] - ret[:-win]

    steps = pd.DataFrame()

    aa = 0
    for bb in steps_index:
        steps.at[aa, 'date'] = data.index[bb]
        steps.at[aa, 'area_min'] = d_min.area[bb]
        steps.at[aa, 'area_max'] = d_max.area[bb]
        steps.at[aa, 'abs_step'] = d_dif.area[bb]
        steps.at[aa, 'rel_step'] = d_dif.area[bb]/w_range
        if ret[bb] > 0:
            steps.at[aa, 'up_down'] = 1
        else:
            steps.at[aa, 'up_down'] = -1
        aa += 1
    if len(steps) > 0:
        steps.set_index('date', inplace=True)

    return steps


def find_step_up(
                 data,
                 window_width=365,
                 step_thres=0.3
                ):
    """
    Find steps going up in reservoir surface area time series

    Arguments:
        data {pd.DataFrame} -- Pandas Dataframe with indexname 'date' and
        columnname 'area' containing areas

    Keyword Arguments:
        window_width {int} -- Size of the moving window. This is the number of
        observations used for calculating the statistic. (default: {365})

        step_thres {float} -- Minimum value for what is seen as a significant
        step (default: {0.3})

    Returns:
        df {pd.DataFrame} -- Pandas DataFrame containing the minimum and
        maximum area at the step, absolute and relative step and start and
        end date. The index value is the average of the start and end date.
    """
    row_list = []

    data_min = min(data.area.values)
    data_max = max(data.area.values)
    data_range = (data_max - data_min)
    threshold = max(step_thres-0.05, 0) * data_range

    d_wave_median = data.rolling(window=window_width, center=True).median()
    d_wave_min = data.rolling(window=window_width, center=True).min()
    d_wave_max = data.rolling(window=window_width, center=True).max()

    n = 0

    for i, med in enumerate(d_wave_median.area):
        if i > 0:
            if med > d_wave_median.area[i-1]:
                n += 1

            if med <= d_wave_median.area[i-1]:

                if med-d_wave_median.area[i-n] > threshold:
                    day_step = (d_wave_median.index[i] -
                                timedelta(days=round(n/2, 0)))
                    min_step = float(d_wave_min.values[i])
                    max_step = float(d_wave_max.values[i])
                    stepsize = max_step-min_step
                    factor_step = float(stepsize/data_range)

                    if factor_step > step_thres:
                        d_step = {'min_step': min_step,
                                  'max_step': max_step,
                                  'abs_step': stepsize,
                                  'rel_step': factor_step,
                                  'start_date': d_wave_median.index[i-n],
                                  'end_date': d_wave_median.index[i],
                                  'date': day_step}
                        row_list.append(d_step)

                n = 0

    df = pd.DataFrame(row_list, columns=['min_step', 'max_step',
                                         'abs_step', 'rel_step',
                                         'start_date', 'end_date',
                                         'date'])
    df.set_index('date', inplace=True)
    return df


def confidence_band(
                    data,
                    window_width=100,
                    lim_max=0.9,
                    lim_min=0.1
                   ):
    """[summary]

    Arguments:
        data {[type]} -- [description]

    Keyword Arguments:
        window_width {int} -- [description] (default: {200})

        lim_max {float} -- [description] (default: {0.9})

        lim_min {float} -- [description] (default: {0.1})

    Returns:
        [type] -- [description]
    """
    data_max = data.rolling(window=window_width,
                            min_periods=1,
                            center=True).quantile(lim_max)
    data_min = data.rolling(window=window_width,
                            min_periods=1,
                            center=True).quantile(lim_min)

    data_max = savitzky_golay(data_max)
    data_min = savitzky_golay(data_min)

    return data_max, data_min
