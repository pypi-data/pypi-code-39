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
import os

from neptune.generated.swagger_client import models, NotebookCreationParams
from neptune.internal.common.api.parameter_api_conversions import parameters_to_api
from neptune.internal.common.config.neptune_config import EmptyConfig


class RichExperimentCreationParams(models.ExperimentCreationParams):

    @classmethod
    def create(cls,
               experiment_config,
               enqueue_command,
               entrypoint,
               exec_args_template,
               tracked_parameters,
               project_id,
               remote_params=None,
               hostname=None,
               is_notebook=False,
               notebook_source_filename=None):

        api_simple_parameters, _ = parameters_to_api(tracked_parameters, experiment_config.parameters)

        notebook_creation_params = None
        if is_notebook:
            notebook_contents = None
            if notebook_source_filename and os.path.isfile(notebook_source_filename):
                with open(notebook_source_filename, "rb") as notebook_file:
                    notebook_contents = notebook_file.read().decode("utf-8")

            notebook_creation_params = NotebookCreationParams(
                notebook_source_file_name=notebook_source_filename,
                notebook_source_file_contents=notebook_contents
            )

        if not experiment_config.local_config == EmptyConfig \
                and experiment_config.cwd in experiment_config.local_config.path:
            config_path = os.path.relpath(experiment_config.local_config.path, experiment_config.cwd)
        else:
            config_path = None

        params = cls(
            name=experiment_config.name,
            description=experiment_config.description,
            tags=experiment_config.tags,
            parameters=api_simple_parameters,
            properties=experiment_config.properties,
            remote_params=remote_params,
            hostname=hostname,
            enqueue_command=enqueue_command,
            entrypoint=entrypoint,
            exec_args_template=exec_args_template,
            project_id=project_id,
            notebook_creation_params=notebook_creation_params,
            config_path=config_path
        )

        return params
