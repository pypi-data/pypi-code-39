import numpy as np
import pandas as pd
from src.preprocess import building_preprocess as bp


def test_day_of_week():
    assert bp.day_of_week(pd.Series(np.array(['1997-04-06']))).values == pd.Series(np.array(['Sunday'])).values
    assert bp.day_of_week(pd.Series(np.array(['1991-10-17']))).values == pd.Series(np.array(['Thursday'])).values
    assert bp.day_of_week(pd.Series(np.array(['2019-07-12']))).values == pd.Series(np.array(['Friday'])).values


def test_time_to_cycle():
    input = bp.set_time_index(pd.DataFrame({'Timestamp': ['1997-04-06 00:00:00']}))
    output = bp.set_time_index(pd.DataFrame({'Timestamp': ['1997-04-06 00:00:00'], 'wday': [6], 'yday': [96], 'month': [4],
                           'wday_sin': [-2.449294e-16], 'wday_cos': [1.0],
                           'yday_sin': [0.996659], 'yday_cos': [-0.081676], 'month_sin': [0.866025],
                           'month_cos': [-0.5], 'time_sin': [0], 'time_cos': [1.0]}))
    assert bp.time_to_cycle(input).values.all() == output.values.all()


def test_add_temperature():
    input_df = pd.DataFrame({'Timestamp': ['2019-07-12 00:00:00']})
    input_weather = pd.DataFrame({'Timestamp': ['2019-07-12 00:00:00'], 'Temperature': [20]})
    output = pd.DataFrame({'Timestamp': ['2019-07-12 00:00:00'], 'Temperature': [20]})

    assert bp.add_temperature(input_df, input_weather).values.all() == output.values.all()


def test_fill_temperature():
    pass
