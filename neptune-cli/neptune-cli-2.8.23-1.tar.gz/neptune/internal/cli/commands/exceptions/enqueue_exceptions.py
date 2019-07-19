#
# Copyright (c) 2018, deepsense.io
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
from neptune.internal.common import NeptuneException
from neptune.internal.common.parsers.common_parameters_configurator import CommonParametersConfigurator


class NeptuneInvalidEnvironmentName(NeptuneException):
    def __init__(self, error_msg):
        super(NeptuneInvalidEnvironmentName, self).__init__(
            (u"{error_msg}\n" +
             u"Visit {doc_url} for a " +
             u"list of Neptune's environment types.").format(error_msg=error_msg,
                                                             doc_url=CommonParametersConfigurator
                                                             .DOCS_AVAILABLE_ENVIRONMENTS)
        )


class NeptuneInvalidWorkerType(NeptuneException):
    def __init__(self, error_msg):
        super(NeptuneInvalidWorkerType, self).__init__(
            (u"{error_msg}\n" +
             u"Visit {doc_url} for a " +
             u"list of Neptune's worker types.").format(error_msg=error_msg,
                                                        doc_url=CommonParametersConfigurator.DOCS_AVAILABLE_WORKERS)
        )


class NeptuneInputFileNotFound(NeptuneException):
    def __init__(self):
        super(NeptuneInputFileNotFound, self).__init__(
            u"You cannot use input that is not in Neptune storage.\n" +
            u"Use 'neptune data upload' to upload data to storage."
        )


class NeptuneFailedToExecute(NeptuneException):
    def __init__(self, cmd, source_exception):
        super(NeptuneFailedToExecute, self).__init__(
            u"Failed to start experiment process.\n" +
            u"Command: {}\n".format(" ".join(cmd)) +
            u"Exception: {}".format(str(source_exception))
        )


class NeptunePipInstallFailure(NeptuneException):
    def __init__(self, exit_code):
        super(NeptunePipInstallFailure, self).__init__(
            u"pip failed to install the requirements with exit code=" + str(exit_code) + ".\n" +
            u"For more details, see the output/neptune-stdout.log and output/neptune-stderr.log files."
        )


class NeptuneNoCreditsToRunExperiment(NeptuneException):
    def __init__(self):
        super(NeptuneNoCreditsToRunExperiment, self).__init__(
            u"Sorry, you don't have enough credits in your account to run this experiment.\n" +
            u"Register your credit card in Neptune to run experiments in the cloud."
        )


class NeptuneExperimentCreationUnauthorized(NeptuneException):
    def __init__(self, organization_name, project_name):
        super(NeptuneExperimentCreationUnauthorized, self).__init__(
            u"Failed to create experiment.\n" +
            u"You are not allowed to create experiments in project {}/{}.".format(
                organization_name, project_name
            )
        )
