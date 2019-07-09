from pyrediseasyio.io.single_io import SingleIO


class NumericIO(SingleIO):
    def __init__(self, name: str, addr: str = None, default: float = 0.0, **kwargs):
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

        self.min = kwargs.get('min')
        self.max = kwargs.get('max')


    def read(self):
        val = super().read()
        if val is None:
            return val
        if self.max is not None and val > self.max:
            val = self.max
        if self.min is not None and val < self.min:
            val = self.min
        return val

    def write(self, value):
        if value is None:
            return super().write(self, value)
        value = self._convert_type(value)
        if self.max is not None and value > self._convert_type(self.max):
            value = self.max
        if self.min is not None and value < self._convert_type(self.min):
            value = self.min
        super().write(value)

