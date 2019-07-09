# -*- coding: utf-8 -*-

from benedict.utils import io_util


class IODict(dict):

    def __init__(self, *args, **kwargs):
        # TODO:
        # if first arguemnt is string,
        # try to decode it using all decoders, try try try try :)
        super(IODict, self).__init__(*args, **kwargs)

    @staticmethod
    def _load_from_and_decode(decoder, s=None, filepath=None, url=None, **kwargs):
        if not any([s, filepath, url]):
            raise ValueError('s or filepath or url args should be provided.')
        if bool(s) ^ bool(filepath) ^ bool(url):
            raise ValueError('s, filepath, url args are mutually exclusive.')
        if not s:
            if filepath:
                s = io_util.read_file(filepath)
            elif url:
                s = io_util.read_url(url)
        d = decoder(s, **kwargs)
        return s

    @staticmethod
    def _encode_to_and_save(d, encoder, filepath=None, **kwargs):
        s = encoder(d, **kwargs)
        if filepath:
            io_util.write_file(filepath, s)
        return s

    @staticmethod
    def from_base64(s=None, filepath=None, url=None, **kwargs):
        return IODict._load_from_and_decode(
            io_util.decode_base64, s, filepath, url, **kwargs)

    @staticmethod
    def from_json(s=None, filepath=None, url=None, **kwargs):
        return IODict._load_from_and_decode(
            io_util.decode_json, s, filepath, url, **kwargs)

    @staticmethod
    def from_query_string(s=None, filepath=None, url=None, **kwargs):
        return IODict._load_from_and_decode(
            io_util.decode_query_string, s, filepath, url, **kwargs)

    @staticmethod
    def from_toml(s=None, filepath=None, url=None, **kwargs):
        return IODict._load_from_and_decode(
            io_util.decode_toml, s, filepath, url, **kwargs)

    @staticmethod
    def from_xml(s=None, filepath=None, url=None, **kwargs):
        return IODict._load_from_and_decode(
            io_util.decode_xml, s, filepath, url, **kwargs)

    @staticmethod
    def from_yaml(s=None, filepath=None, url=None, **kwargs):
        return IODict._load_from_and_decode(
            io_util.decode_yaml, s, filepath, url, **kwargs)

    def to_base64(self, filepath=None, **kwargs):
        return IODict._encode_to_and_save(
            self, encoder=io_util.encode_base64, **kwargs)

    def to_json(self, filepath=None, **kwargs):
        return IODict._encode_to_and_save(
            self, encoder=io_util.encode_json, **kwargs)

    def to_query_string(self, filepath=None, **kwargs):
        return IODict._encode_to_and_save(
            self, encoder=io_util.encode_query_string, **kwargs)

    def to_toml(self, filepath=None, **kwargs):
        return IODict._encode_to_and_save(
            self, encoder=io_util.encode_toml, **kwargs)

    def to_xml(self, filepath=None, **kwargs):
        return IODict._encode_to_and_save(
            self, encoder=io_util.encode_xml, **kwargs)

    def to_yaml(self, filepath=None, **kwargs):
        return IODict._encode_to_and_save(
            self, encoder=io_util.encode_yml, **kwargs)
