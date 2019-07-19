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
from __future__ import print_function
from future.builtins import object, str, zip
from future.utils import iteritems, PY3

import ast
import functools
import io
import itertools
import re
import os
import yaml

from past.builtins import basestring

from neptune.generated.swagger_client import (models, KeyValueProperty)
from neptune.internal.cli.exceptions.job_config_exceptions import ParameterCLIDuplicatedDefinitionException
from neptune.internal.cli.exceptions.params_exceptions import (
    CLIParameterParseException,
    RangeParameterParseException
)
from neptune.internal.common.config.connection_info import ConnectionInfo
from neptune.internal.common.config.job_config import ConfigKeys, JobConfig
from neptune.internal.common.config.neptune_config_validator import NeptuneConfigValidator
from neptune.internal.common import NeptuneException
from neptune.internal.common.models.key_value_properties_utils import merge_properties_lists
from neptune.internal.common.parsers.common_parameters_configurator import CommonParametersConfigurator
from neptune.internal.common.parsers.tracked_parameter_parser import (
    GridSearchArray,
    GridSearchRange,
    TrackedParameterParser
)
from neptune.internal.common.parsers.tracked_parameter_regexes import range_regex_part, list_brackets_regex_part, \
    range_brackets_regex_part
from neptune.internal.common.parsers.type_mapper import TypeMapper
from neptune.internal.common.utils.cmdline_arguments_parsing import find_outside_of_quotes
from neptune.internal.common.utils.logging_utils import OnlineNeptuneLogger
from neptune.internal.common.utils.str import to_bytestring
from neptune.internal.common.utils.system import IS_WINDOWS
from neptune.internal.common.values import Tag, LogChannel
from neptune.internal.cli.processes.utils import supports_integration, \
    supports_notebook_integration

DEFAULT_CONFIG_FILENAMES = (u'.neptune.yaml', u'.neptune.yml', u'neptune.yaml', u'neptune.yml')


class ConfigOrigin(object):
    DEFAULT = "default values"
    ENV_VARS = "environment variables"
    CMD_LINE = "command line"


class EmptyConfig(object):

    path = "<config not provided>"

    def get_config(self):
        return {}


def load_local_config(config_filename=None):

    if config_filename is not None:
        config_filepath = os.path.abspath(config_filename)

        if os.path.exists(config_filepath):
            return JobConfig(config_filepath)

        else:
            raise NeptuneException(
                'Config file ({}) does not exist.'.format(config_filename))
    else:

        for config_filename in DEFAULT_CONFIG_FILENAMES:

            config_filepath = os.path.abspath(config_filename)

            if os.path.exists(config_filepath):
                return JobConfig(config_filepath)

        return EmptyConfig()


def global_config_dirpath(profile):
    return os.path.join(os.path.expanduser('~'),
                        CommonParametersConfigurator.NEPTUNE_DIRECTORY,
                        CommonParametersConfigurator.PROFILE_DIRECTORY,
                        profile)


def get_global_config_file(profile):
    for config_filename in DEFAULT_CONFIG_FILENAMES:
        config_filepath = str(os.path.join(global_config_dirpath(profile), config_filename))

        if os.path.exists(config_filepath):
            return config_filepath

    config_path_loc = str(os.path.join(global_config_dirpath(profile), DEFAULT_CONFIG_FILENAMES[0]))
    if not IS_WINDOWS:
        config_path_loc = to_bytestring(config_path_loc)

    return config_path_loc


def load_global_config(profile):
    config_filepath = get_global_config_file(profile)
    if os.path.exists(config_filepath):
        return JobConfig(config_filepath)

    try:
        with io.open(config_filepath, 'w', encoding='utf-8') as configfile:
            configfile.write(u"project: sandbox")
        return load_global_config(profile)
    except IOError:
        pass

    return EmptyConfig()


class _DeprecatedConfigKey(object):
    DEPRECATED_KEY_WARNING = u"Warning: '{deprecated}' config key is deprecated, use '{current}' instead."
    IGNORED_KEY_WARNING_WITH_CURRENT_OPTION = u"Warning: '{deprecated}' config key is ignored, use '{current}' instead."
    IGNORED_KEY_WARNING = u"Warning: '{deprecated}' config key is ignored. It is not valid config key anymore."

    CMD_LINE_ORIGIN_MESSAGE = u"Check your command line arguments."
    ENV_VARS_ORIGIN_MESSAGE = u"Check your environment variables."
    CONFIG_FILE_ORIGIN_MESSAGE = u"Check your config file: '{}'."

    def __init__(self, deprecated_key_name, warning_message, current_key_name=None):
        self.deprecated_key_name = deprecated_key_name
        self._current_key_name = current_key_name
        self._warning_message = warning_message

    def get_warning(self, origin):
        warning_msg = self._warning_message.format(deprecated=self.deprecated_key_name, current=self._current_key_name)
        return (warning_msg + u' ' + self._origin_message(origin)).strip()

    def _origin_message(self, origin):
        if origin == ConfigOrigin.DEFAULT:
            return u''
        elif origin == ConfigOrigin.CMD_LINE:
            return self.CMD_LINE_ORIGIN_MESSAGE
        elif origin == ConfigOrigin.ENV_VARS:
            return self.ENV_VARS_ORIGIN_MESSAGE
        else:
            return self.CONFIG_FILE_ORIGIN_MESSAGE.format(origin)


class NeptuneConfig(object):
    DEFAULT_EXECUTABLES = ['main.py', 'main.R', 'main.jar']

    NO_EXECUTABLE_MESSAGE = (
        u"Executable not found. Provide executable using positional argument or use the default ({})."
    ).format(u', '.join(DEFAULT_EXECUTABLES))
    NO_EXECUTABLE_MESSAGE = NO_EXECUTABLE_MESSAGE if PY3 else NO_EXECUTABLE_MESSAGE.encode('utf-8')

    DEFAULT_NOTEBOOK = ['main.ipynb', 'my.ipynb']
    LIST_MERGED_ARGUMENTS = [
        ConfigKeys.EXCLUDE, ConfigKeys.REQUIREMENTS, ConfigKeys.TAGS,
        ConfigKeys.BACKUP, ConfigKeys.LOG_CHANNELS
    ]
    DEPRECATED_CONFIG_KEYS = [
        _DeprecatedConfigKey(u'project-key', _DeprecatedConfigKey.DEPRECATED_KEY_WARNING, ConfigKeys.PROJECT),
        _DeprecatedConfigKey(u'executable', _DeprecatedConfigKey.IGNORED_KEY_WARNING),
        _DeprecatedConfigKey(u'organization-name', _DeprecatedConfigKey.IGNORED_KEY_WARNING),
        _DeprecatedConfigKey(u'notebook', _DeprecatedConfigKey.IGNORED_KEY_WARNING_WITH_CURRENT_OPTION,
                             ConfigKeys.NOTEBOOK_FILE)
    ]

    @property
    def address(self):
        return self.connection_info.address

    @property
    def http_url(self):
        return self.connection_info.http_url

    @property
    def rest_url(self):
        return self.connection_info.rest_url

    @property
    def ws_url(self):
        return self.connection_info.ws_url

    @property
    def frontend_address(self):
        return self.connection_info.frontend_address

    @property
    def frontend_http_url(self):
        return self.connection_info.frontend_http_url

    @property
    def username(self):
        return self.connection_info.username

    @property
    def auth_code_http_url(self):
        return self.connection_info.auth_code_http_url

    @property
    def metric(self):
        if self._dict_metric:
            return models.Metric(channel_name=self._dict_metric['channel'],
                                 direction=self._dict_metric['goal'])
        return None

    def __init__(self,
                 connection_info=ConnectionInfo(),
                 commandline_args=None,
                 global_config=EmptyConfig(),
                 local_config=EmptyConfig(),
                 cli_parameters=None,
                 show_deprecated_config_keys_warnings=False):

        self.connection_info = connection_info

        if not cli_parameters:
            cli_parameters = []

        self.global_config = global_config
        self.local_config = local_config

        self.configs_paths = {
            'local_path': self.local_config.path,
            'global_path': self.global_config.path
        }
        self.neptune_config_validator = NeptuneConfigValidator(self.configs_paths)

        if commandline_args is not None:
            commandline_config_dict = self._commandline_config_dict(commandline_args.known_args)
        else:
            commandline_config_dict = {}

        if commandline_args is not None and hasattr(commandline_args.known_args, 'entrypoint')\
                and commandline_args.known_args.entrypoint:
            commandline_config_dict[ConfigKeys.COMMAND] = [commandline_args.known_args.entrypoint] + \
                                                 (commandline_args.known_args.cmd_args or [])

        env_config = NeptuneConfig._read_env_config()

        self.config_dict, self.origin_dict = functools.reduce(self._merge_config_and_origin, [
            self._preprocessed_config_with_origin(NeptuneConfig._get_config_defaults(),
                                                  ConfigOrigin.DEFAULT),
            self._preprocessed_config_with_origin(global_config.get_config(), global_config.path),
            self._preprocessed_config_with_origin(local_config.get_config(), local_config.path),
            self._preprocessed_config_with_origin(env_config, ConfigOrigin.ENV_VARS),
            self._preprocessed_config_with_origin(commandline_config_dict, ConfigOrigin.CMD_LINE)
        ])

        self._check_config_schema()

        if show_deprecated_config_keys_warnings:
            self._deprecated_keys_warnings()

        self.organization_name = None
        self.project_name = None

        project = self.get('project') or self.get('project-key')
        if project:
            project_split = project.rsplit('/', 1)
            if len(project_split) == 2:
                self.organization_name = project_split[0]
                self.project_name = project_split[1]
            elif len(project_split) == 1:
                self.organization_name = connection_info.username
                self.project_name = project_split[0]
            else:
                self.organization_name = None
                self.project_name = None

        self.cwd = os.getcwd()

        self.name = self.get('name')
        if self.name is None:
            self.name = os.path.basename(self.cwd)

        self.description = self.get('description', '')

        # We sort tags as soon as possible  and keep it this way.
        # It is important during serialization to JSON.
        self.tags = sorted([Tag.create_from(tag) for tag in self.get('tags', [])])

        self.properties = self.get('properties', [])
        self.requirements = self.get('requirements', [])

        self.open_auth_url = load_bool_env('NEPTUNE_OPEN_AUTH_URL')
        self.manual_login = load_bool_env('NEPTUNE_MANUAL_LOGIN', default=False)

        open_webbrowser = self.get('open-webbrowser')
        self.open_webbrowser = TypeMapper.to_bool(open_webbrowser is None or open_webbrowser)

        self.exclude = self._preprocess_excludes()

        self.executable = self._get_executable()
        self.cmd_args = self._get_cmd_args()

        self.notebook_filename = self._get_notebook()
        self.log_channels = self._preprocess_log_channels()
        self._dict_metric = self.get('metric')
        self.ml_framework = self.get('ml-framework')
        self.backup = set(self.get('backup', []))

        self.tracking = self.get('tracking')
        self.tracking_url = self.get('tracking-url')
        self.parameters = self._preprocess_parameters(cli_parameters)
        self.tracking_app_id = self.get('tracking-app-id')
        self.stdout_channel = not self.get('disable-stdout-channel')
        self.stderr_channel = not self.get('disable-stderr-channel')
        self.pip_requirements_file = self.get('pip-requirements-file')

        self.worker = self.get('worker')
        self.environment = self.get('environment')
        self.input = self._preprocess_input_file_names(self.get('input', []))


    def _preprocess_excludes(self):

        excludes = set(self.get('exclude', []))
        excludes.add(OnlineNeptuneLogger.ONLINE_EXECUTION_LOG_FILENAME)

        return excludes

    def _preprocess_log_channels(self):
        channels = self.config_dict[ConfigKeys.LOG_CHANNELS]
        prefixes = set()
        for prefix, _ in channels:
            prefixes.add(prefix)

        if len(prefixes) != len(channels):
            raise NeptuneException("Log channel prefixes must be unique.")

        return [LogChannel.create(prefix, name) for prefix, name in channels]

    def write(self, config_file_path, keys=None):
        if keys is None:
            keys = ConfigKeys.NEPTUNE_CONFIG
        neptune_config_dict = {
            key: self.config_dict[key]
            for key in keys
            if key in self.config_dict and self.config_dict[key] is not None
        }
        if ConfigKeys.LOG_CHANNELS in self.config_dict:
            neptune_config_dict[ConfigKeys.LOG_CHANNELS] = [a + ":" + b for (a, b) in
                                                            neptune_config_dict[ConfigKeys.LOG_CHANNELS]]
        with open(config_file_path, 'w') as outfile:
            yaml.dump(neptune_config_dict, outfile, default_flow_style=False)

    def _check_config_schema(self):
        self.neptune_config_validator.validate(
            'neptune_config_schema.yaml', source_data=self.config_dict)

    def _is_executable_implicit(self):
        command = self.get(ConfigKeys.COMMAND, None)
        executable_candidate = (command or [None])[0]
        return executable_candidate is None or executable_candidate.startswith(u'-')

    def _get_cmd_args(self):
        command = self.get(ConfigKeys.COMMAND, None)
        if self._is_executable_implicit():
            return command or []
        else:
            return command[1:]

    def _get_executable(self):
        if self._is_executable_implicit():
            return self._get_implicit_executable()
        else:
            return self._get_explicit_executable()

    def _get_implicit_executable(self):
        executable = self._search_for_default_executable()
        if executable is not None:
            return os.path.normpath(executable)
        else:
            return None

    def _get_explicit_executable(self):
        executable = self.get(ConfigKeys.COMMAND)[0]
        if supports_integration(executable):
            if os.path.exists(executable):
                return os.path.normpath(executable)
            else:
                message = u"Executable '{}' does not exist.".format(executable)
                raise NeptuneException(message if PY3 else message.encode('utf-8'))
        else:
            return os.path.normpath(executable)

    @staticmethod
    def _preprocess_input_file_names(input_files):
        for f in input_files:
            if len(f.strip()) == 0:
                raise NeptuneException("Input name cannot be empty.")
        return input_files

    def _get_notebook(self):

        notebook = self.get(ConfigKeys.NOTEBOOK_FILE, None) or \
                     self.get(ConfigKeys.POSITIONAL_NOTEBOOK, None)

        if notebook is not None:
            if supports_notebook_integration(notebook):
                if not os.path.exists(notebook):
                    message = u"Notebook '{}' does not exist.".format(notebook)
                    raise NeptuneException(message if PY3 else message.encode('utf-8'))

                if not os.path.abspath(notebook).startswith(os.path.abspath(os.getcwd())):
                    message = u"Notebook file has to be inside current directory."
                    raise NeptuneException(message if PY3 else message.encode('utf-8'))

                return os.path.normpath(notebook)
            else:
                message = u"Notebook file has to end with .ipynb extension."
                raise NeptuneException(message if PY3 else message.encode('utf-8'))
        else:
            notebook = self._search_for_default_notebook()

            if notebook is not None:
                return os.path.normpath(notebook)
            else:
                return None

    def _preprocess_cli_parameters(self, cli_parameters):
        config_params = self.get(ConfigKeys.PARAMETERS, {})

        cli_parameter_names = []

        for parameter in cli_parameters:
            colon_indices = find_outside_of_quotes(u':', parameter, must_be_preceded_by_whitespace=False)

            parameter_description = None
            parameter_value = None

            if len(colon_indices) == 0:
                raise CLIParameterParseException(parameter)
            elif len(colon_indices) == 1:
                parameter_value = parameter[(colon_indices[0] + 1):]
            elif len(colon_indices) == 2:
                parameter_description = parameter[(colon_indices[1] + 1):]
                if colon_indices[0] + 1 != colon_indices[1]:
                    parameter_value = parameter[(colon_indices[0] + 1):colon_indices[1]]
            else:
                raise CLIParameterParseException(parameter)

            parameter_name = TrackedParameterParser.\
                    process_quotable_parameter_field(parameter[:colon_indices[0]])

            if parameter_name in cli_parameter_names:
                raise ParameterCLIDuplicatedDefinitionException(parameter_name)
            else:
                cli_parameter_names.append(parameter_name)

            parsed_parameter = {}
            if parameter_value:
                matched_list_brackets = re.match(r'^' + list_brackets_regex_part(with_api_part=False) + r'$',
                                                 str(TrackedParameterParser.process_quotable_parameter_field(
                                                     parameter_value)))
                if matched_list_brackets and str(parameter_value).startswith("["):
                    array = ast.literal_eval(parameter_value)
                    parsed_parameter['value'] = array
                else:
                    parsed_parameter['value'] = parameter_value
                parsed_parameter['repr'] = str(parameter_value)
            if parameter_description:
                parsed_parameter['description'] = TrackedParameterParser.\
                    process_quotable_parameter_field(parameter_description)

            if parameter_name in config_params:
                if ('value' not in parsed_parameter or not parsed_parameter['value']) and \
                   ('value' in config_params[parameter_name] and config_params[parameter_name]['value']):
                    parsed_parameter['value'] = config_params[parameter_name]['value']
                    parsed_parameter['repr'] = config_params[parameter_name]['repr']
                if ('description' not in parsed_parameter or not parsed_parameter['description']) and \
                   ('description' in config_params[parameter_name] and config_params[parameter_name]['description']):
                    parsed_parameter['description'] = config_params[parameter_name]['description']

            config_params[parameter_name] = parsed_parameter

        return config_params

    def _preprocess_parameters(self, cli_parameters):

        config_params = self._preprocess_cli_parameters(cli_parameters)

        config_params = config_params or {}

        params = {}

        for name, param in config_params.items():
            if 'value' not in param:
                if not isinstance(param, dict):
                    param['value'] = param
            if 'value' in param:
                processed_string = TrackedParameterParser.process_quotable_parameter_field(str(param['value']))
                matched_range_brackets = re.match(r'^' + range_brackets_regex_part() + r'$', processed_string)
                if matched_range_brackets and not str(param['value']).startswith("\""):
                    matched_range = re.match(r'^' + range_regex_part() + r'$', processed_string)
                    if matched_range:
                        param['value'] = GridSearchRange(
                            start=matched_range.group('from'),
                            end=matched_range.group('to'),
                            step=matched_range.group('step'))
                    else:
                        raise RangeParameterParseException(name)
                elif isinstance(param['value'], list):
                    array = [u'' + TrackedParameterParser.process_quotable_parameter_field(str(a))
                             for a in param['value']]
                    array = GridSearchArray(values=array)
                    param['value'] = array
                else:
                    param['value'] = u'' + processed_string
            if 'description' in param:
                param['description'] = u'' + TrackedParameterParser.\
                    process_quotable_parameter_field(str(param['description']))
            param_name = u'' + TrackedParameterParser.process_quotable_parameter_field(str(name))
            params[param_name] = param

        return params

    @staticmethod
    def _get_config_defaults():
        return {
            'open-webbrowser': True,
            ConfigKeys.PROJECT: None,
            ConfigKeys.LOG_CHANNELS: [],
            ConfigKeys.TRACKING: True,
            ConfigKeys.DISABLE_STDOUT_CHANNEL: False,
            ConfigKeys.DISABLE_STDERR_CHANNEL: False,
        }

    @staticmethod
    def _commandline_config_dict(known_args):

        ALL_KEYS = ConfigKeys.NEPTUNE_CONFIG + ConfigKeys.EXPERIMENT_CONFIG

        cmdline_config = dict()

        for key in ALL_KEYS:
            cmdline_config[key] = getattr(known_args, key, None)

        # We need to convert user supplied string values from argparse to their desired type.
        # We cannot convert those values earlier since boolean flags from known_args
        # are translated to "--x" representation instead of "--x true" and we need to preserve
        # user's input in original format.
        def convert(key, value):
            if value is None:
                return value
            elif key in ConfigKeys.BOOLEAN_PARAMETERS:
                return TypeMapper.to_bool(value)
            else:
                return value

        cmdline_config = {k: convert(k, v) for k, v in cmdline_config.items()}
        cmdline_config[ConfigKeys.PROPERTIES] = NeptuneConfig._to_properties(cmdline_config)

        return cmdline_config

    @staticmethod
    def _read_env_config():
        env_parameters = []

        envs = {param_name: klass(os.environ[env_name])
                for (env_name, param_name, klass) in env_parameters
                if env_name in os.environ}
        return envs

    @classmethod
    def _merge_config_and_origin(cls, parent, child):
        parent_config, parent_origin = parent
        child_config, child_origin = child

        return NeptuneConfig._merge_config(parent_config, child_config), \
            NeptuneConfig._merge_config(parent_origin, child_origin)

    @classmethod
    def _merge_config(cls, parent_config, child_config):
        config = {
            k: v
            for k, v in itertools.chain(iteritems(parent_config), iteritems(child_config))
            if v is not None
        }

        config[ConfigKeys.PROPERTIES] = cls._get_properties(parent_config, child_config)
        for list_prop in cls.LIST_MERGED_ARGUMENTS:
            config[list_prop] = cls._merge_lists(list_prop, parent_config, child_config)
        return config

    @classmethod
    def _preprocessed_config_with_origin(cls, config, name):
        """Converts config to `origin`: pseudo-config with the same structure that has config name
        instead of values. Merging two `origins` should than reflect what was the original location
        of corresponding value in merged two configs, hence the name `origin`."""
        cls._preprocess_config(config)
        origin = {k: name for k, v in iteritems(config) if v is not None}

        origin[ConfigKeys.PROPERTIES] = [
            KeyValueProperty(p.key, name) for p in config.get(ConfigKeys.PROPERTIES, [])
        ]

        for list_prop in cls.LIST_MERGED_ARGUMENTS:
            origin[list_prop] = [name] if config.get(list_prop) else []
        return config, origin

    @classmethod
    def _preprocess_config(cls, config):
        log_channels = []
        for log_channel in config.get(ConfigKeys.LOG_CHANNELS, []) or []:
            log_channels += cls._to_log_channel_pairs(log_channel)
        config[ConfigKeys.LOG_CHANNELS] = log_channels

    def pretty_info(self):
        return self._pretty_info(self.config_dict, self.origin_dict)

    def _pretty_info(self, config, origin):
        fields = [
            self._pretty_info_field(key, config.get(key), origin_value)
            for key, origin_value in iteritems(origin)
        ]
        return '\nUsed settings:\n' + \
               '\n'.join([field_info for field_info in fields if field_info is not None]) + \
               '\nAll other config values are empty.'

    def _pretty_info_field(self, key, config_value, origin_value):
        if key == ConfigKeys.PROPERTIES:
            if not config_value:
                return None
            config_with_origin_value = list(
                zip(sorted(
                    config_value, key=lambda k: k.key),
                    sorted(
                        origin_value, key=lambda k: k.key)))

            return '\n'.join([
                'property {} = "{}" (from {})'.format(prop_origin.key, prop_config.value,
                                                      prop_origin.value)
                for prop_config, prop_origin in config_with_origin_value
            ])
        elif key in self.LIST_MERGED_ARGUMENTS:
            if not config_value:
                return None
            return '{} = {} (from {})'.format(
                key, ', '.join(['"{}"'.format(v) for v in config_value]), ', '.join(origin_value))
        else:
            return '{} = "{}" (from {})'.format(key, config_value, origin_value)

    @staticmethod
    def _merge_collections(key, config, override_config, merging_fun):
        properties_from_config = config.get(key) or []
        properties_from_overrides = override_config.get(key) or []
        merged = merging_fun(properties_from_config, properties_from_overrides)
        return merged

    @staticmethod
    def _get_properties(config, override_config):
        return NeptuneConfig._merge_collections(ConfigKeys.PROPERTIES, config, override_config,
                                                merge_properties_lists)

    @staticmethod
    def _to_properties(override_config):
        properties = override_config.get(ConfigKeys.PROPERTIES) or []
        properties_models = [p.to_swagger_key_value_property() for p in properties]
        return properties_models

    @staticmethod
    def _to_log_channel_pairs(string_or_dict):
        result = []
        if isinstance(string_or_dict, dict):
            for prefix, name in string_or_dict.items():
                result.append((prefix, name))
        elif isinstance(string_or_dict, basestring):
            if string_or_dict.count(u':') == 0:
                result.append((string_or_dict, string_or_dict))
            elif string_or_dict.endswith(u':'):
                result.append((string_or_dict, string_or_dict.rsplit(u':', 1)[0]))
            else:
                prefix, name = string_or_dict.rsplit(u':', 1)
                result.append((prefix, name))
        else:
            raise NeptuneException("Incorrect log channel definition: '{}'".format(string_or_dict))

        for prefix, name in result:
            if len(prefix) == 0:
                raise NeptuneException("Empty string can not be log channel prefix.")
            if len(name) == 0:
                raise NeptuneException("Empty string can not be log channel name.")

        return result

    @staticmethod
    def unique_list_sum(l1, l2):
        return list(set(l1).union(set(l2)))

    @staticmethod
    def _merge_lists(key, config, override_config):
        return NeptuneConfig._merge_collections(key, config, override_config,
                                                NeptuneConfig.unique_list_sum)

    def get(self, obj, objtype=None):
        return self.config_dict.get(obj, objtype)

    def is_default(self, key):
        return key not in self.origin_dict or self.origin_dict[key] == ConfigOrigin.DEFAULT

    def __getitem__(self, item):
        return self.config_dict.__getitem__(item)

    def __str__(self):
        return self.config_dict.__str__()

    def __contains__(self, item):
        return self.config_dict.__contains__(item)

    def _search_for_default_executable(self):
        for exec_name in self.DEFAULT_EXECUTABLES:
            if os.path.isfile(os.path.abspath(exec_name)):
                return exec_name

        return None

    def _search_for_default_notebook(self):
        for notebook_name in self.DEFAULT_NOTEBOOK:
            if os.path.isfile(os.path.abspath(notebook_name)):
                return notebook_name

        return None

    def _deprecated_keys_warnings(self):
        for deprecated_config_key in self.DEPRECATED_CONFIG_KEYS:
            key_name = deprecated_config_key.deprecated_key_name
            if self.get(key_name):
                print(deprecated_config_key.get_warning(self.origin_dict.get(key_name)))


class ConfigSingleton(object):
    _CONFIG = None

    @staticmethod
    def get():
        if ConfigSingleton._CONFIG is None:
            raise ValueError("Config Singleton is empty")

        return ConfigSingleton._CONFIG

    @staticmethod
    def set(config):
        ConfigSingleton._CONFIG = config


def load_bool_env(key, default=True):

    value = os.environ.get(key, default)
    value = value is None or value
    return TypeMapper.to_bool(value is None or value)
