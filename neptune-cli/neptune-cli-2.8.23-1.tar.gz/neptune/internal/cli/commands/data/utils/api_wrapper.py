# -*- coding: utf-8 -*-
#
# Copyright (c) 2018, deepsense.io
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
from neptune.internal.cli.commands.exceptions.data_exceptions import NeptuneFileNotFoundException, \
    NeptuneFileAccessForbidden

from neptune.internal.common.api.exceptions import NeptuneEntityNotFoundException, NeptuneServerResponseErrorException


class DataApiWrapper(object):

    def __init__(self):
        pass

    @staticmethod
    def execute(api_fun, **kwargs):
        try:
            return api_fun(**kwargs)
        except NeptuneEntityNotFoundException as ex:
            raise NeptuneFileNotFoundException(ex.response_message)
        except NeptuneServerResponseErrorException as ex:
            if u"is forbidden" in ex.response_message:
                raise NeptuneFileAccessForbidden(ex.response_message)
            else:
                raise
