import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
import datetime

class DataframeException(Exception):
    pass


def day_of_week(time_sr, time_index='Timestamp'):

    """
    Takes a pandas.Series representing dates,
    Returns a pandas.Series with the corresponding days of the week ('Monday', 'Tuesday', ...).
    The formula comes from https://www.hackerearth.com/blog/developers/how-to-find-the-day-of-a-week/ .

    :param time_sr: pandas.Series
    :return: week_day_sr: pandas.Series
    """

    week_day_sr = time_sr.copy()
    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday']
    t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]

    for index, value in time_sr.iteritems():
        year, month, day = int(value[:4]), int(value[5:7]), int(value[8:10])
        week_day_sr.loc[index] = days[(year + int(year / 4) - int(year / 100) + int(year / 400) + t[month - 1] + day) % 7]

    return week_day_sr


def set_time_index(df, timeindex='Timestamp'):

    """
    Takes a dataframe with dates in one column, and
    Returns a copy with these dates as index in the format datetime from pandas.

    :param df: the pandas.DataFrame containing the dates in one column
    :param timeindex: label of the column containing the dates ; by default equal to 'Timestamp'
    :return: df_indexed: a copy of df with dates as index
    """

    df_indexed = df.copy()
    try:
        df_indexed[timeindex] = pd.to_datetime(df_indexed[timeindex])
        df_indexed = df_indexed.set_index(timeindex)
    except KeyError:
        time_index = input('Enter the time column\'s name:  ')
        df_indexed[time_index] = pd.to_datetime(df_indexed[time_index])
        df_indexed = df_indexed.set_index(time_index)
    return df_indexed


def time_to_cycle(df_input):

    """
    Takes a pandas.DataFrame with timestamps as index in the format datetime from pandas,
    Returns a copy of it with the following new features:
        - day of the year in [1, 365];
        - day of the week in [1, 7];
        - month in [1, 12];
        - sin and cos values of the day of the week, the month, the time of the day.

    :param df_input: pandas.DataFrame with Timestamp as index
    :return: copy of df_input with new features
    """

    df = df_input.copy()
    # Extract units of time from the timestamp
    try:
        df['min'] = df.index.minute
    except AttributeError:
        df = set_time_index(df)
        df['min'] = df.index.minute

    df['hour'] = df.index.hour
    df['wday'] = df.index.dayofweek
    df['yday'] = df.index.dayofyear
    df['month'] = df.index.month

    # Create a time of day to represent hours and minutes
    df['timeofday'] = df['hour'] + (df['min'] / 60)
    df = df.drop(columns=['hour', 'min'])

    # === Transformation of time value into cycles ===

    # wday has period of 6
    df['wday_sin'] = np.sin(2 * np.pi * df['wday'] / 6)
    df['wday_cos'] = np.cos(2 * np.pi * df['wday'] / 6)

    """
    VOIR SI ANNÉE BISSEXTILE CHANGE QQCHOSE
    """

    # yday has period of 365
    df['yday_sin'] = np.sin(2 * np.pi * df['yday'] / 365)
    df['yday_cos'] = np.cos(2 * np.pi * df['yday'] / 365)

    # month has period of 12
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)

    # time has period of 24
    df['time_sin'] = np.sin(2 * np.pi * df['timeofday'] / 24)
    df['time_cos'] = np.cos(2 * np.pi * df['timeofday'] / 24)
    df = df.drop(columns=['timeofday'])

    return df


def add_temperature(df_input, weather_input, timeindex='Timestamp', freq_temp='15 min'):

    """
    Takes a pandas.DataFrame with datetime and temperature as a columns (whatever the name is),
    Returns a copy with re-sampling done with the temperature for each sample (on the day by default).

    IDEE: MOYENNE PONDERE DE LA TEMPERATURE (POUR UN BATIMENT DE BUREAUX 10H EST PLUS INTERESSANT
    QUE MINUIT)

    :param df_input: pandas.DataFrame to which add the temperature
    :param weather_input: pandas.DataFrame containing the temperature values
    :param timeindex: label of the column containing the time
    :param freq_temp: frequency wanted for the data
    :return: new pandas.DataFrame containing df_input data plus the temperature
    """

    df = df_input.copy()
    weather = weather_input.copy()

    if weather.shape[1] > 2:
        raise DataframeException('The DataFrame given to mean_temperature()'
                                 'should only contain timestamps and temperature.\n')

    try:
        # Convert timestamp to a pandas datetime object
        weather[timeindex] = pd.to_datetime(weather[timeindex])
    except KeyError:
        timeindex = input('Enter the time column\'s name:  ')
        weather[timeindex] = pd.to_datetime(weather[timeindex])

    weather = weather.set_index(timeindex)
    weather.index = weather.index.round(freq=freq_temp)
    weather = weather.reset_index(level=0)

    # Merge the building data with the weather data
    df[timeindex] = pd.to_datetime(df[timeindex])
    df = df.merge(weather, how='left', on=[timeindex])

    return df


# def fill_temperature(df_input, tempindex='Temperature'):
#     """
#     Look for NaN values in the tempereature and fill those with the mean of the to closest framing
#     values. Returns a copy of df_input with filled Temperature.
#
#     :param df_input: pandas.DataFrame to fill
#     :param tempindex: label of the column containing the temperature values
#     :return: filled copy of df_input
#     """
#
#     df = df_input.copy()
#     nan_values = df[tempindex].isna()
#
#     for index in range(len(nan_values)):
#
#         if nan_values[index] == np.bool_(True) and index == 0:
#             df.set_value(index, tempindex, int(df.loc[tempindex, index+1].values))
#
#         elif nan_values[index] == np.bool_(True) and index == len(nan_values)-1:
#             df.set_value(index, tempindex, int(df.loc[tempindex, index-1].values))
#
#         elif nan_values[index] == np.bool_(True):
#
#             # Look for the previous closest value
#             i = index
#             while nan_values[i] == np.bool_(True):
#                 i -= 1
#             before_value = int(df.loc[tempindex, i].values)
#
#             # Look for the next closest value
#             i = index
#             while nan_values[i] == np.bool_(True):
#                 i += 1
#             after_value = int(df.loc[tempindex, i].values)
#
#             # Add the new value
#             df.set_value(index, tempindex, str((after_value+before_value)/2))
#
#     return df


def creat_test(freq='D', timeindex='Timestamp'):
    """
    Take the train file and create a test file having the same features but the targeted values.

    :param timeindex:
    :param freq:
    :return: nothing ! Write a test.csv file for prediction
    """

    current_time = datetime.datetime.now().round(freq)
    current_time.day += 1
    time = [current_time]
    for i in range(30):
        current_time.day += 1
        time.append(current_time)
    test = pd.DataFrame({timeindex: current_time})
    test = time_to_cycle(test)
    test = set_time_index(test)
    return test


if __name__ == '__main__':
    weather_main = pd.read_csv('../../../ForecastChallenge/datasets_dir/weather.csv')
    train_main = pd.read_csv('../../../ForecastChallenge/datasets_dir/train.csv')

    weather_main = weather_main[weather_main['SiteId'] == 2]
    train_main = train_main[train_main['ForecastId'] == 38]

    lol = add_temperature(train_main, weather_main[['Timestamp', 'Temperature']], freq_temp='H')[['Timestamp',
                                                                                                  'Temperature']]
    # # print(lol)
    # for index_main, row in lol.iterrows():
    #     if index_main%10 == 0:
    #         lol.set_value(index_main, 'Temperature', 'NaN')
    #
    # # print(lol)
    #
    # lol = fill_temperature(lol)
    #
    # print(lol)

