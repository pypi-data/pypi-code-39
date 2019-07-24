import numpy as np
import pandas as pd
from OpenQlab.io.base_importer import StreamImporter
from OpenQlab.io.data_container import DataContainer
from pandas.errors import EmptyDataError
from OpenQlab.io.importers import utils


class Gwinstek(StreamImporter):
    NAME = 'Gwinstek'
    AUTOIMPORTER = True
    STARTING_LINES = [r'^Format,1.0B', r'^(Memory Length,\d*,)*$']
    SAVEMODES = ('Detail', 'Fast')
    HEADER_MAP = {
        'Source': (str, None),
        'Vertical Units': (str, 'yUnit'),
        'Vertical Units Div': (float, None),
        'Vertical Units Extend Div': (float, None),
        'Label': (str, None),
        'Probe Type': (float, None),
        'Probe Ratio': (float, None),
        'Vertical Scale': (float, 'yScale'),
        'Vertical Position': (float, 'yOffset'),
        'Horizontal Units': (str, 'xUnit'),
        'Horizontal Scale': (float, 'xScale'),
        'Horizontal Position': (float, 'xOffset'),
        'SincET Mode': (str, None),
        'Sampling Period': (float, None),
        'Horizontal Old Scale': (float, None),
        'Horizontal Old Position': (float, None),
        'Firmware': (str, None),
        'Mode': (str, None),
    }

    def read(self):
        self._read_header()
        data = self._read_data()
        output = DataContainer(data, type='osci')

        output.update_header(self._header)
        return output

    def _read_header(self):
        split = self._header_lines[1].split(',')
        num_traces = int((len(split)) / 2)
        num_points = int(split[1])
        self._header.update({'NumTraces': num_traces, 'NumPoints': num_points})
        line = True
        while line:
            line = self._stream.readline()
            if line.startswith('Waveform Data'):
                break
            self._read_line(line)

    def _read_data(self):
        xlabel = 'Time'
        try:
            mode = self._header['Mode']
            num_traces = self._header['NumTraces']
            num_points = self._header['NumPoints']
            x_offset = self._header['xOffset']
            start = - self._header['xScale'] * 10 / 2 + x_offset
            stop = self._header['xScale'] * 10 / 2 + x_offset
            if self._header['xUnit'] == 'S':
                self._header['xUnit'] = 's'
        except KeyError:
            raise utils.ImportFailed(
                f"'{self.NAME}' importer: could not gather necessary information in file '{self._stream.name}'")

        ylabel = utils.get_file_basename(self._stream.name)
        ylabels = [f'{ylabel}_{trace_num}' for trace_num in range(1, num_traces + 1)]
        if mode == 'Detail':
            names = [xlabel] + ylabels
            usecols = [0, 1] + list(range(3, 2 * num_traces + 1, 2))
            output = pd.read_csv(self._stream, sep=',', index_col=0, usecols=usecols, prefix=ylabel + '_', header=None)
            output.index.name = xlabel
            output.columns = ylabels
        elif mode == 'Fast':
            names = ylabels
            usecols = list(range(0, 2 * num_traces - 1, 2))
            x = np.linspace(start, stop, endpoint=False, num=num_points)
            output = pd.read_csv(self._stream, sep=',', usecols=usecols,
                                 names=names, header=None, skipinitialspace=True)
            output = output * (self._header['yScale']) / 25
            if output.empty:
                raise EmptyDataError(
                    f"'{self.NAME}' importer: Did not find any valid data in file '{self._stream.name}'")
            output.index = x
            output.index.name = xlabel
        else:
            raise utils.ImportFailed(
                f"'{self.NAME}' importer: expected save modes {self.SAVEMODES} not found in file '{self._stream.name}'")
        return output
