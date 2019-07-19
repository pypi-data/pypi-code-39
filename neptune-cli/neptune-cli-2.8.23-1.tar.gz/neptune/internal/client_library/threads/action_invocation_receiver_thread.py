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
from neptune.internal.client_library.threads.action_executor import ActionInvocationInfo
from neptune.internal.client_library.threads.job_internal_thread import JobInternalThread
from neptune.internal.common.exceptions.base_exceptions import NeptuneThreadInterruptedException
from neptune.internal.common.websockets.message import MessageType
from neptune.internal.common.websockets.websocket_message_processor import \
    WebsocketMessageProcessor


class ActionInvocationReceiverThread(JobInternalThread):
    def __init__(self, action_executor, websocket_factory, shutdown_event):
        super(ActionInvocationReceiverThread, self).__init__(
            name='action-invocation-receiver-thread', is_daemon=True)
        self._shutdown_event = shutdown_event
        self._action_executor = action_executor
        self._action_invoked_message_processor = ActionInvokedMessageProcessor(action_executor)
        self._websocket_factory = websocket_factory

    def run(self):
        ws_client = self._websocket_factory.create(self._shutdown_event)
        try:
            while not self._shutdown_event.is_set():
                raw_message = ws_client.recv()
                self._action_invoked_message_processor.run(raw_message)
        except NeptuneThreadInterruptedException:
            pass


class ActionInvokedMessageProcessor(WebsocketMessageProcessor):
    def __init__(self, action_executor):
        super(ActionInvokedMessageProcessor, self).__init__()
        self._action_executor = action_executor

    def _process_message(self, message):
        if message.get_type() == MessageType.ACTION_INVOCATION:
            self._action_executor.execute_action(ActionInvocationInfo(
                message.action_id,
                message.action_invocation_id,
                message.argument
            ))
