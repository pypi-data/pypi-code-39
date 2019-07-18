from bqmigratrr.enums.DataType import DataType
from bqmigratrr.enums.Mode import Mode


class Column:
    def __init__(self, name: str, datatype: DataType, mode: Mode):
        self.datatype = datatype
        self.mode = mode
        self.name = name

        # if datatype == DataType.record:
        #     if len(columns) == 0:
        #         raise Exception("Columns must be defined when using record")
        #     self.columns = columns
