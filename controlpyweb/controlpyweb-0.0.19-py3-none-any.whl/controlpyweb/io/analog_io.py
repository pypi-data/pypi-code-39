from controlpyweb.io.single_io import SingleIO
from controlpyweb.io.io_out import IOOut
from controlpyweb.abstract_reader_writer import AbstractReaderWriter


class AnalogIn(SingleIO):
    def __init__(self, name: str, addr: str, default: float = 0.0,
                 reader: AbstractReaderWriter = None, *args, **kwargs):
        super().__init__(name, addr, default, reader, *args, **kwargs)

    @staticmethod
    def _convert_type(value):
        return float(value)


class AnalogOut(IOOut, AnalogIn):
    def __init__(self, name: str, addr: str, default: float = 0.0,
                 reader: AbstractReaderWriter = None, *args, **kwargs):
        super().__init__(name, addr, default, reader, *args, **kwargs)

    @staticmethod
    def _convert_type(value):
        return float(value)