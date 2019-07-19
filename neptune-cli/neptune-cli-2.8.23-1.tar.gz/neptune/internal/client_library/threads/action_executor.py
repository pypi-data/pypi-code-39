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
from future.builtins import object, str

import logging
import threading
import traceback
from multiprocessing.pool import ThreadPool

from neptune.internal.common.utils.str import to_unicode


class ActionExecutor(object):
    def __init__(self, thread_pool_size, experiment_id, api_service, actions_map,
                 done_event, shutdown_event):
        self._thread_pool = ThreadPool(thread_pool_size)
        self._experiment_id = experiment_id
        self._api_service = api_service
        self._actions_map = actions_map
        self._logger = logging.getLogger(__name__)
        self._done_event = done_event
        self._shutdown_event = shutdown_event
        self._running_action_count = 0
        self._running_actions_lock = threading.Lock()

        done_event.set()

    def execute_action(self, action_invocation):
        def execute_action(action_invocation_info):
            self._logger.debug("Invoking action: " + str(action_invocation_info))
            try:
                action_handler = self._actions_map[action_invocation_info.action_id].handler
                result = action_handler(action_invocation_info.argument)
                result = "" if result is None else to_unicode(result)
                self._api_service.mark_action_invocation_succeeded(
                    self._experiment_id,
                    action_invocation_info.action_id,
                    action_invocation_info.action_invocation_id,
                    result)
            except BaseException:
                exception_traceback = "\n".join(to_unicode(traceback.format_exc()).splitlines())
                self._api_service.mark_action_invocation_failed(
                    self._experiment_id,
                    action_invocation_info.action_id,
                    action_invocation_info.action_invocation_id,
                    exception_traceback)
            finally:
                self._execution_finished()
        if self._shutdown_event.is_set():
            self._logger.debug("Got action to invoke, but experiment is shutting down!")
        else:
            self._execution_started()
            return self._thread_pool.apply_async(func=execute_action, args=(action_invocation,))

    def _execution_finished(self):
        self._running_actions_lock.acquire()
        self._running_action_count -= 1
        if self._running_action_count == 0:
            self._done_event.set()
        self._running_actions_lock.release()

    def _execution_started(self):
        self._running_actions_lock.acquire()
        self._done_event.clear()
        self._running_action_count += 1
        self._running_actions_lock.release()

    def allow_no_more_actions(self):
        self._thread_pool.close()

    def wait_for_running_actions(self):
        self._thread_pool.join()


class ActionInvocationInfo(object):
    def __init__(self, action_id, action_invocation_id, argument):
        self.action_id = action_id
        self.action_invocation_id = action_invocation_id
        self.argument = argument

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __unicode__(self):
        return u"action_id: {}, action_invocation_id: {}, argument: {}".format(
            self.action_id, self.action_invocation_id, self.argument)
