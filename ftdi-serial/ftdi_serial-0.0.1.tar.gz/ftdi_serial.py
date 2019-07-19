import time
from typing import Any, Union, List, Optional, Callable
from ctypes import c_void_p
import threading
import asyncio
import janus
import queue
import atexit
from ftd2xx import FTD2XX
import ftd2xx


Device2 = ftd2xx.FTD2XX
SerialDeviceType = Union[str, int, ftd2xx.FTD2XX]
NumberType = Union[float, int]
DeviceWriteHandler = Callable[[int, 'Device'], None]


class SerialException(Exception):
    pass


class SerialTimeoutException(SerialException):
    pass


class SerialReadTimeoutException(SerialTimeoutException):
    pass


class SerialWriteTimeoutException(SerialTimeoutException):
    pass


class SerialDeviceInfo:
    def __init__(self,
                 index: Optional[int]=None,
                 flags: Optional[int]=None,
                 type: Optional[int]=None,
                 id: Optional[int]=None,
                 location: Optional[int]=None,
                 serial: Union[bytes, str]='',
                 description: Optional[Union[bytes, str]]=None,
                 handle: Optional[c_void_p]=None,
                 virtual: bool = False,) -> None:
        self.index = index
        self.flags = flags
        self.type = type
        self.id = id
        self.location = location
        self.handle = handle
        self.serial = serial.decode() if isinstance(serial, bytes) else serial
        self.description = description.decode() if isinstance(description, bytes) else description
        self.virtual = virtual


class Device:
    def __init__(self):
        self.write_handlers: List[DeviceWriteHandler] = []
        self.read_timeout = 1.0
        self.write_timeout = 1.0

    def add_write_handler(self, handler: DeviceWriteHandler):
        self.write_handlers.append(handler)

    def close(self):
        pass

    def clear(self):
        pass

    def purge(self):
        self.clear()

    def reset(self):
        self.clear()

    def set_baud_rate(self, baudrate: int):
        pass

    def set_timeouts(self, read_timeout: float, write_timeout: float):
        self.read_timeout = read_timeout / 1000
        self.write_timeout = write_timeout / 1000

    def get_input_size(self) -> int:
        return 0

    def get_output_size(self) -> int:
        return 0

    def write(self, data: bytes):
        for handler in self.write_handlers:
            handler(data, self)

    def read(self, num_bytes: int, raw: bool=True) -> bytes:
        return bytes()

    def read_all(self) -> bytes:
        return self.read(self.get_input_size())

    def enable_write_log(self, enable: bool=True):
        self.write_log_enable = enable

    def get_write_log(self):
        return self.write_log

    def clear_write_log(self):
        self.write_log = bytes()


class FtdiDevice(Device):
    def __init__(self, ftdi: FTD2XX):
        Device.__init__(self)
        self.ftdi = ftdi

    def close(self):
        self.ftdi.close()

    def clear(self):
        self.ftdi.purge()

    def reset(self):
        self.ftdi.resetDevice()
        self.ftdi.resetPort()

    def set_baud_rate(self, baudrate: int):
        self.ftdi.setBaudRate(baudrate)

    def set_timeouts(self, read_timeout: float, write_timeout: float):
        self.ftdi.setTimeouts(read_timeout, write_timeout)

    def get_input_size(self) -> int:
        return self.ftdi.getStatus()[0]

    def get_output_size(self) -> int:
        return self.ftdi.getStatus()[1]

    def write(self, data: bytes):
        super().write(data)
        self.ftdi.write(data)

    def read(self, num_bytes: int, raw: bool = True) -> bytes:
        return self.ftdi.read(num_bytes, raw)


class Serial:
    # FT_STATUS
    FT_OK = 0

    # FT_Purge
    FT_PURGE_RX = 1
    FT_PURGE_TX = 2

    @staticmethod
    def list_devices() -> List[SerialDeviceInfo]:
        devices = ftd2xx.listDevices()

        if devices is None:
            return []

        num_devices = len(devices)
        return [SerialDeviceInfo(**ftd2xx.getDeviceInfoDetail(i)) for i in range(0, num_devices)]

    def __init__(self,
                 device: Optional[Device]=None,
                 device_serial: Optional[str]=None,
                 device_number: Optional[int]=None,
                 baudrate: int=115200,
                 read_timeout: NumberType=5,
                 write_timeout: NumberType=5,
                 connect_timeout: Optional[NumberType]=30,
                 connect_retry: bool=True,
                 connect_settle_time: NumberType=3,
                 connect: bool=True) -> None:
        self.device = device
        self.device_serial = device_serial
        self.device_number = device_number
        self.baudrate = baudrate
        self.read_timeout_value = read_timeout
        self.write_timeout_value = write_timeout
        self.connect_timeout = connect_timeout
        self.connect_retry = connect_retry
        self.connect_settle_time = connect_settle_time
        self.input_buffer = b''
        self.output_buffer = b''
        self.connected = False

        if connect:
            self.connect()

        atexit.register(self.disconnect)

    def open_device(self):
        if self.device is not None:
            pass
        elif self.device_serial is not None:
            self.device = FtdiDevice(ftd2xx.openEx(self.device_serial.encode()))
            # self.device = ftd2xx.openEx(self.device_serial.encode())
        elif self.device_number is not None:
            self.device = FtdiDevice(ftd2xx.open(self.device_number))
            # self.device = ftd2xx.open(self.device_number)
        else:
            self.device = FtdiDevice(ftd2xx.open())
            # self.device = ftd2xx.open()

    def connect(self):
        if self.connected:
            return

        first = True
        start_time = time.time()
        while first or (self.connect_retry and self.device is None):
            try:
                self.open_device()
                # if we weren't able to connect right way, we'll have to wait for the device to settle
                if not first:
                    # wait for the device to settle down
                    time.sleep(self.connect_settle_time)
                    # purge the read buffer to get rid of any bad data accumulated during connection
                    self.device.clear()
                    self.init_device()
            except ftd2xx.DeviceError:
                time.sleep(0.5)

            connect_time = time.time() - start_time

            if self.device is None and connect_time >= self.connect_timeout:
                raise SerialTimeoutException('Timeout while connecting to device')

            first = False

        #time.sleep(0.5)
        self.init_device()
        self.connected = True

    def disconnect(self):
        if not self.connected:
            return

        self.device.close()
        self.connected = False

    def init_device(self):
        self.device.reset()
        self.device.set_baud_rate(self.baudrate)
        self.update_timeouts()

    def update_timeouts(self):
        self.device.set_timeouts(int(self.read_timeout_value * 1000), int(self.write_timeout_value * 1000))

    @property
    def info(self) -> SerialDeviceInfo:
        if self.device is None or not self.connected:
            raise SerialException('Cannot get device info, device is not connected')

        if isinstance(self.device, FtdiDevice):
            return SerialDeviceInfo(**self.device.ftdi.getDeviceInfo())

        return SerialDeviceInfo()

    @property
    def serial_number(self)-> str:
        if self.device is None or not self.connected:
            raise SerialException('Cannot get device serial, device is not connected')

        return self.info.serial

    @property
    def in_waiting(self) -> int:
        if self.device is None or not self.connected:
            return 0

        return self.device.get_input_size() + len(self.input_buffer)

    @property
    def out_waiting(self) -> int:
        if self.device is None or not self.connected:
            return 0

        return self.device.get_output_size()

    @property
    def read_timeout(self):
        return self.read_timeout_value

    @read_timeout.setter
    def read_timeout(self, value):
        self.read_timeout_value = value
        self.update_timeouts()

    @property
    def write_timeout(self):
        return self.write_timeout_value

    @write_timeout.setter
    def write_timeout(self, value):
        self.write_timeout_value = value
        self.update_timeouts()

    def read(self, num_bytes: int=None, timeout: Optional[NumberType]=None) -> bytes:
        if self.device is None or not self.connected:
            raise SerialException('Cannot read, device is not connected')

        if num_bytes is None:
            num_bytes = self.in_waiting

        if num_bytes == 0:
            return b''

        if timeout is not None:
            old_timeout = self.read_timeout
            self.read_timeout = timeout

        serial_data = self.device.read(num_bytes - len(self.input_buffer))

        if timeout is not None:
            self.read_timeout = old_timeout

        if serial_data == b'' and num_bytes != len(self.input_buffer):
            raise SerialReadTimeoutException('Read timeout')

        data = self.input_buffer + serial_data
        self.input_buffer = b''

        return data

    def read_line(self, line_ending: bytes=b'\r', timeout: Optional[NumberType]=None) -> bytes:
        if self.device is None or not self.connected:
            raise SerialException('Cannot read, device is not connected')

        line = b''
        ending_length = len(line_ending)
        while True:
            num_bytes = self.in_waiting
            # always read at least len(line_ending) bytes
            bytes_to_read = num_bytes if num_bytes != 0 else 1
            data = self.read(bytes_to_read, timeout=timeout)
            line += data
            try:
                ending_index = line.index(line_ending)
                [line_data, remaining] = [line[:ending_index], line[ending_index + ending_length:]]
                self.input_buffer += remaining
                return line_data
            except ValueError:
                pass

    def write(self, data: Union[bytes, str], timeout: Optional[NumberType]=None) -> int:
        if self.device is None or not self.connected:
            raise SerialException('Cannot write, device is not connected')

        if isinstance(data, str):
            data = data.encode()

        if timeout is not None:
            old_timeout = self.write_timeout
            self.write_timeout = timeout

        num_bytes = self.device.write(data)

        if timeout is not None:
            self.write_timeout = old_timeout

        return num_bytes

    def request(self, data: bytes, timeout: Optional[NumberType]=None, line_ending: bytes=None):
        self.write(data, timeout=timeout)
        return self.read_line(timeout=timeout, line_ending=line_ending)

    def flush(self):
        self.device.purge()

    def reset_input_buffer(self):
        self.device.purge(self.FT_PURGE_RX)

    def reset_output_buffer(self):
        self.device.purge(self.FT_PURGE_TX)

