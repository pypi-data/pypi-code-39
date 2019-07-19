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
from neptune.internal.cli.exceptions.job_config_exceptions import MetricNotDeclaredException, NoValueSetException
from neptune.internal.common.parsers.tracked_parameter_parser import (
    is_tracked_parameter_gridable,
    GridSearchArray,
    GridSearchRange
)


def check_if_no_param_is_gridable(tracked_parameters):
    for param in tracked_parameters:
        if is_tracked_parameter_gridable(param):
            raise MetricNotDeclaredException(param.name)


def check_if_no_cli_param_is_gridable(cli_parameters):
    for param, value in cli_parameters.items():
        if 'value' in value:
            if isinstance(value['value'], GridSearchArray) or isinstance(value['value'], GridSearchRange):
                raise MetricNotDeclaredException(param)


def check_if_all_parameters_have_value(parameters):
    for param, value in parameters.items():
        if 'value' not in value:
            raise NoValueSetException(param)
