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

import logging
import threading


class Service(object):
    def __init__(self, name):
        self._done_event = threading.Event()
        self._shutdown_event = threading.Event()
        self._name = name
        self._logger = logging.getLogger(__name__)

    @property
    def name(self):
        return self._name

    @property
    def done(self):
        return self._done_event

    def shutdown(self):
        self._shutdown_event.set()

    def await_termination(self):
        raise NotImplementedError
