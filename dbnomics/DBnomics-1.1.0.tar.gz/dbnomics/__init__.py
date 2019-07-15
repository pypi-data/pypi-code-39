# dbnomics-python-client -- Access DBnomics time series from Python
# By: Christophe Benz <christophe.benz@cepremap.org>
#
# Copyright (C) 2017-2018 Cepremap
# https://git.nomics.world/dbnomics/dbnomics-python-client
#
# dbnomics-python-client is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# dbnomics-python-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""Access DBnomics time series from Python."""


import itertools
import json
import logging
import os
import urllib.parse
from urllib.parse import urljoin

import pandas as pd
import requests

default_api_base_url = os.environ.get('API_URL') or 'https://api.db.nomics.world/v22/'
default_max_nb_series = 50

default_editor_api_base_url = os.environ.get('EDITOR_API_URL') or 'https://editor.dbnomics.org/api/v1/'
editor_apply_endpoint_nb_series_per_post = 100

log = logging.getLogger(__name__)


class TooManySeries(Exception):
    def __init__(self, num_found, max_nb_series):
        self.num_found = num_found
        self.max_nb_series = max_nb_series
        message = (
            "DBnomics Web API found {num_found} series matching your request, " +
            (
                "but you passed the argument 'max_nb_series={max_nb_series}'."
                if max_nb_series is not None
                else "but you did not pass any value for the 'max_nb_series' argument, "
                     "so a default value of {default_max_nb_series} was used."
            ) +
            " Please give a higher value (at least max_nb_series={num_found}), and try again."
        ).format(
            default_max_nb_series=default_max_nb_series,
            max_nb_series=max_nb_series,
            num_found=num_found,
        )
        super().__init__(message)


def fetch_series(provider_code=None, dataset_code=None, series_code=None, dimensions=None, series_ids=None,
                 max_nb_series=None, api_base_url=default_api_base_url,
                 editor_api_base_url=default_editor_api_base_url, filters=None):
    """Download time series from DBnomics. Filter series by different ways according to the given parameters.

    If not `None`, `dimensions` parameter must be a `dict` of dimensions (`list` of `str`), like so:
    `{"freq": ["A", "M"], "country": ["FR"]}`.

    If not `None`, `series_code` must be a `str`. It can be a series code (one series), or a "mask" (many series):
    - remove a constraint on a dimension, for example `M..PCPIEC_WT`;
    - enumerate many values for a dimension, separated by a '+', for example `M.FR+DE.PCPIEC_WT`;
    - combine these possibilities many times in the same SDMX filter.

    If the rightmost dimension value code is removed, then the final '.' can be removed too: `A.FR.` = `A.FR`.

    If not `None`, `series_ids` parameter must be a non-empty `list` of series IDs.
    A series ID is a string formatted like `provider_code/dataset_code/series_code`.

    If `max_nb_series` is `None`, a default value of 50 series will be used.

    If `filters` is not `None`, apply those filters using the Time Series Editor API (Cf https://editor.dbnomics.org/filters)

    Return a Python Pandas `DataFrame`.

    Examples:

    - fetch one series:
      fetch_series("AMECO/ZUTN/EA19.1.0.0.0.ZUTN")

    - fetch all the series of a dataset:
      fetch_series("AMECO", "ZUTN")

    - fetch many series from different datasets:
      fetch_series(["AMECO/ZUTN/EA19.1.0.0.0.ZUTN", "AMECO/ZUTN/DNK.1.0.0.0.ZUTN", "IMF/CPI/A.AT.PCPIT_IX"])

    - fetch many series from the same dataset, searching by dimension:
      fetch_series("AMECO", "ZUTN", dimensions={"geo": ["dnk"]})

    - fetch many series from the same dataset, searching by code mask:
      fetch_series("IMF", "CPI", series_code="M.FR+DE.PCPIEC_WT")
      fetch_series("IMF", "CPI", series_code=".FR.PCPIEC_WT")
      fetch_series("IMF", "CPI", series_code="M..PCPIEC_IX+PCPIA_IX")

    - fetch one series and apply interpolation filter:
      fetch_series('AMECO/ZUTN/EA19.1.0.0.0.ZUTN', filters=[{"code": "interpolate", "parameters": {"frequency": "monthly", "method": "spline"}}])
    """
    # Parameters validation
    if not api_base_url.endswith('/'):
        api_base_url += "/"
    if dataset_code is None:
        if isinstance(provider_code, list):
            series_ids = provider_code
            provider_code = None
        elif isinstance(provider_code, str):
            series_ids = [provider_code]
            provider_code = None

    if provider_code is not None and not isinstance(provider_code, str):
        raise ValueError("`provider_code` parameter must be a string")
    if dataset_code is not None and not isinstance(dataset_code, str):
        raise ValueError("`dataset_code` parameter must be a string")
    if dimensions is not None and not isinstance(dimensions, dict):
        raise ValueError("`dimensions` parameter must be a dict")
    if series_code is not None and not isinstance(series_code, str):
        raise ValueError("`series_code` parameter must be a string")
    if series_ids is not None and (
        not isinstance(series_ids, list) or
        any(not isinstance(series_id, str) for series_id in series_ids)
    ):
        raise ValueError("`series_ids` parameter must be a list of strings")
    if api_base_url is not None and not isinstance(api_base_url, str):
        raise ValueError("`api_base_url` parameter must be a string")

    series_base_url = urljoin(api_base_url, 'series')

    if dimensions is None and series_code is None and series_ids is None:
        if not provider_code or not dataset_code:
            raise ValueError("When you don't use `dimensions`, you must specifiy `provider_code` and `dataset_code`.")
        api_link = series_base_url + '/{}/{}?observations=1'.format(provider_code, dataset_code)
        return fetch_series_by_api_link(api_link, filters=filters, max_nb_series=max_nb_series,
                                        editor_api_base_url=editor_api_base_url)

    if dimensions is not None:
        if not provider_code or not dataset_code:
            raise ValueError("When you use `dimensions`, you must specifiy `provider_code` and `dataset_code`.")
        api_link = series_base_url + \
            '/{}/{}?observations=1&dimensions={}'.format(provider_code, dataset_code, json.dumps(dimensions))
        return fetch_series_by_api_link(api_link, filters=filters, max_nb_series=max_nb_series,
                                        editor_api_base_url=editor_api_base_url)

    if series_code is not None:
        if not provider_code or not dataset_code:
            raise ValueError("When you use `series_code`, you must specifiy `provider_code` and `dataset_code`.")
        api_link = series_base_url + '/{}/{}/{}?observations=1'.format(provider_code, dataset_code, series_code)
        return fetch_series_by_api_link(api_link, filters=filters, max_nb_series=max_nb_series,
                                        editor_api_base_url=editor_api_base_url)

    if series_ids is not None:
        if provider_code or dataset_code:
            raise ValueError("When you use `series_ids`, you must not specifiy `provider_code` nor `dataset_code`.")
        api_link = series_base_url + '?observations=1&series_ids={}'.format(','.join(series_ids))
        return fetch_series_by_api_link(api_link, filters=filters, max_nb_series=max_nb_series,
                                        editor_api_base_url=editor_api_base_url)

    raise ValueError("Invalid combination of function arguments")


def fetch_series_by_api_link(api_link, max_nb_series=None,
                             editor_api_base_url=default_editor_api_base_url, filters=None):
    """Fetch series given an "API link" URL.

    "API link" URLs can be found on DBnomics web site (https://db.nomics.world/) on dataset or series pages
    using "Download" buttons.

    If `filters` is not `None`, apply those filters using the Time Series Editor API (Cf https://editor.dbnomics.org/filters)

    Example:
      fetch_series(api_link="https://api.db.nomics.world/v22/series?provider_code=AMECO&dataset_code=ZUTN")
    """
    series_list = list(iter_series(api_link, max_nb_series=max_nb_series))

    if len(series_list) == 0:
        return pd.DataFrame()

    common_columns = ["@frequency", "provider_code", "dataset_code", "dataset_name", "series_code", "series_name",
                      "indexed_at", "original_period", "period", "original_value", "value"]

    normalized_series_list = list(map(normalize_dbnomics_series, series_list))

    if filters:
        common_columns.insert(common_columns.index("period") + 1, "period_middle_day")
        common_columns.append("filtered")
        filtered_series_list = [
            {**series, "filtered": True}
            for series in filter_series(series_list=series_list, filters=filters,
                                        editor_api_base_url=editor_api_base_url)
        ]
        normalized_series_list = [
            {**series, "filtered": False}
            for series in normalized_series_list
        ] + filtered_series_list

    all_columns = set.union(*[set(series.keys()) for series in normalized_series_list])
    dimension_columns = sorted(all_columns - set(common_columns))
    ordered_columns = common_columns + dimension_columns
    dataframes = (
        pd.DataFrame(data=series, columns=ordered_columns)
        for series in normalized_series_list
    )
    return pd.concat(objs=dataframes, sort=False)


def fetch_series_page(series_endpoint_url, offset):
    series_page_url = '{}{}offset={}'.format(
        series_endpoint_url,
        '&' if '?' in series_endpoint_url else '?',
        offset,
    )

    response = requests.get(series_page_url)
    response_json = response.json()
    if not response.ok:
        message = response_json.get('message')
        raise ValueError("Could not fetch data from URL {!r} because: {}".format(series_page_url, message))

    series_page = response_json.get('series')
    if series_page is not None:
        assert series_page['offset'] == offset, (series_page['offset'], offset)

    return response_json


def filter_series(series_list, filters, editor_api_base_url=default_editor_api_base_url):
    if not editor_api_base_url.endswith('/'):
        editor_api_base_url += "/"
    apply_endpoint_url = urljoin(editor_api_base_url, "apply")
    return list(iter_filtered_series(series_list, filters, apply_endpoint_url))


def iter_filtered_series(series_list, filters, apply_endpoint_url):
    for series_group in grouper(editor_apply_endpoint_nb_series_per_post, series_list):
        # Keep only keys required by the editor API.
        posted_series_list = [
            {
                "frequency": series["@frequency"],
                "period_start_day": series["period_start_day"],
                "value": series["value"],
            }
            for series in series_group
        ]
        response = requests.post(apply_endpoint_url, json={"filters": filters, "series": posted_series_list})
        try:
            response_json = response.json()
        except ValueError:
            log.error("Invalid response from Time Series Editor (JSON expected)")
            continue
        if not response.ok:
            log.error("Error with series filters: %s", json.dumps(response_json, indent=2))
            continue

        filter_results = response_json.get("filter_results")
        if not filter_results:
            continue

        for dbnomics_series, filter_result in zip(series_group, filter_results):
            yield normalize_editor_series(series=filter_result["series"], dbnomics_series=dbnomics_series)


def iter_series(api_link, max_nb_series=None):
    total_nb_series = 0

    while True:
        response_json = fetch_series_page(api_link, offset=total_nb_series)

        errors = response_json.get("errors")
        if errors:
            for error in errors:
                log.error("{}: {}".format(error["message"], error))

        series_page = response_json["series"]

        num_found = series_page['num_found']
        if max_nb_series is None and num_found > default_max_nb_series:
            raise TooManySeries(num_found, max_nb_series)

        page_nb_series = len(series_page['docs'])
        total_nb_series += page_nb_series

        # Stop if we have enough series.
        if max_nb_series is not None:
            if total_nb_series == max_nb_series:
                break
            elif total_nb_series > max_nb_series:
                # Do not respond more series than the asked max_nb_series.
                nb_remaining_series = page_nb_series - (total_nb_series - max_nb_series)
                yield from series_page['docs'][:nb_remaining_series]
                break

        yield from series_page['docs']

        # Stop if we downloaded all the series.
        assert total_nb_series <= num_found, (total_nb_series, num_found)  # Can't download more series than num_found.
        if total_nb_series == num_found:
            break


def normalize_dbnomics_series(series):
    """Adapt DBnomics series attributes to ease DataFrame construction."""
    series = normalize_period(series)
    series = normalize_value(series)

    # Flatten dimensions.
    dimensions = series.get("dimensions") or {}
    series = {
        **without_keys(series, keys={"dimensions"}),
        **dimensions,
    }

    # Flatten observations attributes.
    observations_attributes = series.get("observations_attributes") or []
    series = {
        **without_keys(series, keys={"observations_attributes"}),
        **dict(observations_attributes),
    }

    return series


def normalize_editor_series(series, dbnomics_series):
    """Adapt Time Series Editor series attributes to ease DataFrame construction."""
    series = normalize_period(series)
    series = normalize_value(series)
    return {
        **without_keys(series, keys={"frequency"}),
        "@frequency": series["frequency"],
        "provider_code": dbnomics_series["provider_code"],
        "dataset_code": dbnomics_series["dataset_code"],
        "dataset_name": dbnomics_series.get("dataset_name"),
        "series_code": "{}_filtered".format(dbnomics_series["series_code"]),
    }


def normalize_period(series):
    """Keep original period and convert str to datetime. Modifies `series`"""
    period = series.get("period") or []
    period_start_day = series.get("period_start_day") or []
    return {
        **without_keys(series, keys={"period_start_day"}),
        "original_period": period,
        "period": list(map(pd.to_datetime, period_start_day)),
    }


def normalize_value(series):
    """Keep original value and convert "NA" to None (or user specified value). Modifies `series`"""
    value = series.get("value") or []
    return {
        **series,
        "original_value": value,
        "value": [
            # None will be replaced by np.NaN in DataFrame construction.
            None if v == 'NA' else v
            for v in value
        ]
    }

# UTILS


def grouper(n, iterable):
    """From https://stackoverflow.com/a/31185097/3548266

    >>> list(grouper(3, 'ABCDEFG'))
    [['A', 'B', 'C'], ['D', 'E', 'F'], ['G']]
    """
    iterable = iter(iterable)
    return iter(lambda: list(itertools.islice(iterable, n)), [])


def without_keys(d, keys):
    return {k: v for k, v in d.items() if k not in keys}
