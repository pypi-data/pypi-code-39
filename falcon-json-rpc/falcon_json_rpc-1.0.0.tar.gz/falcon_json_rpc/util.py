from datetime import datetime
from typing import Any
import json
from .config import config
from .errors import JsonEncodingError


class JsonDateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


def json_encode(data: Any):
    try:
        return str.encode(json.dumps(data, cls=JsonDateTimeEncoder))
    except Exception as e:
        raise JsonEncodingError(f'JSON encoding failed. {e}')


def update_config(**kwargs):
    for k in kwargs:
        if hasattr(config, k):
            setattr(config, k, kwargs.get(k))





