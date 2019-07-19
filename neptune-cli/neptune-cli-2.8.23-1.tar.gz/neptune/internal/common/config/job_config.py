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
from future.builtins import object

import ast
import io
import re
import yaml

from neptune.internal.cli.exceptions.job_config_exceptions import (
    InvalidJobConfigException,
    JobConfigFileNotYAMLException,
    NeptuneReadConfigException,
    ParameterYAMLInvalidDefinitionException
)
from neptune.internal.cli.exceptions.params_exceptions import RangeParameterParseException
from neptune.internal.common.config.neptune_config_validator import NeptuneConfigValidator
from neptune.internal.common.models.key_value_properties_utils import properties_from_config_file
from neptune.internal.common.parsers.tracked_parameter_parser import TrackedParameterParser
from neptune.internal.common.parsers.tracked_parameter_regexes import (
    range_regex_part,
    range_brackets_regex_part,
    list_brackets_regex_part
)
from neptune.internal.common.utils.str import to_bytestring
from neptune.internal.common.utils.system import IS_WINDOWS


class ConfigKeys(object):

    # Profile
    PROFILE = 'profile'

    # Project
    PROJECT = 'project'

    # Experiment
    NAME = 'name'
    DESCRIPTION = 'description'
    TAGS = 'tags'
    REQUIREMENTS = 'requirements'  # probably to be deprecated and eventually removed
    PIP_REQUIREMENTS_FILE = 'pip-requirements-file'
    PROPERTIES = 'properties'
    PARAMETERS = 'parameters'
    METRIC = 'metric'

    # Neptune connection
    OPEN_WEBBROWSER = 'open-webbrowser'
    LOG_CHANNELS = 'log-channels'

    EXCLUDE = 'exclude'
    COMMAND = 'command'
    NOTEBOOK_FILE = 'notebook-file'
    POSITIONAL_NOTEBOOK = 'positional_notebook'
    BACKUP = 'backup'

    DISABLE_STDOUT_CHANNEL = 'disable-stdout-channel'
    DISABLE_STDERR_CHANNEL = 'disable-stderr-channel'

    WORKER = "worker"
    ENVIRONMENT = "environment"
    INPUT = "input"

    ML_FRAMEWORK = 'ml-framework'

    DEBUG = 'debug'

    TRACKING = 'tracking'

    NEPTUNE_CONFIG = [
        OPEN_WEBBROWSER
    ]

    EXPERIMENT_CONFIG = [
        NAME,
        DESCRIPTION,
        TAGS,
        REQUIREMENTS,
        PIP_REQUIREMENTS_FILE,
        PROPERTIES,
        EXCLUDE,
        COMMAND,
        PROJECT,
        LOG_CHANNELS,
        ML_FRAMEWORK,
        DISABLE_STDOUT_CHANNEL,
        DISABLE_STDERR_CHANNEL,
        BACKUP,
        NOTEBOOK_FILE,
        POSITIONAL_NOTEBOOK,
        WORKER,
        ENVIRONMENT,
        INPUT
    ]

    BOOLEAN_PARAMETERS = [
        OPEN_WEBBROWSER
    ]


class JobConfig(object):
    def __init__(self, config_path):

        self.path = config_path
        self.neptune_config_validator = NeptuneConfigValidator(self.path)

        try:
            config_path_loc = config_path
            if not IS_WINDOWS:
                config_path_loc = to_bytestring(config_path_loc)

            with io.open(config_path_loc, 'r', encoding='utf-8') as configfile:
                config = yaml.load(configfile.read())

        except yaml.YAMLError:
            raise JobConfigFileNotYAMLException(self.path)
        except IOError as io_error:
            raise NeptuneReadConfigException(io_error)

        if config is None:
            config = dict()

        elif not isinstance(config, dict):
            raise InvalidJobConfigException(
                job_config_path=self.path,
                cause='The structure of the file is incorrect.')

        if ConfigKeys.PROPERTIES not in config:
            config[ConfigKeys.PROPERTIES] = []
        config[ConfigKeys.PROPERTIES] = self._properties_from_config(config_path, config)

        self.neptune_config_validator.validate(
            'neptune_config_schema.yaml', source_data=dict(config))

        parameters = config.get(ConfigKeys.PARAMETERS, {})
        config[ConfigKeys.PARAMETERS] = self._pre_process_params(parameters)

        self._config = dict(config)

    def _pre_process_params(self, raw_params):

        params = {}
        raw_params = raw_params or {}

        for name, param in raw_params.items():

            if not isinstance(param, dict):
                param = {'value' : param}

            if 'value' not in param and 'description' not in param:
                raise ParameterYAMLInvalidDefinitionException(name)

            # Make sure that we have empty dicts instead of None values.
            param = param or {}
            if 'value' in param:
                param_to_string = str(param['value']).replace("'", "\"")
                matched_range_brackets = re.match(r'^' + range_brackets_regex_part() + r'$', param_to_string)
                matched_list_brackets = re.match(r'^' + list_brackets_regex_part(with_api_part=False) + r'$',
                                                 param_to_string)
                if matched_range_brackets and not param_to_string.startswith("\""):
                    matched_range = re.match(r'^' + range_regex_part() + r'$', param_to_string)
                    if not matched_range:
                        raise RangeParameterParseException(name)
                    param['repr'] = str(param['value'])
                    param['value'] = param_to_string
                elif matched_list_brackets and isinstance(param['value'], list):
                    array = ast.literal_eval(matched_list_brackets.group('value'))
                    array = [u'' + TrackedParameterParser.process_quotable_parameter_field(str(a)) for a in array]
                    param['repr'] = str(param['value'])
                    param['value'] = array
                else:
                    if re.search(r'\s', str(param['value'])) and not str(param['value']).startswith("\""):
                        param['repr'] = '\"' + str(param['value']) + '\"'
                    else:
                        param['repr'] = str(param['value'])
                    self._check_parameter_default_value(param_to_string)
                    param['value'] = param_to_string

            params[name] = param

        return params

    def _check_parameter_default_value(self, value):
        if isinstance(value, dict):
            self.neptune_config_validator.validate('param_gridable_default.yaml', source_data=value)
        else:
            self.neptune_config_validator.validate('param_simple_default.yaml', source_data=value)

    @staticmethod
    def _properties_from_config(config_path, config):
        raw_properties = config.get(ConfigKeys.PROPERTIES)
        try:
            return properties_from_config_file(raw_properties)
        except KeyError:
            raise InvalidJobConfigException(
                job_config_path=config_path,
                cause="Section `properties` has invalid structure. "
                      "Each property should consist of fields: 'key', 'value'.")

    def get(self, obj, objtype=None):
        return self._config.get(obj, objtype)

    def get_config(self):
        return self._config

    def __getitem__(self, item):
        return self._config.__getitem__(item)

    def __str__(self):
        return self._config.__str__()

    def __contains__(self, item):
        return self._config.__contains__(item)
