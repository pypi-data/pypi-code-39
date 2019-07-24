import six

import IPython.display

import pandas as pd
import numpy as np

DEFAULT_DATASOURCE_NAME = 'Seeq Data Lab'
DEFAULT_DATASOURCE_CLASS = 'Seeq Data Lab'
DEFAULT_DATASOURCE_ID = 'Seeq Data Lab'
DEFAULT_WORKBOOK_PATH = 'Data Lab >> Data Lab Analysis'
DEFAULT_SEARCH_PAGE_SIZE = 100
DEFAULT_PULL_PAGE_SIZE = 1000000
DEFAULT_PUT_SAMPLES_AND_CAPSULES_BATCH_SIZE = 100000


def present(row, column):
    return (column in row) and \
           (row[column] is not None) and \
           (not isinstance(row[column], float) or not pd.isna(row[column]))


def get(row, column, default=None):
    return row[column] if present(row, column) else default


def get_timings(http_headers):
    output = dict()
    for header, cast in [('Server-Meters', int), ('Server-Timing', float)]:
        server_meters_string = http_headers[header]
        server_meters = server_meters_string.split(',')
        for server_meter_string in server_meters:
            server_meter = server_meter_string.split(';')
            if len(server_meter) < 3:
                continue

            dur_string = cast(server_meter[1].split('=')[1])
            desc_string = server_meter[2].split('=')[1].replace('"', '')

            output[desc_string] = dur_string

    return output


def none_to_nan(v):
    return np.nan if v is None else v


def ensure_unicode(o):
    if isinstance(o, six.binary_type):
        return six.text_type(o, 'utf-8', errors='replace')
    else:
        return o


def ipython_clear_output(wait=False):
    IPython.display.clear_output(wait)


def ipython_display(*objs, include=None, exclude=None, metadata=None, transient=None, display_id=None, **kwargs):
    IPython.display.display(*objs, include=include, exclude=exclude, metadata=metadata, transient=transient,
                            display_id=display_id, **kwargs)
