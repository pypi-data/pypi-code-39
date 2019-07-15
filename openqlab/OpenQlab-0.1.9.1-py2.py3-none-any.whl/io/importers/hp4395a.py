from typing import Dict, List
import pandas as pd
import numpy as np
from OpenQlab.io.importers import utils
from OpenQlab.io.base_importer import BaseImporter
from OpenQlab.io.data_container import DataContainer


# TODO implement header

class HP4295A(BaseImporter):
    NAME = 'HP4295A'
    AUTOIMPORTER = True
    STARTING_LINES = [r'^"4395A|^"8751A']

    def read(self):
        points = 0
        channel = 0
        channels: List = []

        line = True
        while line:
            line = self._stream.readline()
            if line.startswith('"NUMBER of POINTS'):
                points = int(line.rstrip('\r\n')[19:-1])
            elif line.startswith('"CHANNEL'):
                channel = int(line.rstrip('\r\n')[10:-1])
            elif line.startswith('"Frequency"'):
                pos = self._stream.tell()  # UGLY: pd.read_table seems to always seek to the
                #       end of the file, so store our approx.
                #       position here.
                channels.append(pd.read_table(self._stream, index_col=0, nrows=points,
                                              names=['Frequency',
                                                     'Ch{0} Data Real'.format(channel),
                                                     'Ch{0} Data Imag'.format(channel),
                                                     'Ch{0} Mem Real'.format(channel),
                                                     'Ch{0} Mem Imag'.format(channel),
                                                     ]))
                self._stream.seek(pos)

        if not channels:
            raise utils.ImportFailed(f'{self.NAME} importer: no data found')
        data = pd.concat(channels, axis=1)
        output = DataContainer(data, type='spectrum')
        return output
