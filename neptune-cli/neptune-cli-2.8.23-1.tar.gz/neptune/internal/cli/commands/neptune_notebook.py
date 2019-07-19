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

from future.builtins import object

from neptune.internal.cli.commands.neptune_run import NeptuneRunWorker
from neptune.internal.common.config.job_config import ConfigKeys
from neptune.internal.common.config.neptune_config import (
    NeptuneConfig,
    load_global_config,
    load_local_config
)
from neptune.internal.common.models.rich_project import ProjectResolver
from neptune.internal.common.parsers.common_parameters_configurator import CommonParametersConfigurator


class NeptuneNotebook(NeptuneRunWorker):
    def __init__(self,
                 config,
                 local_storage,
                 api_service,
                 tracked_parameter_parser,
                 inputs,
                 environment,
                 worker,
                 web_browser,
                 project,
                 experiment_executor_factory):
        super(NeptuneNotebook, self).__init__(config=config, local_storage=local_storage, api_service=api_service,
                                              tracked_parameter_parser=tracked_parameter_parser,
                                              inputs=inputs, environment=environment, worker=worker,
                                              web_browser=web_browser, project=project,
                                              experiment_executor_factory=experiment_executor_factory)

    def run(self, args):
        self.prepare(args)

        self.experiment_ids = self._create_experiments(args).experiment_ids
        self._close_experiment_creation_message()

        self._configure_experiments(self.experiment_ids)

    def _get_notebook_absolute_path(self):
        notebook = self.experiment_config.notebook_filename
        if self.experiment_config.notebook_filename is None:
            print(u"Using default notebook")
            self.experiment_config.notebook = NeptuneConfig.DEFAULT_NOTEBOOK[0]
            return self.experiment_config.notebook
        else:
            return notebook

    @classmethod
    def _create_run_parameters(cls, args):
        profile = getattr(args.known_args,
                          ConfigKeys.PROFILE,
                          CommonParametersConfigurator.DEFAULT_PROFILE)
        return NeptuneConfig(
            commandline_args=args,
            local_config=load_local_config(args.known_args.config),
            global_config=load_global_config(profile),
            cli_parameters=[]
        )


class NeptuneNotebookFactory(object):

    def __init__(self, api_service, config, local_storage, tracked_parameter_parser, web_browser,
                 experiment_executor_factory):
        self.api_service = api_service
        self.config = config
        self.local_storage = local_storage
        self.tracked_parameter_parser = tracked_parameter_parser
        self.web_browser = web_browser
        self.experiment_executor_factory = experiment_executor_factory

    def create(self, inputs, environment, worker):
        web_browser = self.web_browser
        project = ProjectResolver.resolve(
            api_service=self.api_service,
            organization_name=self.config.organization_name,
            project_name=self.config.project_name)

        return NeptuneNotebook(
            config=self.config,
            local_storage=self.local_storage,
            api_service=self.api_service,
            tracked_parameter_parser=self.tracked_parameter_parser,
            inputs=inputs,
            environment=environment,
            worker=worker,
            project=project,
            web_browser=web_browser,
            experiment_executor_factory=self.experiment_executor_factory
        )
