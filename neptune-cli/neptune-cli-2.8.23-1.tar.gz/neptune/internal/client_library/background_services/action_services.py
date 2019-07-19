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
from neptune.internal.client_library.background_services.service import Service
from neptune.internal.client_library.threads.action_executor import ActionExecutor
from neptune.internal.client_library.threads.action_invocation_receiver_thread import \
    ActionInvocationReceiverThread


class ActionInvocationsService(Service):
    def __init__(self, executor_service, websocket_factory):
        super(ActionInvocationsService, self).__init__(u"ActionsService")
        self._action_invocation_receiver_thread = ActionInvocationReceiverThread(
            action_executor=executor_service,
            websocket_factory=websocket_factory,
            shutdown_event=self._shutdown_event)
        self._done_event.set()  # can be shut down in any moment
        self._action_invocation_receiver_thread.start()

    def await_termination(self):
        self._action_invocation_receiver_thread.join()
        self._done_event.wait()


class ActionsExecutorService(Service):
    def __init__(self, experiment_id, job_actions, job_api_service):
        super(ActionsExecutorService, self).__init__(u"ActionsService")
        self._action_executor = ActionExecutor(
            thread_pool_size=1,
            experiment_id=experiment_id,
            api_service=job_api_service,
            actions_map=job_actions,
            done_event=self._done_event,
            shutdown_event=self._shutdown_event)

    def execute_action(self, action_invocation):
        self._action_executor.execute_action(action_invocation)

    def await_termination(self):
        self._done_event.wait()
