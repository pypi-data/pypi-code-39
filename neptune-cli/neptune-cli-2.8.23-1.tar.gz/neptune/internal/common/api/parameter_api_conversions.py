#
# Copyright (c) 2017, deepsense.io
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
import functools
import uuid

from neptune.generated.swagger_client import Parameter, ParameterTypeEnum, GridSearchParameter, RangeValueSet, \
    ArrayValueSet
from neptune.internal.common import is_float
from neptune.internal.common.parsers.tracked_parameter_parser import GridSearchRange, GridSearchArray


def parameters_to_api(tracked_parameters, cli_parameters):
    grid_search_parameters = []
    simple_parameters = []

    for name, value in cli_parameters.items():
        if isinstance(value['value'], GridSearchRange):
            grid_search_parameters.append(_grid_search_range_cli_parameter_to_api(name, value['value'],
                                                                                  None if 'description' not in value
                                                                                  else value['description']))
        elif isinstance(value['value'], GridSearchArray):
            grid_search_parameters.append(_grid_search_array_cli_parameter_to_api(name, value['value'],
                                                                                  None if 'description' not in value
                                                                                  else value['description']))

        else:
            simple_parameters.append(_simple_cli_parameter_to_api(name, value['value'],
                                                                  None if 'description' not in value
                                                                  else value['description']))

    for parameter in tracked_parameters:
        if parameter.display_name() not in cli_parameters.keys():
            if isinstance(parameter.value, GridSearchRange):
                grid_search_parameters.append(_grid_search_range_parameter_to_api(parameter))
            elif isinstance(parameter.value, GridSearchArray):
                grid_search_parameters.append(_grid_search_array_parameter_to_api(parameter))
            else:
                simple_parameters.append(_simple_parameter_to_api(parameter))

    return simple_parameters, grid_search_parameters


def _simple_cli_parameter_to_api(parameter_name, parameter_value, parameter_description=None):
    return Parameter(
        id=str(uuid.uuid4()),
        name=parameter_name,
        description=parameter_description,
        parameter_type=_detect_type_of_parameter(parameter_value),
        value=parameter_value
    )


def _simple_parameter_to_api(simple_parameter):
    return Parameter(
        id=str(uuid.uuid4()),
        name=simple_parameter.display_name(),
        description=None,
        parameter_type=_detect_type_of_parameter(simple_parameter.value),
        value=simple_parameter.value
    )


def _grid_search_range_cli_parameter_to_api(parameter_name, parameter_value, parameter_description=None):
    return GridSearchParameter(
        id=str(uuid.uuid4()),
        name=parameter_name,
        description=parameter_description,
        parameter_type=_detect_type_of_parameter(parameter_value),
        ranges=[RangeValueSet(parameter_value.start, parameter_value.end, parameter_value.step)],
        values=[]
    )


def _grid_search_range_parameter_to_api(grid_search_range_parameter):
    value = grid_search_range_parameter.value
    return GridSearchParameter(
        id=str(uuid.uuid4()),
        name=grid_search_range_parameter.display_name(),
        description=None,
        parameter_type=_detect_type_of_parameter(grid_search_range_parameter.value),
        ranges=[RangeValueSet(value.start, value.end, value.step)],
        values=[]
    )


def _grid_search_array_cli_parameter_to_api(parameter_name, parameter_value, parameter_description=None):

    return GridSearchParameter(
        id=str(uuid.uuid4()),
        name=parameter_name,
        description=parameter_description,
        parameter_type=_detect_type_of_parameter(parameter_value),
        ranges=[],
        values=[ArrayValueSet(parameter_value.values)]
    )


def _grid_search_array_parameter_to_api(grid_search_array_parameter):

    return GridSearchParameter(
        id=str(uuid.uuid4()),
        name=grid_search_array_parameter.display_name(),
        description=None,
        parameter_type=_detect_type_of_parameter(grid_search_array_parameter.value),
        ranges=[],
        values=[ArrayValueSet(grid_search_array_parameter.value.values)]
    )


def _detect_type_of_parameter(param_value):
    if isinstance(param_value, GridSearchRange):
        return ParameterTypeEnum.double
    elif isinstance(param_value, GridSearchArray):
        assert len(param_value.values) > 0
        all_values_numeric = functools.reduce(
            lambda a, b: a and b,
            [
                _detect_parameter_type_of_string(value) == ParameterTypeEnum.double
                for value in param_value.values
            ]
        )
        return ParameterTypeEnum.double if all_values_numeric else ParameterTypeEnum.string
    else:
        return _detect_parameter_type_of_string(param_value)


def _detect_parameter_type_of_string(str_value):
    if is_float(str_value):
        return ParameterTypeEnum.double
    else:
        return ParameterTypeEnum.string
