#
# Copyright (c) 2016, deepsense.io
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from future.builtins import str, int
from future.utils import iteritems

import datetime


from dateutil.parser import parse  # pylint:disable=import-error, no-name-in-module

from neptune.generated.swagger_client import ExperimentStates
from neptune.internal.common.utils.memory_units import human_readable
from neptune.internal.common.utils.str import to_unicode


def extract_to_unicode(key, container, _):
    if key not in container:
        return ''
    value = container[key]
    return to_unicode(value) if value is not None else ''


def extract_to_datetime(key, container, _):
    if key not in container:
        return ''
    value = container[key]
    if isinstance(value, datetime.date):
        return format_datetime_with_minute_accuracy(value)
    elif isinstance(value, str):
        return format_datetime_with_minute_accuracy(parse(value))
    else:
        return ""


def format_datetime_with_minute_accuracy(value):
    return value.strftime("%Y-%m-%d %H:%M")


def format_bytes(key, container, _):
    if key not in container:
        return "-"
    value = container[key]
    if isinstance(value, int) or isinstance(value, int):
        return human_readable(value)
    else:
        return "-"


def format_time(key, container, _):
    if key not in container:
        return "-"
    value = container[key]
    if isinstance(value, int) or isinstance(value, int):
        return str(value) + ' s'
    else:
        return "-"


def format_channels(key, container, _):
    if key not in container:
        return ''
    channels = container[key]
    channels_lines = [channel['name'] + "(" + channel['channel_type'] + ")" for channel in channels]
    return " ".join(sorted(channels_lines, key=str.lower))


def format_parameters(key, container, _):
    if key not in container:
        return ''
    parameters = container[key]
    name_value_pairs = []
    for param in parameters:
        if param['value'] is not None:
            name_value_pairs.append(param['name'] + "=" + param['value'])
    return " ".join(
        sorted([param_dict for param_dict in name_value_pairs], key=str.lower))


def format_properties(key, container, _):
    if key not in container:
        return ''
    properties = container[key]
    props = [prop['key'] + ":" + prop['value'] for prop in properties]
    return " ".join(sorted(props, key=str.lower))


def format_tags(key, container, _):
    if key not in container:
        return ''
    tags = container[key]
    return " ".join(sorted(tags, key=str.lower))


def format_state(key, container, _):
    if key not in container:
        return ''
    return container[key]


def format_grid_search_params(key, container, _):
    if key not in container:
        return ''
    grid_search_params = container[key]
    if not grid_search_params:
        return ''

    param_descriptions = []
    for param in grid_search_params:
        param_descriptions.append(format_grid_search_param(param))
    return '\n'.join(sorted(param_descriptions, key=str.lower))


def format_grid_search_param(param):
    ranges_description = format_ranges(param['ranges'])
    arrays_description = format_arrays(param['values'])

    if ranges_description and arrays_description:
        description = '{ranges_description}, {arrays_description}'.format(
            ranges_description=ranges_description, arrays_description=arrays_description)
    else:
        description = ranges_description + arrays_description

    return param['name'] + to_unicode(': ' + description)


def format_ranges(ranges):
    if ranges:
        formatted_ranges = [format_range(range_values) for range_values in ranges]
        return ', '.join(formatted_ranges)
    else:
        return ''


def format_arrays(arrays):
    if arrays:
        sorted_flat_values = sorted(
            [value for array_values in arrays for value in array_values['values']])
        sorted_flat_values_as_strings = [str(value) for value in sorted_flat_values]
        return '[' + ', '.join(sorted_flat_values_as_strings) + ']'
    else:
        return ''


def format_range(range_value):
    return '({}, {}, {})'.format(range_value['from_'], range_value['to'], range_value['step'])



def format_best_experiment(key, container, _):
    if key not in container:
        return ''
    best_experiment = container[key]
    if not best_experiment:
        return ''

    return best_experiment['id']


def format_experiment_states(key, container, _):
    if key not in container:
        return ''

    experiment_states = container[key]

    swagger_experiment_states = ExperimentStates().swagger_types
    # those job states are hidden
    swagger_experiment_states.pop('queued')

    return ' '.join(
        sorted([
            '{state}={count}'.format(
                state=state, count=experiment_states[state]) for state in swagger_experiment_states
        ]))


def format_job_states_from_json(key, container, _):
    if key not in container:
        return ''

    job_states = {}
    for (state, count) in iteritems(container[key]):
        job_states[state] = count
    # those job states are hidden
    job_states.pop('queued')

    return ' '.join([
        '{state}={count}'.format(
            state=state, count=job_states[state]) for state in job_states
    ])


def format_metric(key, container, _):
    if key not in container:
        return ''
    metric = container[key]
    if metric is None:
        return ''

    return '{channel_name} ({direction})'.format(
        direction=metric['direction'], channel_name=metric['channel_name'])


def format_metric_from_json(key, container, _):
    if key not in container:
        return ''

    metric = container[key]

    if metric is None:
        return ''

    return '{channel_name} ({direction})'.format(
        direction=metric['direction'], channel_name=metric['channelName'])
