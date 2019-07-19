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

from neptune.internal.common.models.key_value_properties_utils import merge_properties_lists

class ConfigurationOverridingUtils(object):
    def __init__(self):
        pass

    @staticmethod
    def merge_tags(job_tags, override_args_tags):
        """
        :param job_tags: list[str]
        :param override_args_tags: list[str]
        :return: list[str]
        Returns job_tags + override_args_tags.
        """
        new_job_tags = []

        if job_tags:
            new_job_tags += job_tags

        if override_args_tags:
            new_job_tags += override_args_tags

        return list(set(new_job_tags))

    @staticmethod
    def merge_properties(job_swagger_properties, override_args_properties):
        """
        :param job_swagger_properties: list[KeyValuePropertyParam]
        :param override_args_properties: list[KeyValuePropertyParam]
        :return: list[KeyValuePropertyParam]
        Overrides job_swagger_properties with override_args_properties.
        """
        return merge_properties_lists(job_swagger_properties or [], override_args_properties or [])
