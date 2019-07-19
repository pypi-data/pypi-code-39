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

from neptune.internal.cli.commands.executing.docker_experiment_executor import DockerExperimentExecutor
from neptune.internal.cli.commands.executing.experiment_executor import (
    ExperimentExecutor,
    GCPJobExecutor,
    InDockerJobExecutor
)
from neptune.internal.cli.hardware.gauges.gauge_mode import GaugeMode
from neptune.internal.cli.processes.job_spawner import JobSpawner
from neptune.internal.client_library.background_services.channel_values_service import \
    ChannelValuesService
from neptune.internal.client_library.job_development_api.channel import ChannelFactory


class JobExecutorFactory(object):

    def __init__(self, config, api_service_factory, api_service, inside_docker,
                 offline_token_storage_service, keycloak_api_service, utilities_service,
                 exec_args_formatter, local_storage, pip_requirements_file=None, inside_gcp=False,
                 sources_dir_to_copy=None):
        self.api_service = api_service
        self.api_service_factory = api_service_factory
        self.config = config
        self.inside_docker = inside_docker
        self.inside_gcp = inside_gcp
        self.keycloak_api_service = keycloak_api_service
        self.offline_token_storage_service = offline_token_storage_service
        self.utilities_service = utilities_service
        self.exec_args_formatter = exec_args_formatter
        self.pip_requirements_file = pip_requirements_file
        self.sources_dir_to_copy = sources_dir_to_copy
        self._local_storage = local_storage

    def create(self, experiment, docker_image=None, custom_execution_paths=None):

        max_form_content_size = self.utilities_service.get_config_info().max_form_content_size

        experiment_id = experiment.id

        channel_factory = ChannelFactory(
            self.api_service,
            experiment_id,
            ChannelValuesService(
                experiment_id,
                self.api_service,
                max_form_content_size))

        if self.inside_docker:
            return self.create_in_docker_experiment_executor(channel_factory, custom_execution_paths)
        elif docker_image:
            return self.create_docker_experiment_executor(docker_image, custom_execution_paths)
        elif self.inside_gcp:
            return self.create_gcp_experiment_executor(channel_factory, custom_execution_paths)
        else:
            return self.create_experiment_executor(channel_factory, custom_execution_paths)

    def create_docker_experiment_executor(self, docker_image, custom_execution_paths):
        return DockerExperimentExecutor(
            api_service=self.api_service,
            job_spawner=JobSpawner(),
            config=self.config,
            docker_image=docker_image,
            custom_execution_paths=custom_execution_paths,
            local_storage=self._local_storage
        )

    def create_experiment_executor(self, channel_factory, custom_execution_paths):
        return ExperimentExecutor(
            config=self.config,
            api_service_factory=self.api_service_factory,
            api_service=self.api_service,
            channel_factory=channel_factory,
            job_spawner=JobSpawner(),
            offline_token_storage_service=self.offline_token_storage_service,
            keycloak_api_service=self.keycloak_api_service,
            exec_args_formatter=self.exec_args_formatter,
            pip_requirements_file=self.pip_requirements_file,
            sources_dir_to_copy=self.sources_dir_to_copy,
            custom_execution_paths=custom_execution_paths,
            hardware_metrics_gauge_mode=GaugeMode.SYSTEM,
            local_storage=self._local_storage
        )

    def create_gcp_experiment_executor(self, channel_factory, custom_execution_paths):
        return GCPJobExecutor(
            config=self.config,
            api_service_factory=self.api_service_factory,
            api_service=self.api_service,
            channel_factory=channel_factory,
            job_spawner=JobSpawner(),
            offline_token_storage_service=self.offline_token_storage_service,
            keycloak_api_service=self.keycloak_api_service,
            exec_args_formatter=self.exec_args_formatter,
            pip_requirements_file=self.pip_requirements_file,
            sources_dir_to_copy=self.sources_dir_to_copy,
            custom_execution_paths=custom_execution_paths,
            hardware_metrics_gauge_mode=GaugeMode.CGROUP,
            local_storage=self._local_storage
        )

    def create_in_docker_experiment_executor(self, channel_factory, custom_execution_paths):
        return InDockerJobExecutor(
            config=self.config,
            api_service_factory=self.api_service_factory,
            api_service=self.api_service,
            channel_factory=channel_factory,
            job_spawner=JobSpawner(),
            offline_token_storage_service=self.offline_token_storage_service,
            keycloak_api_service=self.keycloak_api_service,
            exec_args_formatter=self.exec_args_formatter,
            pip_requirements_file=self.pip_requirements_file,
            sources_dir_to_copy=self.sources_dir_to_copy,
            custom_execution_paths=custom_execution_paths,
            hardware_metrics_gauge_mode=GaugeMode.CGROUP,
            local_storage=self._local_storage
        )
