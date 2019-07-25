from dataclasses import asdict, fields, is_dataclass
from datetime import date, datetime
from typing import Any, Type

from dateutil.parser import parse as date_parser
from flask import json

SERIALIZERS = {
    dict: json.dumps,
    str: str,
    int: str,
    float: str,
    bool: str,
    list: str,
    date: lambda d: d.isoformat(),
    datetime: lambda d: d.isoformat(),
}


def serialize(data: Any) -> str:
    '''Serialize ``data`` into a ``str``'''
    serializer = SERIALIZERS.get(data.__class__)
    if serializer is not None:
        return serializer(data)
    if is_dataclass(data):
        return SERIALIZERS.get(dict, json.dumps)(asdict(data))
    if hasattr(data, '__marshmallow__'):
        return data.__marshmallow__.dumps(data).data
    raise TypeError(f'Cannot serialize type {data.__class__}')


TRUE_STRS = ['true', '1', 't', 'y']
FALSE_STRS = ['false', '0', 'f', 'n']


def str_to_bool(data: str):
    if data.lower() in TRUE_STRS:
        return True
    if data.lower() in FALSE_STRS:
        return False
    raise ValueError(
        f'{data} not in accepted values {TRUE_STRS}, {FALSE_STRS}')


DESERIALIZERS = {
    dict: json.load,
    str: str,
    int: int,
    float: float,
    bool: str_to_bool,
    datetime: date_parser,
    date: lambda d: date_parser(d).date()
}


def deserialize(data: Any, class_: Type) -> Any:
    '''Deserialize a str ``data`` into the given ``data_type``'''
    deserializer = DESERIALIZERS.get(class_)
    if issubclass(class_, list):
        return data
    if isinstance(data, list):
        data = data[0]
    if deserializer is not None:
        return deserializer(data)
    if is_dataclass(class_):
        parsed_data = json.loads(data)
        for field in fields(class_):
            if parsed_data.get(field.name):
                parsed_data[field.name] = deserialize(
                    parsed_data[field.name], field.type)
        return class_(**parsed_data)
    if hasattr(class_, '__marshmallow__'):
        if isinstance(data, str):
            return class_.__marshmallow__.loads(data).data
        else:
            return class_.__marshmallow__.load(data).data
    raise TypeError(f'Cannot deserialize type {class_}')
