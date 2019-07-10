# -*- coding: utf-8 -*-

import base64
import json
import requests
import xmltodict
import toml
import yaml

try:
    # python 3
    from urllib.parse import quote as url_quote
    from urllib.parse import unquote as url_unquote
except ImportError:
    # python 2
    from urllib import quote as url_quote
    from urllib import unquote as url_unquote


def decode(s, **kwargs):
    try:
        d = decode_base64(s, **kwargs)
    except Exception:
        try:
            d = decode_json(s, **kwargs)
        except Exception:
            try:
                d = decode_query_string(s, **kwargs)
            except Exception:
                try:
                    d = decode_yaml(s, **kwargs)
                except Exception:
                    try:
                        d = decode_toml(s, **kwargs)
                    except Exception:
                        try:
                            d = decode_xml(s, **kwargs)
                        except Exception:
                            d = None
    return d


def decode_base64(s, **kwargs):
    j = base64.b64decode(s, **kwargs)
    return decode_json(j, **kwargs)


def decode_json(s, **kwargs):
    return json.loads(s, **kwargs)


def decode_query_string(s, **kwargs):
    d = {}
    pairs = s.split('&')
    for pair in pairs:
        kv = pair.split('=')
        key = kv[0]
        val = url_unquote(kv[1])
        d[key] = val
    return d


def decode_xml(s, **kwargs):
    return xmltodict.parse(s, **kwargs)


def decode_toml(s, **kwargs):
    return toml.loads(s, **kwargs)


def decode_yaml(s, **kwargs):
    return yaml.load(s, **kwargs)


def encode_base64(d, **kwargs):
    j = encode_json(d, **kwargs)
    return base64.b64encode(j, **kwargs)


def encode_json(d, **kwargs):
    return json.dumps(d, **kwargs)


def encode_query_string(d, **kwargs):
    pairs = []
    for key, val in d.items():
        pair = '='.join(key, url_quote(key))
        pairs.append(pair)
    s = '&'.join(pairs)
    return s


def encode_toml(d, **kwargs):
    return toml.dumps(d, **kwargs)


def encode_xml(d, **kwargs):
    return xmltodict.unparse(d, **kwargs)


def encode_yaml(d, **kwargs):
    return yaml.dump(d, **kwargs)


def read_file(filepath):
    handler = open(filepath, 'r')
    content = handler.read()
    handler.close()
    return content


def read_url(url, *args, **kwargs):
    response = requests.get(url, *args, **kwargs)
    return response.text


def write_file(filepath, content):
    handler = open(filepath, 'w+')
    handler.write(content)
    handler.close()
    return True
