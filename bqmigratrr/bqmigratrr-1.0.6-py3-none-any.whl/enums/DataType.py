from enum import Enum


class DataType(Enum):
    string = "STRING"
    timestamp = "TIMESTAMP"
    boolean = "BOOLEAN"
    float = "FLOAT"
    integer = "INTEGER"
    numeric = "NUMERIC"
    date = "DATE"
    time = "TIME"
    datetime = "DATETIME"
    geography = "GEOGRAPHY"
    record = "RECORD"
