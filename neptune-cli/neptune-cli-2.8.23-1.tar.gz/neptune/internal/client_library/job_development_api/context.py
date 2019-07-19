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

from neptune.internal.client_library.context_factory import ContextFactory


def Context(tags=None, properties=None, offline_parameters=None):
    ''' Create Neptune Context - main entry point for Neptune functionality.

    If called without *offline_parameters*, Neptune will work normally; otherwise
    Neptune will work in offline mode.

    :param tags: Tags passed to Offline Context.
    :param properties: Properties passed to Offline Context
    :param offline_parameters: Parameters passed to Offline Context.
    :type tags: list
    :type properties: dict
    :type offline_parameters: dict
    :return: Neptune Context.
    :rtype: neptune.NeptuneContext
    '''

    return ContextFactory().create(
        tags=tags,
        properties=properties,
        offline_parameters=offline_parameters)
