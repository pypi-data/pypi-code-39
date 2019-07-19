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
from __future__ import print_function

import logging
from platform import node as hostname

from future.builtins import object
from past.builtins import basestring

from neptune.generated.swagger_client import ExperimentTemplateParams, GroupCreationParams, Metric
from neptune.internal.cli.commands.exceptions.enqueue_exceptions import NeptuneInputFileNotFound, \
    NeptuneInvalidEnvironmentName, NeptuneInvalidWorkerType, NeptuneNoCreditsToRunExperiment, \
    NeptuneExperimentCreationUnauthorized
from neptune.internal.cli.commands.neptune_command import Entity
from neptune.internal.cli.commands.utils.parameters import check_if_all_parameters_have_value, \
    check_if_no_cli_param_is_gridable, check_if_no_param_is_gridable
from neptune.internal.cli.commands.utils.payments_utils import PaymentsUtils
from neptune.internal.common.api.exceptions import NeptuneBadClientRequest, NeptunePaymentRequiredException, \
    NeptuneValidationException, NeptuneServerResponseErrorException
from neptune.internal.common.api.parameter_api_conversions import parameters_to_api
from neptune.internal.common.models.rich_experiment import RichExperimentCreationParams
from neptune.internal.common.parsers.tracked_parameter_validations import validate_tracked_parameters


class EnqueueUtils(object):
    def __init__(self,
                 config,
                 api_service,
                 web_browser):
        """
        :type config:
        :type api_service: neptune.internal.common.api.job_api_service.JobApiService
        """
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.api_service = api_service
        self.web_browser = web_browser

    @staticmethod
    def is_grid_search(tracked_params, base_params):
        for tracked_param in tracked_params:
            if not isinstance(tracked_param.value, basestring):
                return True
        for param_name in base_params:
            if not isinstance(base_params[param_name]['value'], basestring):
                return True
        return False

    def parse_experiment_arguments(self, experiment_config, tracked_parameter_parser):
        tracked_params = tracked_parameter_parser.parse(
            experiment_config.cmd_args,
            experiment_config.parameters,
            print_warnings=True
        )
        check_if_all_parameters_have_value(experiment_config.parameters)
        tracked_params = validate_tracked_parameters(tracked_params)
        if 'metric' not in self.config:
            check_if_no_param_is_gridable(tracked_params)
            check_if_no_cli_param_is_gridable(experiment_config.parameters)
        return tracked_params

    def create_enqueued_experiment(self, entrypoint, tracked_params, enqueue_command, exec_args_template,
                                   project, remote_params=None):
        self.logger.info("CREATING EXPERIMENT")

        new_params = RichExperimentCreationParams.create(
            experiment_config=self.config,
            enqueue_command=enqueue_command,
            exec_args_template=exec_args_template,
            tracked_parameters=tracked_params,
            entrypoint=entrypoint,
            project_id=project.id,
            remote_params=remote_params,
            hostname=self._get_hostname(is_local=remote_params is None),
            is_notebook=False,
            notebook_source_filename=None,
        )
        experiment = self._call_with_exception_mapping(project, self.api_service.create_experiment, new_params)

        self.logger.info("EXPERIMENT: %s ENQUEUED", experiment.id)
        self.print_creation_confirmation(
            experiment.organization_name,
            experiment.project_name,
            Entity.experiment,
            experiment.short_id
        )
        return experiment

    def create_enqueued_notebook(self, notebook_source_filename, project, remote_params=None):
        self.logger.info("CREATING NOTEBOOK")

        new_params = RichExperimentCreationParams.create(
            experiment_config=self.config,
            enqueue_command=notebook_source_filename,
            exec_args_template=u'',
            tracked_parameters=[],
            entrypoint=notebook_source_filename,
            project_id=project.id,
            remote_params=remote_params,
            hostname=self._get_hostname(is_local=remote_params is None),
            is_notebook=True,
            notebook_source_filename=notebook_source_filename,
        )
        notebook = self._call_with_exception_mapping(project, self.api_service.create_experiment, new_params)

        self.logger.info("NOTEBOOK: %s ENQUEUED", notebook.id)
        self.print_creation_confirmation(
            notebook.organization_name,
            notebook.project_name,
            Entity.notebook,
            notebook.short_id
        )
        return notebook

    def create_enqueued_group(self, entrypoint, tracked_parameters, enqueue_command, exec_args_template,
                              project, remote_params=None):
        self.logger.info("CREATING GROUP")
        api_simple_parameters, api_grid_search_params = parameters_to_api(
            tracked_parameters,
            self.config.parameters
        )

        new_params = GroupCreationParams(
            project_id=project.id,
            name=self.config.name,
            description=self.config.description,
            tags=self.config.tags,
            grid_search_parameters=api_grid_search_params,
            metric=Metric(
                self.config.metric.channel_name,
                self.config.metric.direction
            ) if self.config.metric else None,
            experiment_template_params=ExperimentTemplateParams(
                parameters=api_simple_parameters,
                properties=self.config.properties,
                remote_params=remote_params,
                hostname=self._get_hostname(is_local=remote_params is None),
                exec_args_template=exec_args_template,
                enqueue_command=enqueue_command,
                entrypoint=entrypoint
            )
        )

        group = self._call_with_exception_mapping(project, self.api_service.create_group, new_params)
        self.logger.info("Group: %s ENQUEUED", group.id)
        self.print_creation_confirmation(
            group.organization_name,
            group.project_name,
            Entity.group,
            group.short_id
        )
        return group

    def print_creation_confirmation(self, organization, project, entity_type, short_id):
        frontend_url_template = (
            "{frontend_url}/{organization}/{project}/{type}/{short_id}"
            "?getStartedState=folded"
        )

        frontend_url = frontend_url_template.format(
            frontend_url=self.config.frontend_http_url,
            organization=organization,
            project=project,
            type=str(entity_type).title()[0].lower(),
            short_id=short_id)

        print(self._format_creation_message(
            frontend_url=frontend_url, entity_id=short_id,
            entity=entity_type))
        self.web_browser.open(frontend_url)

    def _call_with_exception_mapping(self, project, fun, *args):
        try:
            return fun(*args)
        except NeptuneBadClientRequest as ex:
            if ex.response_message == u"Worker type {worker_type} is invalid.".format(worker_type=self.config.worker):
                raise NeptuneInvalidWorkerType(ex.response_message)
            elif ex.response_message == u"Environment {env} is invalid.".format(env=self.config.environment):
                raise NeptuneInvalidEnvironmentName(ex.response_message)
            else:
                raise ex
        except NeptuneValidationException as ex:
            if self._is_validation_error_caused_by_input(ex):
                raise NeptuneInputFileNotFound
            else:
                raise ex
        except NeptunePaymentRequiredException:
            PaymentsUtils(self.config).print_insufficient_funds()
            raise NeptuneNoCreditsToRunExperiment
        except NeptuneServerResponseErrorException as e:
            if e.status == 401:
                raise NeptuneExperimentCreationUnauthorized(project.organization_name, project.name)
            else:
                raise

    @staticmethod
    def _is_validation_error_caused_by_input(ex):
        return [err for err in ex.validation_error.validation_errors
                if u"inputs" in err.path]

    @staticmethod
    def _format_creation_message(frontend_url, entity_id, entity):
        return u">\n" + \
               u"> {entity} enqueued, id: {id}\n>\n".format(
                   entity=str(entity).title(), id=entity_id) + \
               u"> To browse the {entity}, follow:\n".format(entity=entity) + \
               u"> {frontend_url}\n>".format(frontend_url=frontend_url)

    @staticmethod
    def _get_hostname(is_local):
        if is_local:
            return hostname()
        else:
            return None
