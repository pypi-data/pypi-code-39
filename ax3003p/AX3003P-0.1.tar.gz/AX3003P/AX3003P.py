"""
AX3003P Programmable Power Supply control library.
"""
# This file is part of AX3003P library.
# Copyright (c) 2019 Krzysztof Adamkiewicz <kadamkiewicz835@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the “Software”), to deal in the
# Software without restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the
# following conditions: THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
# OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from time import sleep, time_ns
import serial

WRITE_COMMAND_DELAY = 0.1 # 100ms - Delay after the write command.
READ_RETRIES_DELAY = 0.03 # 30ms - Delay between read command and waiting for response

def connect(device):
    """ Open connection to the AX3003P.
    Connects to the AX3003P and returns the Power Supply control object.
    over the serial port. Path to the serial port file is given as device.

    :param device: Path to the power supply.
    :type device: Str

    :return: AX300P object.
    :rtype: AX3003P

    :raises SerialException: If there is a problem with the serial port.
    """
    return AX3003P(device)

class AX3003P():
    """ AX3003P Programmable Power Supply control class.

    :param device: Path to the serial port file. example: '/dev/ttyUSB0'
    :type device: Str
    """
    def __init__(self, device):
        self.device = device
        self.connect()

    def connect(self):
        """ Connect to the power supply over the serial interface.
        Connects to the power supply over the serial interface.

        :raises SerialException: If there is a problem with the serial port.
        """
        self.connection = serial.Serial(port=self.device, baudrate=9600, bytesize=serial.EIGHTBITS,
                                        parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                                        timeout=None, xonxoff=False, rtscts=False, write_timeout=100,
                                        dsrdtr=False, inter_byte_timeout=None, exclusive=None)

    def disconnect(self):
        """ Disconnect from the power supply.
        Closes serial connection to the power supply.
        """
        self.connection.close()

    def sendWriteCommand(self, command):
        """ Send command to the power supply.
        Sends command to the power supply.

        :param command: Command
        :type command: Str
        """

        # message must be in a form of a byte array
        message = command + "\n"
        message = str.encode(message)

        self.connection.write(message)
        sleep(WRITE_COMMAND_DELAY)

    def sendReadCommand(self, command, timeout=1000):
        """ Send command and read response.
        Sends command to the power supply and reads the respinse.
        Timeout parameter can be used to determine how long shall te function wait for
        the response. If no response is received before the time runs out the function
        returns None. Otherwise the string containing response is returned.
        If timeout is set to None the function will wait until some data are received.
        This however can cause the program to freeze if no response is received due to
        for example communication error.

        :param command: Command
        :type command: Str
        :param timeout: Timeout in ms
        :type timeout: Int

        :return: Response or None if there is no response.
        :rtype: Str
        """

        # message must be in a form of a byte array
        message = command + "\n"
        message = str.encode(message)

        stopTime = time_ns() + timeout*1000000
        while time_ns() < stopTime:
            self.connection.write(message)
            sleep(READ_RETRIES_DELAY)

            if self.connection.in_waiting > 0:
                received = self.connection.readline()
                received = received.decode('unicode_escape')
                return received[:-1]

        return None

    def setVoltage(self, voltage):
        """ Set output voltage.

        :param voltage: Output voltage in Volts.
        :type voltage: Float
        """
        self.sendWriteCommand("VOLT "+str(voltage))

    def setCurrent(self, current):
        """ Set output current.

        :param current: Output current in Amps.
        :type current: Float
        """
        self.sendWriteCommand("CURR "+str(current))

    def measureVoltage(self):
        """ Measure voltage on the power supply output.
        Function returns the voltage across the power supply terminals
        in Volts. It returns None if the read operation has failed.

        :return: Output voltage.
        :rtype: Float
        """
        return float(self.sendReadCommand("MEAS:VOLT?"))

    def measureCurrent(self):
        """ Measure voltage on the power supply output.
        Function returns the current flowing througth the power supply terminals.
        in Amps. It returns None if the read operation has failed.

        :return: Output current.
        :rtype: Float
        """
        return float(self.sendReadCommand("MEAS:CURR?"))

    def measurePower(self):
        """ Measure power delivered by the power supply output.
        Function returns the current power consumed by the load connected
        to the power supply termonals in Watts.
        It returns None if the read operation has failed.

        :return: Output power.
        :rtype: Float
        """
        return float(self.sendReadCommand("MEAS:POW?"))

    def enableOvp(self):
        """ Enable overvoltage protection.
        """
        self.sendWriteCommand("VOLT:PROT:STAT ON")

    def disableOvp(self):
        """ Disable overvoltage protection.
        """
        self.sendWriteCommand("VOLT:PROT:STAT OFF")

    def enableOcp(self):
        """ Enable overvoltage protection.
        """
        self.sendWriteCommand("CURR:PROT:STAT ON")

    def disableOcp(self):
        """ Disable overvoltage protection.
        """
        self.sendWriteCommand("CURR:PROT:STAT OFF")

    def setOvpTreshold(self, voltageThreshold):
        """ Set overvoltage protection threshold.

        :param voltageThreshold: Voltage treshold in Volts.
        :type voltageThreshold: Float
        """
        self.sendWriteCommand("VOLT:PROT " + str(voltageThreshold))

    def setOcpTreshold(self, currentThreshold):
        """ Set overcurrent protection threshold.

        :param currentThreshold: Current treshold in Amps.
        :type currentThreshold: Float
        """
        self.sendWriteCommand("CURR:PROT " + str(currentThreshold))

    def ovpTripped(self):
        """ Check if overvoltage protection has tripped.
        Returns True if overvoltage protection has tripped.
        Returns False if it hasn't tripped.
        Returns None if error occured while checking the ovp state.

        :return: True if ovp has tripped, False if it is not.
        :rtype: Boolean
        """
        return self.sendReadCommand("VOLT:PROT:TRIP?") == "ON"

    def ocpTripped(self):
        """ Check if overcurrent protection has tripped.
        Returns True if overcurrent protection has tripped.
        Returns False if it hasn't tripped.
        Returns None if error occured while checking the ovp state.

        :return: True if ocp has tripped, False if it is not.
        :rtype: Boolean
        """
        return self.sendReadCommand("CURR:PROT:TRIP?") == "ON"

    def resetOvp(self):
        """ Reset overvoltage protection.
        """
        self.sendWriteCommand("VOLT:PROT:CLE")

    def resetOcp(self):
        """ Reset overcurrent protection.
        """
        self.sendWriteCommand("CURR:PROT:CLE")

    def enableOutput(self):
        """ Enable the power supply output.
        """
        self.sendWriteCommand("OUTP ON")

    def disableOutput(self):
        """ Disable the power supply output.
        """
        self.sendWriteCommand("OUTP OFF")

    def outputEnabled(self):
        """ Check if output is enabled.
        Returns the state of the power supply output.
        If output is enabled, True is Returned, if not, False
        is returned. None is returned if the read operation has failed.

        :return: Power supply state.
        :rtype: Boolean
        """
        return bool(self.sendReadCommand("OUTP?"))
