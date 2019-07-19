# -*- coding: utf-8 -*-
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

from future.builtins import object, str

from neptune.internal.cli.commands.command_names import CommandNames
from neptune.internal.cli.commands.executing.null_executor import NullExecutor
from neptune.internal.cli.commands.neptune_command import NeptuneCommand
from neptune.internal.cli.commands.utils.docker_utils import resolve_docker_image
from neptune.internal.cli.validation.validations import (
    JobIsInState,
    JobValidationRules,
    ValidationError
)
from neptune.internal.common import NeptuneException
from neptune.internal.common.api.exceptions import NeptuneEntityNotFoundException, NeptuneUnprocessableEntityException
from neptune.internal.common.api.job_api_service import ExperimentState


class GetExperimentError(NeptuneException):
    def __init__(self, message, critical=True):
        super(GetExperimentError, self).__init__(message)
        self.critical = critical


class NeptuneExec(NeptuneCommand):

    def __init__(self, experiment_id, config, api_service, experiment_executor_factory,
                 environment=None, custom_execution_paths=None):

        super(NeptuneExec, self).__init__(CommandNames.EXEC, config, api_service)
        self._experiment_executor_factory = experiment_executor_factory
        self._custom_execution_paths = custom_execution_paths
        self._validations = JobValidationRules(JobIsInState(
            expectedState=ExperimentState.waiting,
            critical=True
        ))
        self.exit_code = self.OK_EXIT_CODE
        self._executor = NullExecutor()
        self.environment = environment
        self.experiment_id = experiment_id

    def abort(self):
        self._executor.abort()

    def _get_experiment(self):
        try:
            return self.api_service.get_experiment(self.experiment_id)
        except NeptuneEntityNotFoundException as exc:
            raise GetExperimentError(exc.response_message)

    def run(self, args):
        try:
            experiment = self._get_experiment()
            self._validations.validate(experiment, args)
            self._execute(experiment, args)

        except NeptuneUnprocessableEntityException as error:
            self.exit_code = self.ENTITY_NOT_FOUND_EXIT_CODE
            self.logger.debug(error)

        except ValidationError as error:
            self.exit_code = self.INVALID_EXPERIMENT_STATE_EXIT_CODE
            print(str(error))

        except GetExperimentError as error:
            self.exit_code = self.NO_EXPERIMENT_TO_EXECUTE
            print(str(error))

        except SystemExit:
            self.exit_code = self.UNKNOWN_EXCEPTION_EXIT_CODE
            raise

        except NeptuneException:
            self.exit_code = self.UNKNOWN_EXCEPTION_EXIT_CODE
            raise

        except BaseException as error:
            self.exit_code = self.UNKNOWN_EXCEPTION_EXIT_CODE
            self.logger.exception(error)

        return self.exit_code

    def _execute(self, experiment, args):

        docker_image = resolve_docker_image(self.environment, self.api_service)
        self._executor = self._experiment_executor_factory.create(
            docker_image=docker_image, experiment=experiment, custom_execution_paths=self._custom_execution_paths)
        self.exit_code = self._executor.execute(experiment, args)


class NeptuneExecFactory(object):
    def __init__(self, config, api_service, experiment_executor_factory):
        self._config = config
        self._api_service = api_service
        self._experiment_executor_factory = experiment_executor_factory

    def create(self, experiment_id, environment=None, custom_execution_paths=None):
        if not experiment_id:
            raise ValueError("experiment_id argument must be provided.")

        return NeptuneExec(experiment_id=experiment_id, config=self._config,
                           api_service=self._api_service, environment=environment,
                           experiment_executor_factory=self._experiment_executor_factory,
                           custom_execution_paths=custom_execution_paths)
