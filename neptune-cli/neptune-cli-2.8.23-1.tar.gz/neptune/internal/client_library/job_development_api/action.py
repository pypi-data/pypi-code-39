# -*- coding: utf-8 -*-
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

import uuid


class Action(object):
    """
    An Action is a registered function that can be invoked externally with passed argument.
    """
    def __init__(self, name, handler):
        """Registers a new action that calls handler with provided argument on invocation.

        .. warning:: For internal use only.

           Use :py:meth:`~neptune.Job.register_action` instead to register a new action.

        :param name: Unique action name.
        :param handler: An one argument function that will be called with an action invocation.
                        Handler must take one unicode or str argument and return unicode or str
                        as the result.
        :type name: unicode
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.handler = handler
