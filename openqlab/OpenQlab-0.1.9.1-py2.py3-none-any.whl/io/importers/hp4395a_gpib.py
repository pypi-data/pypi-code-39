from OpenQlab.io.base_importer import BaseImporter
from OpenQlab.io.data_container import DataContainer
import numpy as np
import pandas as pd
import serial


class GPIB:
    def __init__(self, ser, addr):
        self._ser = ser
        self.command('++ver')
        print(self._ser.readline().decode())
        self.command('++addr {0}'.format(addr))
        self.command('++auto 0')
        self.target_id = self.command('*idn?')
        print('Connected to', self.target_id)

    def command(self, cmd, always_read=False):
        self._ser.write(bytes(cmd + '\n', encoding='utf-8'))
        if cmd.endswith('?') or always_read:
            return self.read_answer()
        else:
            return None

    def read_answer(self):
        self.command('++read eoi')
        return self._ser.readline().decode().strip()


class HP4295AGPIB(BaseImporter):
    """ HP4395A GPIB IMPORTER

    This importer is designed to work together with a Prologix
    GPIB-USB interface, which presents itself as a virtual
    serial port.
    """

    NAME = 'HP4295AGPIB'
    AUTOIMPORTER = False
    STARTING_LINES: list = []

    def __init__(self, file):
        self.file = file

    def read(self):
        serial_port, gpib_address = self.file.split('::')
        with serial.Serial(serial_port, 115200, timeout=1) as ser:
            gpib = GPIB(ser, gpib_address)
            x_data = gpib.command('OUTPSWPRM?')
            y_data = gpib.command('OUTPDTRC?')
            y_unit = gpib.command('FMT?')
            if y_unit == 'LOGM':
                y_unit = 'Magnitude (dB)'
            elif y_unit == 'LINM':
                y_unit = 'Linear Magnitude'
            elif y_unit == 'SPECT':
                y_unit = 'Noise Power (dBm)'
            elif y_unit == 'LINY':
                y_unit = 'Linear Units'
            elif y_unit == 'LOGY':
                y_unit == 'Log. Units'
            elif y_unit == 'PHAS':
                phase_unit = gpib.command('PHAU?')
                if phase_unit == 'DEG':
                    y_unit = 'Phase (deg)'
                elif phase_unit == 'RAD':
                    y_unit = 'Phase (rad)'
            else:
                print('Don\'t know how to handle Y unit:', y_unit)

            X = np.fromstring(x_data, sep=',')
            Y = np.fromstring(y_data, sep=',')
            if len(X) == len(Y):
                df = pd.DataFrame(Y, X, columns=[y_unit])
            else:
                df = pd.DataFrame(Y[::2] + 1j * Y[1::2], X, columns=[y_unit])
            df.index.NAME = 'Frequency'
            # add some attributes to the dataframe to store
            # additional information for plotting
            if gpib.command('CHAN1?') == '1':
                df.channel = 1
            else:
                df.channel = 2
            if gpib.command('SWPT?') == 'LOGF':
                df.log_x = True
            else:
                df.log_x = False
            output = DataContainer(df)
            return output
