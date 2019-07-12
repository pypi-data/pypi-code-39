import os

from time_converter import Converter
import pandas as pd


class Change4LocalTimeConverter(Converter):
    _data = None

    def _load_data(self):
        if self._data is not None:
            return self._data
        else:
            filename = os.path.join(os.path.dirname(__file__), 'change4_localtime.dat')
            data = pd.read_csv(filename, index_col=0, parse_dates=[0, 2])
            data['time'] = pd.Series([val.time() for val in data['time']], index=data.index)
            self._data = data
            return data

    def supports(self, unit=None, datatype=None):
        return (datatype is None or issubclass(datatype, tuple)) and (unit == 'ce4lst')

    def convert_from_datetime(self, datetime):
        data = self._load_data()
        value = pd.Timestamp(datetime)

        if value > data.index.max() or value < data.index.min():
            raise ValueError('unsupported date: {}'.format(datetime))

        row = data.asof(value)
        return row['LD'], row['time']

    def convert_to_datetime(self, value):
        data = self._load_data()

        if value[0] < 1 or value[0] >= data['LD'].max():
            raise ValueError('unsupported lunar day: {}'.format(value[0]))

        masked_data = data[data['LD'] == value[0]][data['time'] >= value[1]]
        if len(masked_data) == 0:
            masked_data = data[data['LD'] > value[0]]
        return pd.Timestamp(masked_data.index.values[0]).to_pydatetime()