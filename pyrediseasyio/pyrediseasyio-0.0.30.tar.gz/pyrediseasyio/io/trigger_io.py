from pyrediseasyio.io.single_io import SingleIO
from typing import Callable


class TriggerIO(SingleIO):
    """ This IO does not actually write to the Redis server. Its intended use is to allow logic to be applied to its
    set or reset operations. For example, one might want to trigger a clearing of errors, in which case the set
    callback of the trigger would be wired to turning off several other IO"""

    def __init__(self, name: str, write_callback: Callable = None, read_callback: Callable = None,
                 error_callback: Callable = None, default = None, **kwargs):
        """
        :param name: A human readable name to be applied to the trigger
        :param write_callback: A method to call when writing to the trigger; of form - on_write(value) => return None
        :param read_callback: A method to call when reading from the trigger; of form - on_read() => return value
        :param error_callback: A method to call if there was an exception with in write/read callbacks;
                             of form - on_error(ex: Exception) => return substitute
        :param kwargs:
         - units:       str: Optional units to assign to the IO
         - on_value:    str: The 'display_value' property will optionally return this value when the value is True
         - on_value:    str: The 'display_value' property will optionally return this value when the value is False
        """
        super().__init__(name, addr=None, default=default, **kwargs)
        self.write_callback = write_callback
        self.read_callback = read_callback
        self.error_callback = error_callback
        self._iter_index = 0

    def read(self):
        if self.read_callback:
            try:
                return self.read_callback()
            except Exception as ex:
                if self.error_callback:
                    return self.error_callback(ex)
                else:
                    raise
        return self.default

    def write(self, value):
        if self.write_callback:
            try:
                return self.write_callback(value)
            except Exception as ex:
                if self.error_callback:
                    return self.error_callback(ex)
                else:
                    raise
        return None

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

