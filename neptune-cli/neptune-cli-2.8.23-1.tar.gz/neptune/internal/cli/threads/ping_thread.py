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

from neptune.internal.cli.processes.aborting import Aborting
from neptune.internal.common.api.exceptions import NeptuneUnprocessableEntityException
from neptune.internal.common.threads.neptune_thread import NeptuneThread


class PingThread(NeptuneThread):
    PING_INTERVAL_SECS = 5

    def __init__(self, api_service_factory, experiment_id, running_job_getter):
        super(PingThread, self).__init__(is_daemon=True)
        self._logger = logging.getLogger(__name__)

        self._api_service, _, _ = api_service_factory.create_services()
        self._experiment_id = experiment_id
        self._running_job_getter = running_job_getter

    def run(self):
        while not self.is_interrupted():
            try:
                self._api_service.ping_experiment(self._experiment_id)
            except NeptuneUnprocessableEntityException:
                # A 422 error means that we tried to ping the job after marking it as completed.
                # In this case, this thread is not needed anymore.
                self._abort()
                break
            except Exception as e:
                self._logger.error(e)
            self._interrupted.wait(self.PING_INTERVAL_SECS)

    def _abort(self):
        self._logger.debug(u'Aborting experiment %s...', self._experiment_id)
        aborting = Aborting(self._running_job_getter.process.pid)
        aborting.abort()
        print(u'Experiment {} has been externally aborted.'.format(self._experiment_id))
