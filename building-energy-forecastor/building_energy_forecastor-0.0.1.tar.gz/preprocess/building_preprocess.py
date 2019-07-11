import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'


# def read_data(filename):
#     data = pd.read_csv(filename)
#
#
# def test_set(test_df):
#     return test_df.drop('Value'), test_df['Value']


# Gives a serie of week days given a serie of dates
# Input: a pd.serie of dates ; Output a pd.serie of string in ['Monday', 'Tuesday', ...]
def day_of_week(time_sr):
    # to_datetime() in case the timestamp is not formatted correctly
    time_sr = pd.to_datetime(time_sr)

    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday', 'Saturday']
    t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    week_day_sr = pd.Series()

    for index, value in time_sr.iteritems():
        year, month, day = value.year, value.month, value.day
        week_day_sr.loc[index] = days[(year + int(year / 4) - int(year / 100) + int(year / 400) + t[month - 1] + day) % 7]

    return week_day_sr


# Turns time into cycles
def cycle_time(df):
    # Convert timestamp into a pandas datatime object
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.set_index('Timestamp')

    # Extract units of time from the timestamp
    df['min'] = df.index.minute
    df['hour'] = df.index.hour
    df['wday'] = df.index.dayofweek
    df['mday'] = df.index.day
    df['yday'] = df.index.dayofyear
    df['month'] = df.index.month
    df['year'] = df.index.year

    # Create a time of day to represent hours and minutes
    df['time'] = df['hour'] + (df['min'] / 60)
    df = df.drop(columns=['hour', 'min'])

    # Cyclical variable transformations

    # wday has period of 6
    df['wday_sin'] = np.sin(2 * np.pi * df['wday'] / 6)
    df['wday_cos'] = np.cos(2 * np.pi * df['wday'] / 6)

    # yday has period of 365
    df['yday_sin'] = np.sin(2 * np.pi * df['yday'] / 365)
    df['yday_cos'] = np.cos(2 * np.pi * df['yday'] / 365)

    # month has period of 12
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)

    # time has period of 24
    df['time_sin'] = np.sin(2 * np.pi * df['time'] / 24)
    df['time_cos'] = np.cos(2 * np.pi * df['time'] / 24)

    # turn the index into a column
    df = df.reset_index(level=0)
    return df


# Function to add weather information into a dataset
# Round timestamp values to the closest quarter/hour/day to match the dataset's ones
def add_weather(df, weather):
    # Keep track of the original length of the dataset
    original_length = len(df)

    # Check the frequency of timestamps in the dataset
    freq_dataset = df.infer_freq('Timestamp')

    # Convert timestamp to a pandas datetime object
    weather['Timestamp'] = pd.to_datetime(weather['Timestamp'])
    weather = weather.set_index('Timestamp')

    # Round the  weather data to the nearest 15 minutes
    weather.index = weather.index.round(freq=freq_dataset)
    weather = weather.reset_index(level=0)

    # Merge the building data with the weather data
    df = pd.merge(df, weather, how='left', on=['Timestamp', 'SiteId'])

    # Drop the duplicate temperature measurements, keeping the closest location
    df = df.sort_values(['Timestamp', 'Distance'])
    df = df.drop_duplicates(['Timestamp', 'SiteId'], keep='first')

    # Checking length of new data
    new_length = len(df)

    # Check to make sure the length of the dataset has not changed
    assert original_length == new_length, 'New Length must match original length'

    return df