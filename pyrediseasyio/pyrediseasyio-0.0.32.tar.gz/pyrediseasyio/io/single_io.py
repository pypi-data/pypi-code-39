from pyrediseasyio.abstract_reader_writer import AbstractReaderWriter
import threading
import json

lock = threading.Lock()


class SingleIO:
    def __init__(self, name: str, addr: str = None, default: object = None, **kwargs):
        """
        :param name:    A human readable name to give to the IO
        :param addr:    An optional address (key), if not given, them namespace + member name will be used
        :param default: The value to assign to the IO if no key is found during read
        :param kwargs:
         - units:       str: Optional units to assign to the IO
         - on_value:    str: The 'display_value' property will optionally return this value when the value is True
         - on_value:    str: The 'display_value' property will optionally return this value when the value is False
         - namespace:   str: Optional leading text to apply to the address to makes its key unique
        """
        self.name = name
        self.addr = addr
        self.namespace = kwargs.get('namespace')
        self._reader_writer = None
        self.default = default
        self.units = kwargs.get('units')

    def __and__(self, other):
        if hasattr(other, 'value'):
            return self.value and other.value
        return self.value and other

    def __add__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value + other

    def __sub__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value - other

    def __mul__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value * other

    def __eq__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value == other

    def __floordiv__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value // other

    def __iadd__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        val = self.value
        val += other
        self.write(val)

    def __idiv__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        val = self.value
        val /= other
        self.write(val)

    def __ifloordiv__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        val = self.value
        val //= other
        self.write(val)

    def __imul__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        val = self.value
        val *= other
        self.write(val)

    def __invert__(self):
        return ~self.value

    def __ipow__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        val = self.value
        val **= other
        self.write(val)

    def __isub__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        val = self.value
        val -= other
        self.write(val)

    def __ne__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value != other

    def __or__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value or other

    def __pos__(self):
        return self.value

    def __pow__(self, power, modulo=None):
        if hasattr(power, 'value'):
            power = power.value
        return self.value ** power

    def __neg__(self):
        return -self.value

    def __set__(self, obj, value):
        self.write(value)

    def __str__(self):
        units = '' if self.units is None else self.units
        return f'[{type(self).__name__}] {self.name} = {self.value} {units}'

    def __truediv__(self, other):
        if hasattr(other, 'value'):
            other = other.value
        return self.value / other

    @property
    def display_value(self):
        return self.value

    @property
    def key(self):
        if self.namespace is None:
            return self.addr
        return f'{self.namespace}{self.addr}'

    @property
    def value(self):
        return self.read()

    @staticmethod
    def _convert_type(value):
        return value

    def publish(self, value, channel: str = None, and_write: bool = False):
        value = self._convert_type(value)
        data = json.dumps({self.key: value})
        self._reader_writer.publish(data, channel)
        if and_write:
            self.write(value)

    def read(self):
        if self._reader_writer is None:
            return None
        with lock:
            val = self._reader_writer.read(self.key)
            if val is None:
                val = self.default
            val = self._convert_type(val)
            return val

    def write(self, value):
        if self._reader_writer is None:
            return
        with lock:
            value = self._convert_type(value)
            self._reader_writer.write(self.key, value)


