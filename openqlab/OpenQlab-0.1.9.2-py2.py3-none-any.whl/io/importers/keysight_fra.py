from re import match
import pandas as pd
from OpenQlab.io.importers import utils
from OpenQlab.io.base_importer import StreamImporter
from OpenQlab.io.data_container import DataContainer
import logging as log


class KeysightFRA(StreamImporter):
    NAME = 'KeysightFrequencyResponse'
    AUTOIMPORTER = True
    ENCODING = 'cp1252'
    STARTING_LINES = [r'^\#. Frequency \(Hz\). Amplitude \(Vpp\). Gain \(dB\). Phase']

    def read(self):
        for s in [',', ';']:
            if s in self._header_lines[0]:
                sep = s
        data = pd.read_csv(self._stream, sep=sep, index_col=0, usecols=[1, 2, 3, 4],
                           names=['Frequency (Hz)',
                                  'Amplitude (Vpp)',
                                  'Gain (dB)',
                                  'Phase (deg)'],
                           header=None)
        output = DataContainer(data)

        if output.empty:
            raise utils.ImportFailed(
                f"'{self.NAME}' importer: \
                Did not find any valid data in file '{self._stream.name}'")
        return output
