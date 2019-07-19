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

import abc
import logging
from enum import Enum

from future.builtins import object
from future.utils import with_metaclass

OK_EXIT_CODE = 0


class INeptuneCommand(object):

    exit_code = OK_EXIT_CODE

    def abort(self):
        pass

    def run(self, args):
        pass


class NeptuneCommand(with_metaclass(abc.ABCMeta, INeptuneCommand)):

    OK_EXIT_CODE = OK_EXIT_CODE
    UNKNOWN_EXCEPTION_EXIT_CODE = 1
    INVALID_EXPERIMENT_STATE_EXIT_CODE = 2
    ENTITY_NOT_FOUND_EXIT_CODE = 3
    NO_EXPERIMENT_TO_EXECUTE = 4
    ABORT_EXIT_CODE = 10

    def __init__(self, name, config, api_service):
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.config = config
        self.api_service = api_service
        self._exit_code = OK_EXIT_CODE

    @property
    def exit_code(self):
        return self._exit_code

    @exit_code.setter
    def exit_code(self, value):
        self._exit_code = value


class Entity(Enum):
    experiment = 2
    group = 4
    notebook = 3

    def __str__(self):
        return self.name


class MethodNames(object):
    def __init__(self, name, active, done):
        self.name = name
        self.active = active
        self.done = done
