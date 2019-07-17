# Copyright 2019 Age of Minds inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import grpc
import time
from distutils.util import strtobool
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

from grpc_reflection.v1alpha import reflection

from aom_framework.version import __version__

import aom_framework.services_pb2 as _services_pbs
from aom_framework.services_pb2_grpc import add_AgentServicer_to_server, add_EnvironmentServicer_to_server


ENABLE_REFLECTION_VAR_NAME = 'AOM_GRPC_REFLECTION'
DEFAULT_PORT = 9000
MAX_WORKERS = 10


# General aom_framework error
class Error(Exception):
    pass


# Error that occured while configuring the aom_framework
class ConfigError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class DataTypes:
    def __init__(self, env_config, env_state, env_state_delta, human_action, agent_action, state_collapse_fn):
        self.env_config = env_config
        self.env_state = env_state
        self.env_state_delta = env_state_delta
        self.human_action = human_action
        self.agent_action = agent_action
        self.state_collapse_fn = state_collapse_fn


# Inherit from this class to implement an agent
class Agent:
    VERSIONS: Dict[str, str]


# Inherit from this class to implement an environment
class Environment:
    VERSIONS: Dict[str, str]

    def __init__(self):
        self._rewards = [[], []]

    def send_reward(self, agent_id, reward_value, reward_confidence, user_data):
        self.rewards[agent_id].append((reward_value, reward_confidence, user_data))


# A Grpc endpoint serving an aom service
class GrpcServer:

    def __init__(self, service_type, data_types, port=DEFAULT_PORT):
        from aom_framework.agent_service import AgentService
        from aom_framework.env_service import EnvService

        self._port = port
        self._grpc_server = grpc.server(ThreadPoolExecutor(max_workers=MAX_WORKERS))

        # Register service
        if issubclass(service_type, Agent):
            self._service_type = _services_pbs._AGENT
            add_AgentServicer_to_server(AgentService(service_type, data_types), self._grpc_server)
        elif issubclass(service_type, Environment):
            self._service_type = _services_pbs._ENVIRONMENT
            add_EnvironmentServicer_to_server(EnvService(service_type, data_types), self._grpc_server)
        else:
            raise ConfigError('Invalid service type')

        # Enable grpc reflection if requested
        if strtobool(os.getenv(ENABLE_REFLECTION_VAR_NAME, 'false')):
            SERVICE_NAMES = (
                self._service_type.full_name,
                reflection.SERVICE_NAME,
            )
            reflection.enable_server_reflection(SERVICE_NAMES, self._grpc_server)

        self._grpc_server.add_insecure_port(f'[::]:{port}')

    def serve(self):
        self._grpc_server.start()
        print(f"{self._service_type.full_name} service listening on port {self._port}")

        try:
            while True:
                time.sleep(24*60*60)
        except KeyboardInterrupt:
            self._grpc_server.stop(0)
