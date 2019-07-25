"""
Library storing utility functions used by the pyesx modules

A. Enguehard - 07/2019
"""

# from math import *
import numpy as np
import pandas as pd
# import sys
import jdcal
import datetime

# Utils functions :
# -----------------


# ======= Frame management ======


def filterframe(frame, mindate=None, maxdate=None):
    """Keep only the values of a dataframe between the indicated dates

    Parameters:
    ----------
    * frame : (pandas.DataFrame)
        Data to filter
    * mindate : (datetime.datetime object) - Default = None
        First date in the dataframe
        If None will keep the data from the first date of the frame
    * maxdate : (datetime.datetime object) - Default = None
        Last date in the dataframe
        If None will keep the data up to the last date of the frame

    Outputs:
    -------
    * frame : (pandas.DataFrame)
        Modified DataFrame
    """
    # Get the first date : If None keep first occuring date
    if mindate is not None:
        idatemin = is_in(mindate, frame.index)[1]  # Check if in the intervalle
        if idatemin == -1:  # Not in the intervalle
            idatemin = 0    # Keep the first date of the dataframe
    else:
        idatemin = 0
    # Get the last date : If None keep last occuring date
    if maxdate is not None:
        idatemax = is_in(maxdate, frame.index)[1]  # Check if in the intervalle
        if idatemax == -1:  # Not in the intervalle
            idatemax = len(frame.index) - 1  # Keep the last date of the frame
    else:
        idatemax = len(frame.index) - 1
    # Filter
    frame = frame.iloc[idatemin:idatemax, :]
    return frame


def filterseries(series, mindate=None, maxdate=None):
    """Keep only the values of a series between the indicated dates

    Parameters:
    ----------
    * series : (pandas.Series)
        Data to filter
    * mindate : (datetime.datetime object) - Default = None
        First date in the dataframe
        If None will keep the data from the first date of the frame
    * maxdate : (datetime.datetime object) - Default = None
        Last date in the dataframe
        If None will keep the data up to the last date of the frame

    Outputs:
    -------
    * series : (pandas.Series)
        Modified Series
    """
    if mindate is not None:
        idatemin = is_in(mindate, series.index)[1]
        if idatemin == -1:
            idatemin = 0
    else:
        idatemin = 0
    if maxdate is not None:
        idatemax = is_in(maxdate, series.index)[1]
        if idatemax == -1:
            idatemax = len(series.index) - 1
    else:
        idatemax = len(series.index) - 1
    return series[idatemin:idatemax]


def firstdate(time_mod, time_obs):
    """Gives the first common date of time_mod and time_obs
    WARNING : Use only sorted time series with datetime / Timestamp objects

    Parameters:
    ----------
    * time_mod : (pd.Series of dates)
        Series giving the dates of modeled values (usually)
        ex: 2012-02-01 10:00:00   2012-02-01 10:00:00
            2012-02-01 11:30:00   2012-02-01 11:30:00
            ...
    * time_obs : (pd.Series of dates)
        Series giving the dates of observed values (usually)

    Outputs:
    -------
    * starting_date0 : (datetime) first date of time_mod in the intersection
    * starting_date1 : (datetime) first date of time_obs in the intersection
    * i0 : (int) index of the first date of time_mod in the intersection
    * i1 : (int) index of the first date of time_obs in the intersection
    """
    # Series0 does start before the other: otherwise reverse
    reversed = False
    if time_mod[0] > time_obs[0]:
        reversed = True
        time_mod, time_obs = time_obs, time_mod
    i = 0
    # Going on until reaching date(time_mod) > date(time_obs)
    while time_mod[i] < time_obs[0] and i < len(time_mod)-1:
        print(time_mod[i] < time_obs[0])
        i = i + 1
    # Case i=0 match
    eq = time_mod[i] == time_obs[0]
    if not reversed and not eq:
        starting_date0 = time_mod[i-1]
        i0 = i - 1
    else:
        starting_date0 = time_mod[i]
        i0 = i
    starting_date1 = time_obs[0]
    i1 = 0
    # If not reached then no starting date found
    if starting_date0 == time_mod[len(time_mod) - 1] and not eq:
        starting_date0, starting_date1 = None, None
    # Get the right order if reversed before
    if reversed is True:
        starting_date0, starting_date1 = starting_date1, starting_date0
        i0, i1 = i1, i0
    return starting_date0, starting_date1, i0, i1


def lastdate(time_mod, time_obs):
    """Gives the last common date of time_mod and time_obs
    WARNING : Use only sorted time series with datetime / Timestamp objects

    Parameters:
    ----------
    * time_mod : (pd.Series of dates)
        Series giving the dates of modeled values (usually)
        ex: 2012-02-01 10:00:00   2012-02-01 10:00:00
            2012-02-01 11:30:00   2012-02-01 11:30:00
            ...
    * time_obs : (pd.Series of dates)
        Series giving the dates of observed values (usually)

    Outputs:
    -------
    * starting_date0 : (datetime) last date of time_mod in the intersection
    * starting_date1 : (datetime) last date of time_obs in the intersection
    * i0 : (int) index of the last date of time_mod in the intersection
    * i1 : (int) index of the last date of time_obs in the intersection
    """
    # Series1 does end before the other: otherwise reverse
    len0 = len(time_mod)
    len1 = len(time_obs)
    reversed = False
    if time_mod[len0 - 1] < time_obs[len1 - 1]:
        reversed = True
        time_mod, time_obs = time_obs, time_mod
        len0, len1 = len1, len0
    i = 0
    # Going on with time until reaching the last common date
    while time_mod[i] < time_obs[len1 - 1] and i < len(time_mod)-1:
        i = i + 1
    eq = time_mod[i] == time_obs[len1 - 1]
    if not reversed and not eq:
        last_date0 = time_mod[i + 1]
        i0 = i + 1
    else:
        last_date0 = time_mod[i]
        i0 = i
    last_date1 = time_obs[len1 - 1]
    i0, i1 = i, len1 - 1
    # If not reached then no last date found
    if last_date0 == time_mod[len0 - 1] and not eq:
        last_date0, last_date1 = None, None
    # Get the right order again
    if reversed is True:
        last_date0, last_date1 = last_date1, last_date0
        i0, i1 = i1, i0
    return last_date0, last_date1, i0, i1


def interpolate_t_frame(frame, timeseries):
    """Time interpolate a dataframe to match a given time series

    Parameters:
    ----------
    * frame : (pandas.Dataframe)
        Original frame with the data to use
    * timeseries : (pandas.Series)
        Series of NaN values with as index the time series to match

    Output:
    ------
    * new : (pandas.DataFrame)
        The time interpolated (linear) dataframe matching the time series
    """
    # Concatenate the two series
    new = pd.concat([frame, timeseries]).sort_index()
    # Interpolate and remove duplicates
    new = new.interpolate(method='values')
    new = new.drop_duplicates()
    # Get only the matching time steps between the two series
    new = new.reindex(timeseries.index)
    return new


def interpolate_t_series(series, time_series):
    """ Interpolate the series to match the time_series

    Parameters:
    ----------
    * series : (pandas.Series)
        The series of values to time interpolate
    * time_series : (pandas.Series)
        Series of NaN values having the wanted time steps as index

    Output:
    ------
    * new : (pandas.Series)
        Time interpolated series matching time_series
    """
    frame = pd.DataFrame(series.values, index=series.index)
    new = interpolate_t_frame(frame, time_series)
    new = pd.Series(new.iloc[:,0], index=new.index)
    return new


# ======= Object management ======


def checkattributes(object, list):
    """Check if an object has all the attributes of a list

    Parameters:
    ----------
    * object : (any object with attributes)
    * list : (list of str)
        ex: ['name', 'values']

    Output:
    ------
    * value : (bool)
        True if has all the attributes, else False
    """
    value = True
    for att in list:
        if not hasattr(object, att):
            print("# No attribute %s" %(att))
            value = False
    return value


def set_zscale(run, zscale):
    """Return the z (grid points) and dz (thickness) lists for a zscale
    zscale = 'mid'
    zscale = 'bound'
    """
    if zscale == 'mid':
        z = run.z
        dz = run.dz
    else:
        z = run.zb
        dz = run.dzb
    return z, dz


def quick_sort(list):
    """Sort the elements of an ESX header (alphabetic and increasing heights)
    Adapted from Quick Sort (C.A.R. Hoare 1960) of a list

    Parameters:
    -----------
    * list : (list of str)
        List of keys from an ESX datafile header
        ex: ['O3:42m'; 'O3:32m', 'NO:0m', 'Temp:']
    """
    if list == []:
        return []
    else:
        t1 = []
        t2 = []
        pivot = list[0]
        for element in list[1:]:
            pname, pheight = get_name_height(pivot)
            ename, eheight = get_name_height(element)
            if eheight is None or pheight is None:
                t2.append(element)
            elif eheight < pheight and pname == ename:
                t1.append(element)
            else:
                t2.append(element)
    return quick_sort(t1) + [pivot] + quick_sort(t2)


def get_datetime(date_array, time_array, format="%Y/%m/%d %H:%M"):
    """Create a datetime array from a date and a time str format arrays used
    by pyesx.run routines - Import esx output files

    Parameters:
    ----------
    * date_array : (numpy.array containing string dates)
    * time_array : (numpy.array containing string hours / time)
    * format : (string - Default = "%Y/%m/%d %H:%M")
        Define the format of the string to convert into datetime arrays

    Output:
    ------
    * (numpy.array of datetime objects)
        Datetime sorted array of the found dates and times
    """
    datetime_list = []
    length = np.size(date_array)
    # Iterate along the dates
    for indice in range(length):
        datetime_string = str(date_array[indice]) + ' ' + \
                              str(time_array[indice])  # Concatenate date time
        # convert datetime_string into datetime object using the datetime mod
        datetime_list.append(datetime.datetime.strptime(
                             datetime_string, format))

    return np.array(datetime_list)


# ======= String management ======
# For ESX foramtting


def quotestr(string):
    """Use to get strings containing '' (quotes) and replace ; by ,

    Parameters:
    ----------
    * string : (str)

    Example:
    -------
    quotestr('Mama;papa,check aa') => "'Mama,papa,check aa'"
    """
    return str("'" + string.replace(';', ',') + "'")


def compute_line_list(list, name=None):
    """Compute the line for esxesx object writting (in pyesx.simulation)

    Parameters:
    ----------
    * list : (list)
        List of values to form the line

    Example:
    -------
    ['O3', 'ppb', '32', '1.0', 'a b', 'T', 'Te']
    >>> 'O3', 'ppb', 32, 1.0, 'a b', T, 'T'
    """
    line = ''
    if name is None:
        name = ''
    # Convert values
    for elmt in list:
        # hard coded exceptions:
        # *********************
        if name.strip() == 'startdate':
            line = line + str(elmt) + ", "  # no need to have '' around date
        elif elmt == 'Te':                  # Hard coded temperature exception
            line = line + quotestr('T') + ", "
        elif elmt == 'T' or elmt == 'F':
            line = line + elmt + ", "       # Boolean values are T and F
        # **********************
        elif is_in('.', str(elmt))[0]:
            try:
                elmt = float(elmt)
                line = line + str(elmt) + ", "  # Line ends by ','
            except ValueError:
                line = line + quotestr(elmt) + ", "
        else:
            try:
                elmt = int(elmt)
                line = line + str(elmt) + ", "  # Line ends by ','
            except ValueError:
                line = line + quotestr(elmt) + ", "
    return line[:-2] + '\n'  # Do not take the last comma


def compute_line(object, list_attr):
    """Compute one line based on the attributes found in the object

    Parameters:
    ----------
    * object : (esxveg object)
        Containing the attribute. ex: esxveg.z0 = 0.5
    * list_attr : (list)
        The attributes to write on one line. ex: ['z0', 'gsto', 'hveg']

    Output:
    ------
    * line : (str)
        One line listing the values of the attributes
    """
    line = ''
    for i in range(len(list_attr)):
        val = list_attr[i]
        if type(val) != 'str':
            val = str(val)
        value = getattr(object, val)
        # Write the value
        if str(value) != value:
            line = line + str(value) + ", "  # Line ends by ','
        elif value == 'T' or value == 'F':
            line = line + value + ", "
        else:
            line = line + quotestr(value) + ", "
    return line + '\n'


def add_height_to_species(spcs, height=None):
    """Add to a string (spcs) a height using the ESX header friendly format
        ex: O3  =>  O3:42m
    """
    if height is None:
        height = ''
    elif type(height) == 'int':
        height = str(height) + 'm'
    return spcs + ':' + height


def filename_strip(filename):
    """Get the information from an ESX formatted filename

    Parameters:
    ----------
    * filename : (str)
        ESX formatted name of a file
        ex: RUNOut__Flux__O3__Turb__nmole_per_m2_per_s.csv

    Output:
    ------
    * prefixe: (str) - The prefixe
    * type : (str) - ex: 'Flux' or 'Conc'
    * spcs : (str) - ex: 'O3'
    * var : (str) - ex: 'Value' or 'CanDep_s'
    * unit : (str) - ex: 'ppb'

    ex: RUNOut__Flux__O3__Turb__nmole_per_m2_per_s.csv
    >>> 'RUNOut' 'Flux' 'O3' 'Turb' 'nmole_per_m2_per_s'
    """
    def findOccurrences(string, character):
        length = len(string)
        return [i for i, letter in enumerate(string[:length-1])
                if letter + string[i+1] == character]
    f = filename
    # find the occurence of '__' in filename
    list = findOccurrences(filename, '__')

    # Prefixe first
    prefixe = f[:list[0]]
    # label then :
    type = f[list[0]+2:list[1]]
    # Flag
    spcs = f[list[1]+2:list[2]]
    # species
    var = f[list[2]+2:list[3]]
    # Units
    unit = f[list[3]+2:len(f)-4]
    return prefixe, type, spcs, var, unit


def get_name_height(string):
    """Separate the name and the height from a given string (ESX header format)

    Parameters:
    ----------
    * string : (str)
        ex: 'O3:42m'

    Output:
    ------
    * name : (str)  >>> 'O3'
    * height : (float)  >>> 42
    """
    check, loc_semicol = is_in(':', string)
    if not check:
        return string, None
    there_is_height = string[-1] == 'm' and check is True

    if there_is_height and loc_semicol + 1 < len(string)-1:
        height = string[loc_semicol + 1: len(string)-1]
        name = string[:loc_semicol]
        return name, float(height)
    else:
        return string[:loc_semicol], None

# ======= Data extraction ======


def plusminus_series(series):
    """Return two lists with the positives and negatives values in series

    Parameters:
    ----------
    * series : (pandas.Series)
        Series of values to separate in two series

    Output:
    ------
    * plus : (pandas.Series)
        Time series with positive values from series
    * minus : (pandas.Series)
        Time series with negative values from series
    """
    plus = np.zeros(len(series))
    minus = np.zeros(len(series))
    for i in range(len(series)):
        if series[i] > 0:
            plus[i] = series[i]
        else:
            minus[i] = series[i]
    return pd.Series(plus, index=series.index), \
            pd.Series(minus, index=series.index)


def hourlygroup(frame, hour):
    """Return a frame with only the data at a given hour of the day (ex: 01am)

    Parameters:
    ----------
    * frame : (pandas.DataFrame or pandas.Series)
    * hour : (int)

    Output:
    ------
    * values : (pandas.DataFrame or pandas.Series)
        Only the values matching the given hour
    """
    return frame.groupby(frame.index.hour).get_group(name=hour)


# ======= Tools ======

def is_higher(number, oneD_array):
    """Give the indice of the first occurence of a float higher or equal than
    number in a sorted array

    Parameters:
    ----------
    * number : (float)
    * oneD_array : (float numpy.array)

    Output:
    ------
    * indice : (int)
       Position of the first float strictly higher than number
    """
    i = 0
    while number >= oneD_array[i]:
        i = i+1
    return i


def is_in(object, group):
    """Check if an object is into a group and may output its position

    Parameters:
    ----------
    * object : (int, float, str)
        The one you are looking for (ex: 'a', 3, 4.2)
    * group : (list, array, str)
        The group you are looking into (ex: 'machine', [3,2], array([2.7,3]))

    Output:
    ------
    * is_in : (bool)
        If the object is in the list or not (True, False)
    * location : (int)
        Position of the object into the group (-1 if object not in group)
    """
    # Functions to find the object into the group

    # Find location in a string
    def is_in_str(object, group):
        loc = group.find(object)
        isin = group.find(object) != -1
        return isin, loc

    # Find location into a list or an array
    def is_in_array(object, group):
        loc = -1
        # Convert list into array to use the numpy library
        if type(group) is list:
            group = np.array(group)
        # If 0 then object is not in the group, thus set isin to False
        isin = np.size(np.where(group == object)) != 0
        if isin is True:
            loc = np.where(group == object)[0][0]
        return isin, loc

    # Return the existency and location of the object in the group
    if type(group) is str:
        isin, loc = is_in_str(object, group)
    else:
        isin, loc = is_in_array(object, group)

    return isin, loc


def datetime2sec(date_time, date_timeR):
    """Converts the time difference between two dates in seconds

    Parameters:
    ----------
    * date_time : (str)
        Date start with format %d-%m-%Y %H:%M:%S
    * date_timeR : (str)
        Date end with format %d-%m-%Y %H:%M:%S

    Output:
    ------
    * dt : (int)
        Delta time in seconds
    """
    ftr = [0, 0, 86400, 3600, 60]

    date_time = date_time.strip()
    date_time = date_time.replace('.', ':')
    date_time = date_time.replace('/', ':')
    date_time = date_time.replace('-', ':')
    date_time = date_time.replace(' ', ':')

    time_obs = np.array(date_time.split(":")).astype('i2')
    time_obs[2] = time_obs[2] + 2000   # Our years !!
    time_obs[2] = sum(jdcal.gcal2jd(time_obs[2], time_obs[1], time_obs[0]))

    date_timeR = date_timeR.strip()
    date_timeR = date_timeR.replace('.', ':')
    date_timeR = date_timeR.replace('/', ':')
    date_timeR = date_timeR.replace(' ', ':')
    time2 = np.array(date_timeR.split(":")).astype('i2')
    time2[2] = time2[2] + 2000
    time2[2] = sum(jdcal.gcal2jd(time2[2], time2[1], time2[0]))

    dt = sum([a*b for a, b in zip(ftr, time2 - time_obs)])
    return dt

# ======= Computation functions ======


def PhotoEquNOxOx(O3, NO, NO2, T, Q):
    """Return the value D giving information about the photo-equilibirum state
    of a given Ox-NOx system under Temperature T and Solar incoming radiation
    Q.

    * Parameters:
      ----------
    - O3 (float)
        Ozone concentration (ppb)
    - NO (float)
        Nitrogen Oxide concentration (ppb)
    - NO2 (float)
        Nitrogen Oxide 2 concentration (ppb)
    - T (float)
        Temperature (Kelvin)
    - Q (float)
        Total incoming radiation (W.m-2)

    * Outputs:
      -------
    - D (float)
        PhotoEq stat

    * Theorie:
      -------
      (https://www.cerc.co.uk/environmental-software/assets/data/doc_techspec/P18_02.pdf)
      ADMS-5 Model (from CERC) NOx chemistry used.

      D = (K1/K2) * [O3]*[NO]/[NO2]
    """

    # Define the constantes:
    k11 = 4.405e-2
    k12 = -1370

    k21 = 8e-4
    k22 = -10
    k23 = 7.4e-6

    # Compute the values:
    K1 = k11 * np.exp(k12/T)
    K2 = k21 * np.exp(k22/Q) + k23 * Q

    D = (K1 / K2) * O3 * NO / NO2
    return D


def NoxEq(NO, NO2, D):
    """ Returns the NO and NO2 concentrations in photoequilibrium according to
    a given state, concerving N quantity.
    """
    alpha = D * NO2 / NO
    NO2eq = alpha * (NO2 + NO) / (1 + alpha)
    NOeq = NO2 + NO - NO2eq
    return NOeq, NO2eq
