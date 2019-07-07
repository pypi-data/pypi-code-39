# -*- coding: utf-8 -*-
#
# Copyright (c) 2018~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from abc import ABC, abstractmethod

EXT2FORMAT_MAP = {
    '.json' : 'json',
    '.json5': 'json5',
    '.yaml' : 'yaml',
    '.yml' : 'yaml',
    '.toml' : 'toml',
}

NAME2FORMAT_MAP = {
    'pipfile' : 'pipfile'
}

_REGISTERED_SERIALIZERS = {}

class FormatNotFoundError(Exception):
    pass


class SerializeError(Exception):
    pass


def _detect_format(file_info):
    ext = file_info.path.name.ext.lower()
    if ext in EXT2FORMAT_MAP:
        return EXT2FORMAT_MAP[ext]

    name = file_info.path.name.lower()
    if name in NAME2FORMAT_MAP:
        return NAME2FORMAT_MAP[name]

    raise FormatNotFoundError(f'Cannot detect format from file {file_info!r}')

def load(file_info, format=None, *, kwargs={}):
    if format is None:
        format = _detect_format(file_info)
    serializer = _load_serializer(format)
    try:
        return serializer.load(file_info, kwargs)
    except Exception as err:
        raise SerializeError(err)

def dump(file_info, obj, format=None, *, kwargs={}):
    if format is None:
        format = _detect_format(file_info)
    serializer = _load_serializer(format)
    try:
        return serializer.dump(file_info, obj, kwargs)
    except NotImplementedError:
        raise
    except Exception as err:
        raise SerializeError(err)

def register_format(name):
    '''
    register a serializer for load and dump.
    '''
    def decorator(cls):
        _REGISTERED_SERIALIZERS[name] = cls
        return cls
    return decorator

def _load_serializer(format_):
    if not isinstance(format_, str):
        raise TypeError(f'format must be str.')

    if format_ not in _REGISTERED_SERIALIZERS:
        raise FormatNotFoundError(f'unknown format: {format_}')

    cls = _REGISTERED_SERIALIZERS[format_]
    return cls()


class ISerializer(ABC):
    @abstractmethod
    def load(self, src, kwargs):
        raise NotImplementedError

    @abstractmethod
    def dump(self, src, obj, kwargs):
        raise NotImplementedError


@register_format('json')
class JsonSerializer(ISerializer):
    def load(self, src, kwargs):
        import json
        return json.loads(src.read_text(), **kwargs)

    def dump(self, src, obj, kwargs):
        import json
        return src.write_text(json.dumps(obj, **kwargs), append=False)


@register_format('pickle')
class PickleSerializer(ISerializer):
    def load(self, src, kwargs):
        import pickle
        return pickle.loads(src.read_bytes(), **kwargs)

    def dump(self, src, obj, kwargs):
        import pickle
        return src.write_bytes(pickle.dumps(obj, **kwargs), append=False)


@register_format('json5')
class Json5Serializer(ISerializer):
    def __init__(self):
        try:
            import json5
        except ModuleNotFoundError as err:
            raise ModuleNotFoundError(
                'You need install `json5` before use it.')
        self.json5 = json5

    def load(self, src, kwargs):
        return self.json5.loads(src.read_text(), **kwargs)

    def dump(self, src, obj, kwargs):
        return src.write_text(self.json5.dumps(obj, **kwargs), append=False)


@register_format('toml')
class TomlSerializer(ISerializer):
    def __init__(self):
        try:
            import toml
        except ModuleNotFoundError as err:
            raise ModuleNotFoundError(
                'You need install `toml` before use it.')
        self.toml = toml

    def load(self, src, kwargs):
        return self.toml.loads(src.read_text(), **kwargs)

    def dump(self, src, obj, kwargs):
        return src.write_text(self.toml.dumps(obj, **kwargs), append=False)


@register_format('yaml')
class YamlSerializer(ISerializer):
    def __init__(self):
        try:
            import yaml
        except ModuleNotFoundError as err:
            raise ModuleNotFoundError(
                'You need install `pyyaml` before use it.')
        self.yaml = yaml

    def load(self, src, kwargs):
        return self.yaml.safe_load(src.read_text(), **kwargs)

    def dump(self, src, obj, kwargs):
        return src.write_text(self.yaml.dump(obj, **kwargs), append=False)


@register_format('pipfile')
class PipfileSerializer(ISerializer):
    def __init__(self):
        try:
            import pipfile
        except ModuleNotFoundError as err:
            raise ModuleNotFoundError(
                'You need install `pipfile` before use it.')
        self.pipfile = pipfile

    def load(self, src, kwargs):
        pipfile = self.pipfile.load(src.path)
        return pipfile.data

    def dump(self, src, obj, kwargs):
        raise NotImplementedError('Cannot dump `pipfile`')
