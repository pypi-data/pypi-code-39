from pyrediseasyio.io.single_io import SingleIO
from str2bool import str2bool
import gettext

_ = gettext.gettext


class BooleanIO(SingleIO):
    def __init__(self, name: str, addr: str = None, default: bool = False, **kwargs):
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
        super().__init__(name, addr, default, **kwargs)
        self.on_value = kwargs.get("on_value", _("On"))
        self.off_value = kwargs.get("off_value", _("Off"))

    @staticmethod
    def _convert_type(value):
        if value is None:
            return False
        if isinstance(value, str):
            return str2bool(value)
        return bool(value)

    def __bool__(self):
        return self.value


    @property
    def display_value(self):
        val = self.value
        dval = self.on_value if val else self.off_value
        return dval

    @property
    def value(self) -> bool:
        return super().value





if __name__ == "__main__":
    io = BooleanIO("Test")
    print(type(io))
    print(BooleanIO)
    print(type(io) == BooleanIO)