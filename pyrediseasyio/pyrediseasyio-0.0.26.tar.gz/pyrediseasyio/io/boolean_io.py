from pyrediseasyio.io.single_io import SingleIO
from pyrediseasyio.abstract_reader_writer import AbstractReaderWriter
from str2bool import str2bool


class BooleanIO(SingleIO):
    def __init__(self, name: str, addr: str = None, default: bool = False, units: str = None,
                 reader: AbstractReaderWriter = None, on_value: str = "On", off_value: str = "Off"):
        super().__init__(name, addr, default, units, reader)
        self.on_value = on_value
        self.off_value = off_value

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