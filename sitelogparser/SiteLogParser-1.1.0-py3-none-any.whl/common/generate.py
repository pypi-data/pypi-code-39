# ------------------------------------------------------------------------------
# Name:        generate.py
# Purpose:
#
# Author:      fredriksson
#
# Created:     10.06.2016
# Copyright:   (c) fredriksson 2016
# ------------------------------------------------------------------------------

import random
import string
import datetime


def generate_id(size=6, chars=string.ascii_uppercase + string.digits):
    """
    Generates an ID of characters with standard size 6

    :param size: size of id
    :param chars: which characters should be uses
    :return:
    :rtype: str
    """
    return ''.join(random.choice(chars) for _ in range(size))


def generate_datetime(string_format="%Y-%m-%dT%H:%M:%S", date=None):
    """

    :param string_format:
    :param date:
    :return:
    :rtype: datetime.datetime
    """
    if date is None:
        return gen_now(string_format, date, date_return=True)
    else:
        return strptime(date)


def generate_datestring(string_format="%Y-%m-%dT%H:%M:%SZ", date=None):
    """

    :param string_format:
    :param date:
    :return:
    :rtype: datetime.datestring
    """
    gen_now(string_format, date, date_return=False)


def strptime(date):
    parts = date.split("T")

    if len(parts) == 1:
        parts = date.split(" ")

    d = parts[0].split("-")
    t = parts[1].replace("Z", "").split(":")

    if len(t) < 3:
        t.append("0")

    for i in range(len(d)):
        d[i] = int(d[i])

    for i in range(len(t)):
        t[i] = int(t[i])

    return datetime.datetime(
        d[0], d[1], d[2],
        t[0], t[1], t[2]
    )


def gen_now(string_format="%Y-%m-%dT%H:%M:%SZ", date=None, date_return=False):
    """
    Liefert ein Datum als Antwort als String im Format 'sf'.
    Bei DATE_RETURN=True wird als Ergebnis ein Typ datetime.datetime als Antwort gegeben.

    :type string_format: str
    :param string_format: date format %Y,%m, ...
    :type date_return: `bool <https://docs.python.org/2/library/functions.html#bool>`_
    :param date_return: if set True return changes from string to datetime.datetime

    :rtype: str, datetime.datetime
    :return: datetime as string or type
    """
    if date is None:
        date = datetime.datetime.now().strftime(string_format)

    if date_return:
        return strptime(date)
    else:
        return date
