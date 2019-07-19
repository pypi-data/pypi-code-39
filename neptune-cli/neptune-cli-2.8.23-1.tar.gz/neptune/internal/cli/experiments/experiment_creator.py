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
from collections import namedtuple

from neptune.internal.common.parsers.command_parsing_utils import compose_exec_args_template


class ExperimentsCreator(object):
    def __init__(self, enqueue_utils, project):
        self.__enqueue_utils = enqueue_utils
        self.__project = project

    def create(self, experiment_config, enqueue_command, notebook_absolute_path,
               tracked_params, parameters, remote_params):
        runnable_type = self._runnable_type(
            tracked_experiment_params=tracked_params, parameters=parameters,
            notebook_absolute_path=notebook_absolute_path)

        if runnable_type == RunnableType.GROUP:
            group = self._create_group(
                experiment_config=experiment_config, enqueue_command=enqueue_command,
                tracked_experiment_params=tracked_params, remote_params=remote_params)
            return ExperimentsCreationResult(
                short_id=group.short_id,
                group_id=group.id,
                experiment_ids=group.experiment_ids
            )
        elif runnable_type == RunnableType.NOTEBOOK:
            notebook = self._create_notebook(notebook_absolute_path=notebook_absolute_path, remote_params=remote_params)
            return ExperimentsCreationResult(
                short_id=notebook.short_id,
                group_id=None,
                experiment_ids=[notebook.id]
            )
        else:
            experiment = self._create_experiment(
                experiment_config=experiment_config, enqueue_command=enqueue_command,
                tracked_experiment_params=tracked_params, remote_params=remote_params)
            return ExperimentsCreationResult(
                short_id=experiment.short_id,
                group_id=None,
                experiment_ids=[experiment.id]
            )

    def _runnable_type(self, tracked_experiment_params, parameters, notebook_absolute_path):
        if notebook_absolute_path is not None:
            return RunnableType.NOTEBOOK
        elif self.__enqueue_utils.is_grid_search(tracked_experiment_params, parameters):
            return RunnableType.GROUP
        else:
            return RunnableType.EXPERIMENT

    def _create_experiment(self, experiment_config, enqueue_command, tracked_experiment_params, remote_params):
        return self.__enqueue_utils.create_enqueued_experiment(
            entrypoint=experiment_config.executable, tracked_params=tracked_experiment_params,
            enqueue_command=enqueue_command, exec_args_template=compose_exec_args_template(experiment_config.cmd_args),
            project=self.__project, remote_params=remote_params
        )

    def _create_group(self, experiment_config, enqueue_command, tracked_experiment_params, remote_params):
        return self.__enqueue_utils.create_enqueued_group(
            entrypoint=experiment_config.executable, tracked_parameters=tracked_experiment_params,
            enqueue_command=enqueue_command,
            exec_args_template=compose_exec_args_template(experiment_config.cmd_args),
            project=self.__project, remote_params=remote_params
        )

    def _create_notebook(self, notebook_absolute_path, remote_params):
        return self.__enqueue_utils.create_enqueued_notebook(
            notebook_source_filename=notebook_absolute_path, project=self.__project, remote_params=remote_params)


ExperimentsCreationResult = namedtuple('ExperimentsCreationResult', ['short_id', 'group_id', 'experiment_ids'])


class RunnableType(object):
    EXPERIMENT = u'experiment'
    NOTEBOOK = u'notebook'
    GROUP = u'group'
