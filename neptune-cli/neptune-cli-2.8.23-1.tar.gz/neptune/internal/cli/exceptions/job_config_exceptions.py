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
from neptune.internal.common import NeptuneException, NeptuneIOException


class NeptuneReadConfigException(NeptuneIOException):

    def __init__(self, io_error):
        super(NeptuneReadConfigException, self).__init__(io_error)
        self.message += " Failed to load job configuration file."


class ParameterYAMLInvalidDefinitionException(NeptuneException):

    def __init__(self, parameter_name):
        super(ParameterYAMLInvalidDefinitionException, self).__init__(
            u'The provided definition in YAML configuration file for parameter \"{}\" is not supported!'. \
            format(parameter_name))


class ParameterCLIDuplicatedDefinitionException(NeptuneException):

    def __init__(self, parameter_name):
        super(ParameterCLIDuplicatedDefinitionException, self).__init__(
            u'The provided definition in -p/--parameter option for parameter \"{}\" is duplicated!'. \
            format(parameter_name))


class JobConfigFileNotYAMLException(NeptuneException):

    def __init__(self, job_config_path):
        super(JobConfigFileNotYAMLException, self).__init__(
            u'The provided job config file {} is not in YAML format!'.format(job_config_path))


class InvalidJobConfigException(NeptuneException):

    def __init__(self, job_config_path, cause):
        message = u'The provided job configuration {} is invalid! {}'.format(job_config_path, cause)
        super(InvalidJobConfigException, self).__init__(message)


class MetricNotDeclaredException(NeptuneException):

    def __init__(self, param_name):
        cause = u"Parameter '{param_name}' is declared using hyper-parameter notation but "\
                u"no metric is declared in the experiment configuration file."\
            .format(param_name=param_name)
        super(MetricNotDeclaredException, self).__init__(cause)


class NoReferenceParameterException(NeptuneException):
    def __init__(self, param_name):
        cause = u"Parameter '{param_name}' must reference to existing parameter definition"\
            .format(param_name=param_name)
        super(NoReferenceParameterException, self).__init__(cause)
        self.param_name = param_name


class NoReferenceParameterInException(NeptuneException):
    def __init__(self, param_name, arg, message=None):
        cause = u"Parameter '{param_name}' in '{arg}' must reference to existing parameter definition.\n"\
                u"{message}"\
            .format(param_name=param_name, arg=arg, message=message or "")
        super(NoReferenceParameterInException, self).__init__(cause)


class NoValueSetException(NeptuneException):
    def __init__(self, param_name):
        cause = u"Parameter '{param_name}' doesn't have a value".format(param_name=param_name)
        super(NoValueSetException, self).__init__(cause)


class JobConfigValidationFailException(InvalidJobConfigException):

    def __init__(self, job_config_path, validation_errors):
        enumerated_validation_errors = [
            u'{}. {}\n'.format(index + 1, validation_error)
            for index, validation_error in enumerate(validation_errors)
        ]
        cause = 'Validation errors: ' + ', '.join(enumerated_validation_errors)
        super(JobConfigValidationFailException, self).__init__(job_config_path, cause)
