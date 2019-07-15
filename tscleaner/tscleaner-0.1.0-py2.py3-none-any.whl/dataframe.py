import os
import json

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tscleaner.reservoir_series as resser

from datetime import datetime, timedelta
from sklearn.neighbors import NearestNeighbors


def dataframe(
              fn,
              keys=['water_area_filled',
                    'water_area_filled_fraction',
                    'water_area_p',
                    'water_area_value',
                    'water_area_time',
                    'quality_score',
                    'ndwi_threshold'],
              date_index='water_area_time'
             ):

    """
    dataframe.dataframe() converts a reservior surface area .json file into a
    pandas.DataFrame().

    Arguments:
        fn {str} -- File input

    Keyword Arguments:
        keys {list} -- Keys of which a column will be made in the dataframe.
        (default: {['water_area_filled','water_area_filled_fraction',
                    'water_area_p','water_area_value',
                    'water_area_time','quality_score',
                    'ndwi_threshold']})

        date_index {str} -- Date key which will be used as index.
        (default: {'water_area_time'})

    Returns:
        df {pd.DataFrame} -- Pandas DataFrame.
    """
    d = json.load(open(fn))['features'][0]['properties']
    index = d[date_index]
    index = [datetime.fromtimestamp(tt/1000).date() for tt in index]

    select_data = {x: d[x] for x in keys}

    df = pd.DataFrame(select_data, index)
    df.index.name = 'date'

    return df


def read_coords(fn):
    """
    Reads location geometry (x,y) from JSON reservoir time series file
    Input:
        fn: str - filename
    Output:
        x, y: floats - longitude and latitude of reservoir location
    """
    with open(fn, 'r') as f:
        return json.loads(f.read())['features'][0]['geometry']['coordinates']


def remove_double_dates(data_original):
    """
    Removes datapoints based on duplicates in dates.

    Arguments:
        data_original {pd.DataFrame} -- pandas.DataFrame

    Returns:
        df_new {pd.DataFrame} -- pandas.DataFrame containing preserved values

        df_out {pd.DataFrame} -- pandas.DataFrame containing removed values
    """
    df_new = data_original.copy(deep=True)

    df_new['date2'] = df_new.index
    df_new = df_new.sort_values(by=['date', 'water_area_filled'],
                                ascending=[True, False])
    df_new = df_new.drop_duplicates('date2', keep='first')
    df_new.drop(columns='date2', inplace=True)

    df_out = pd.concat([df_new, data_original], sort=False)
    df_out = df_out.drop_duplicates(keep=False)

    return df_new, df_out


def remove_outliers_frac(
                         data,
                         thres_fraction=0.5
                        ):

    """
    Removes optional ouliers from reservior surface area timeseries
    based on the value of water_area_filled_fraction.

    Arguments:
        data {pd.DataFrame} -- Usually output from dataframe.dataframe()

    Keyword Arguments:
        thres_fraction {float} -- Maximum value for
        'water_area_filled_fraction'. (default: {0.5})

    Returns:
        df_new {pd.DataFrame} -- Pandas DataFrame with preserved values.

        df_out {pd.DataFrame} -- Pandas DataFrame containing all removed
        values.
    """

    df_new = data.copy(deep=True)

    df_new = df_new[df_new.water_area_filled_fraction.values < thres_fraction]

    df_out = pd.concat([df_new, data], sort=False)
    df_out = df_out.drop_duplicates(keep=False)

    return df_new, df_out


def remove_outliers_quantile(
                             data_continuous,
                             data_original,
                             window=100,
                             f_std=2,
                             thres_quant=0.90
                            ):
    """
    Removes optional ouliers from reservior surface area timeseries
    based on the distance from the 90% (default) quantile. Based on
    pandas.DataFrame.rolling().

    Arguments:
        data_continuous {pd.DataFrame} -- Pandas DataFrame containing daily
        values

        data_original {pd.DataFrame} -- Pandas DataFrame containing original
        data points

    Keyword Arguments:
        window {int} -- Size of the moving window. This is the number of
        observations used for calculating the statistic. Each window will be a
        fixed size. (default: {100})

        f_std {int} -- Maximum allowed standard deviation distance from the
        quantile (default: {2})

        thres_quant {float} -- Quantile value (default: {0.90})

    Returns:
        df_new {pd.DataFrame} -- Pandas DataFrame with preserved values.

        df_out {pd.DataFrame} -- Pandas DataFrame containing all removed
        values.
    """

    data = data_continuous
    point = data_original
    df_new = point.copy(deep=True)

    quant = data.rolling(window,
                         min_periods=window//2,
                         center=True).quantile(thres_quant)
    std = data.rolling(window,
                       min_periods=1,
                       center=True).std()

    low = min(quant.index)
    high = max(quant.index)

    list_out = []

    for date in df_new.index:
        if date >= low and date <= high:
            d_app = float(quant.loc[date].values)
            d_dot = df_new.water_area_filled.loc[date]
            d_abs = abs(d_app - d_dot)
            d_std = float(std.loc[date].values)

            if d_abs > (f_std*d_std) and d_std != np.nan:
                list_out.append(df_new.loc[date])

    df_out = pd.DataFrame(list_out)
    df_new = pd.concat([df_new, df_out], sort=False)
    df_new = df_new.drop_duplicates(keep=False)

    return df_new, df_out


def remove_outliers_std(
                        data_original,
                        data_continuous,
                        window=180,
                        f_std=2
                       ):
    """[summary]

    Arguments:
        data_original {[type]} -- [description]

        data_daily {[type]} -- [description]

    Keyword Arguments:
        window {int} -- [description] (default: {180})

    Returns:
        [type] -- [description]
    """
    df_new = data_original.copy(deep=True)
    med = data_continuous.rolling(window,
                                  min_periods=1,
                                  center=True).median()
    std = np.mean(data_continuous.rolling(window,
                                          min_periods=1,
                                          center=True).std().values)
    low = min(med.index)
    high = max(med.index)

    list_out = []
    list_abs = []

    for date in df_new.index:
        if date >= low and date <= high:
            d_app = float(med.loc[date].values)
            d_dot = df_new.water_area_filled.loc[date]
            d_abs = abs(d_app - d_dot)

            if d_abs > (f_std*std):
                list_out.append(df_new.loc[date])
                list_abs.append(d_abs)

    df_out = pd.DataFrame(list_out)
    df_new = pd.concat([df_new, df_out], sort=False)
    df_new = df_new.drop_duplicates(keep=False)
    df_out['abs_diff_to_median'] = list_abs

    return df_new, df_out


def nearest(
            data,
            n=5
           ):
    """
    n=Number of neighbors to use by default for :meth:`kneighbors` queries.
    """
    NN = NearestNeighbors(n_neighbors=n,)
    result = NN.fit(data)
    dist = result.kneighbors(data)[0][:, -1]
    near = pd.DataFrame({'date': data.index,
                         'neighbor': dist})
    near.set_index('date', inplace=True)
    return near


def nan_values(data):
    """[summary]

    Arguments:
        data {[type]} -- [description]

    Returns:
        [type] -- [description]
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
    df = pd.DataFrame({'date': dates, 'water_area_filled': areas})
    df.set_index('date', inplace=True)
    df.index = [i.date() for i in df.index]

    return df


def remove_outliers(data):
    # removal of double dates
    # temporarily remove outliers based on water_area_filled_fraction
    d_new, d_out = remove_double_dates(data)
    d_new_temp_1 = remove_outliers_frac(d_new,
                                        thres_fraction=0.5)[0]

    # interpolate the output of previous step towards daily values
    # temporaily remove outliers based on the distance from the 90% quantile
    d_daily = resser.daily_values(d_new_temp_1,
                                  inter_method='slinear',
                                  mirroring=4)
    d_new_temp_2 = remove_outliers_quantile(d_daily,
                                            d_new_temp_1,
                                            window=100,
                                            f_std=2,
                                            thres_quant=0.90)[0]

    # interpolate the output of previous step towards daily values
    # remove outliers based on the distance from the median
    d_daily_2 = resser.daily_values(d_new_temp_2,
                                    inter_method='slinear')
    d_new_3, d_out_3 = remove_outliers_std(d_new,
                                           d_daily_2,
                                           window=180,
                                           f_std=2)

    # rename the preserved values dataframe and combine the removed data points
    d_new = d_new_3
    d_out = pd.concat([d_out, d_out_3], sort=False)

    return d_new, d_out
