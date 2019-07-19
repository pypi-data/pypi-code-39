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

from future.builtins import str

class ExecArgsFormatter(object):
    def __init__(self, tracked_parameter_parser):
        self._tracked_parameter_parser = tracked_parameter_parser

    def format_exec_args_for_cmdline(self, exec_args_template_list, api_parameters):
        return self._format_exec_args(exec_args_template_list, api_parameters)

    def _format_exec_args(self, exec_args_template_list, api_parameters):

        parameter_values = self._api_parameters_to_dict(api_parameters)
        formatted_api_values = {}
        for name, value in parameter_values.items():
            formatted_api_values[name] = {'value': value}

        tracked_params = self._tracked_parameter_parser.parse(exec_args_template_list, formatted_api_values)

        if tracked_params:
            tracked_param_index = 0
            result = []
            for arg in exec_args_template_list:
                if len(arg) <= 0 or arg[0] != '%' or len(arg) <= 1 or arg[:2] == '%%':
                    result.append(arg)
                    continue
                tracked_param = tracked_params[tracked_param_index]
                value = str(tracked_param.value)
                result.append(value)
                tracked_param_index += 1
            return result
        else:
            return exec_args_template_list

    @staticmethod
    def _api_parameters_to_dict(api_parameters):
        return {api_param.name: api_param.value for api_param in api_parameters}
