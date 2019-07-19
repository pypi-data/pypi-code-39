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

from neptune.internal.client_library.background_services.action_services import (
    ActionInvocationsService,
    ActionsExecutorService
)
from neptune.internal.client_library.background_services.channel_values_service import \
    ChannelValuesService
from neptune.internal.client_library.threads.job_internal_thread import JobInternalThread


class Services(object):
    def __init__(self, experiment_id, job_api_service, max_form_content_size, job_actions,
                 parent_thread, websocket_factory):
        self._experiment_id = experiment_id
        self._job_api_service = job_api_service
        self._max_form_content_size = max_form_content_size
        self._job_actions = job_actions
        self._actions_invocation_receiver_service = None
        self._actions_executor_service = None
        self._channel_values_service = None
        self._services_watcher_thread = None
        self._parent_thread = parent_thread
        self._websocket_factory = websocket_factory

    @property
    def channel_values_service(self):
        return self._channel_values_service

    def start(self):
        self._actions_executor_service = ActionsExecutorService(
            self._experiment_id,
            self._job_actions,
            self._job_api_service)
        self._actions_invocation_receiver_service = ActionInvocationsService(
            self._actions_executor_service,
            self._websocket_factory)
        self._channel_values_service = ChannelValuesService(
            self._experiment_id, self._job_api_service, self._max_form_content_size)

        services = [
            self._actions_invocation_receiver_service,
            self._actions_executor_service,
            self._channel_values_service
        ]

        self._services_watcher_thread = ServicesWatcherThread(
            parent_thread=self._parent_thread,
            watched_services=services)
        self._services_watcher_thread.start()

        return self

    def await_termination(self):
        self._services_watcher_thread.join()


class ServicesWatcherThread(JobInternalThread):
    def __init__(self, parent_thread, watched_services):
        super(ServicesWatcherThread, self).__init__(name='services-watcher-thread', is_daemon=False)
        self._parent_thread = parent_thread
        self._watched_services = watched_services

    def run(self):
        if self._parent_thread:
            self._wait_for_parent_thread()
        self._wait_for_services()
        self._logger.debug("Shutting down!")

    def _wait_for_parent_thread(self):
        self._logger.debug("Waiting for the parent thread!")
        self._parent_thread.join()
        self._logger.debug("The parent thread joined!")

    def _wait_for_services(self):
        for service in self._watched_services:
            self._logger.debug("Notifying service: " + service.name)
            service.shutdown()
            self._logger.debug("Waiting for service: " + service.name)
            service.done.wait()
