from pyrediseasyio.io.single_io import SingleIO


class TriggerIO(SingleIO):
    """ This IO does not actually write to the Redis server. Its intended use is to allow logic to be applied to its
    set or reset operations. For example, one might want to trigger a clearing of errors, in which case the set
    callback of the trigger would be wired to turning off several other IO"""

    def __init__(self, name: str, set_callback=None, read_callback=None, default = None, **kwargs):
        """
        :param name: A human readable name to be applied to the trigger
        :param set_callback: A method to call when setting the trigger, takes a single argument - value
        :param read_callback: A method to call when reading the trigger, takes no arguments, and return any object
        :param kwargs:
         - units:       str: Optional units to assign to the IO
         - on_value:    str: The 'display_value' property will optionally return this value when the value is True
         - on_value:    str: The 'display_value' property will optionally return this value when the value is False
        """
        super().__init__(name, addr=None, default=default, **kwargs)
        self.set_callback = set_callback
        self.read_callback = read_callback
        self._iter_index = 0

    def read(self):
        if self.read_callback:
            val = self.read_callback()
            return val
        return None

    def write(self, value):
        if self.set_callback:
            self.set_callback(value)

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        val = self.value
        if self._iter_index >= len(val):
            raise StopIteration
        else:
            self._iter_index += 1
            return val[self._iter_index - 1]

