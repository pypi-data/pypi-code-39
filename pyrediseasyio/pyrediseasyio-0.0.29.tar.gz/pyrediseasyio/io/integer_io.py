from pyrediseasyio.io.numeric_io import NumericIO
from pyrediseasyio.io.single_io import SingleIO
from pyrediseasyio.abstract_reader_writer import AbstractReaderWriter


class IntIO(NumericIO):
    def __init__(self, name: str, addr: str = None, default: int=0, **kwargs):
        """
        :param name:    A human readable name to give to the IO
        :param addr:    An optional address (key), if not given, them namespace + member name will be used
        :param default: The value to assign to the IO if no key is found during read
        :param kwargs:
         - units:       str: Optional units to assign to the IO
         - on_value:    str: The 'display_value' property will optionally return this value when the value is True
         - on_value:    str: The 'display_value' property will optionally return this value when the value is False
         - namespace:   str: Optional leading text to apply to the address to makes its key unique
         - min:              The smallest allowable number for the entry, reads and writes will be limited by this.
         - max:              The largest allowable number for the entry, reads and writes will be limited by this.
        """
        super().__init__(name, addr, default, **kwargs)

    @staticmethod
    def _convert_type(value):
        return int(value)



