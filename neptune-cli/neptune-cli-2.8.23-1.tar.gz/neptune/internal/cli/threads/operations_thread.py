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

import logging
import threading

from neptune.internal.cli.processes.aborting import Aborting
from neptune.internal.common.exceptions.base_exceptions import NeptuneThreadInterruptedException
from neptune.internal.common.threads.neptune_thread import NeptuneThread
from neptune.internal.common.websockets.message import MessageType
from neptune.internal.common.websockets.websocket_message_processor import \
    WebsocketMessageProcessor


class OperationsThread(NeptuneThread):
    def __init__(self, experiment_id, running_job_getter, websocket_factory):
        super(OperationsThread, self).__init__(is_daemon=True)
        self._abort_message_processor = AbortMessageProcessor(experiment_id, running_job_getter)
        self._ws_client = websocket_factory.create(shutdown_condition=threading.Event())

    def run(self):
        try:
            while not self.is_interrupted():
                raw_message = self._ws_client.recv()
                self._abort_message_processor.run(raw_message)
        except NeptuneThreadInterruptedException:
            pass

    def interrupt(self):
        super(OperationsThread, self).interrupt()
        self._ws_client.shutdown()

    def received_abort_message(self):
        return self._abort_message_processor.received_abort_message


class AbortMessageProcessor(WebsocketMessageProcessor):
    def __init__(self, experiment_id, running_job_getter):
        super(AbortMessageProcessor, self).__init__()
        self._logger = logging.getLogger(__name__)

        self._experiment_id = experiment_id
        self._running_job_getter = running_job_getter
        self.received_abort_message = False

    def _process_message(self, message):
        if message.get_type() == MessageType.ABORT:
            self._abort()

    def _abort(self):
        self._logger.debug(u'Aborting experiment %s...', self._experiment_id)
        self.received_abort_message = True
        aborting = Aborting(self._running_job_getter().process.pid)
        aborting.abort()
