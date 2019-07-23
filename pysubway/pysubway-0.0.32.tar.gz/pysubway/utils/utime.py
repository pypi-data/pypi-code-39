# -*-coding: utf-8-*-

import time
from datetime import datetime
from typing import Optional
from typing import Union

DEFAULT_FMT = '%Y-%m-%d %H:%M:%S'
NO_BLANK_FMT = '%Y%m%d%H%M%S'


def strftime(obj: Optional[datetime] = None, fmt: str = DEFAULT_FMT) -> str:
    """
    if obj, format obj to string.
    else format now time to string.
    :param obj:
    :param fmt:
    :return:
    """
    if obj and isinstance(obj, datetime):
        return obj.strftime(fmt)
    return time.strftime(fmt)


def timestamp(precision: str = 's', returned_str: bool = False) -> Union[int, str]:
    """

    :param precision: s means seconds, ms means millisecond, others is not support
    :param returned_str: returned type is str or int
    :return:
    """
    origin = time.time()
    may_ms = origin * 1000 if precision == 'ms' else origin
    to_int = int(may_ms)
    return str(to_int) if returned_str else to_int


if __name__ == '__main__':
    s = timestamp(precision='ms', returned_str=True)
    print(s)
