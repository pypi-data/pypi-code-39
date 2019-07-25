__version__ = "1.0.0"
__author__ = "Niel Venter"
__copyright__ = "Copyright 2019, Minelert"

from enum import Enum
from threading import Thread
import logging as log
import serial
from minelert_utils.tag import Tag, TagType, INGECOM_MAP


class ReaderType(Enum):
    SERIAL = 10


class Reader(Thread):
    def __init__(self, callback, **kwargs):
        Thread.__init__(self, name="Reader Task")

        self.callback = callback

        self.type = kwargs.get('type', ReaderType.SERIAL)
        self.port = kwargs.get('port', None)
        self.baud = kwargs.get('baud', 115200)
        self.timeout = kwargs.get('timeout', None)
        self.serialPort = None

        self.thread_runner = False

    def connect(self):
        try:
            if self.type == ReaderType.SERIAL:
                self.serialPort = serial.Serial(port=self.port, baudrate=self.baud, timeout=self.timeout)

                if self.serialPort.isOpen():
                    self.serialPort.write('\r\n'.encode())
                    self.thread_runner = True
                    self.start()
                    return True
        except Exception as ex:
            return ex

    def disconnect(self):
        try:
            if self.type == ReaderType.SERIAL:

                if self.serialPort and self.serialPort.isOpen():
                    self.thread_runner = False
                    self.serialPort.close()
                    return True
            return True

        except Exception as ex:
            return ex

    def run(self):
        try:
            while self.thread_runner:
                if self.serialPort and self.serialPort.isOpen():
                    if self.serialPort.in_waiting > 0:
                        data = self.serialPort.readline().decode('Ascii').replace('\r\n', '')

                        if data.startswith('DD'):
                            tag = Tag()

                            data_len = len(data)

                            if data_len == 22:  # example: DD0901000085C83F2E0733
                                tag.tag_id = data[10:18]
                                tag.tag_type = TagType.ML_TRACK.value
                                tag.set_battery_voltage(int(data[18:20], 16))
                                tag.rssi = int(data[20:22], 16)

                            elif data_len == 30:  # example: DD0D0124828C1012C4F3C06292EC33
                                tag.tag_id = '{}{}'.format(INGECOM_MAP.get(data[10:22]), data[22:26])
                                tag.tag_type = TagType.INGECOM.value
                                tag.set_battery_voltage(int('0{}'.format(data[27:28]), 16))
                                tag.rssi = int(data[28:30], 16)


                            print(data, tag)

                            if self.callback:
                                self.callback(tag=tag)
        except Exception as ex:
            self.disconnect()
            return ex
