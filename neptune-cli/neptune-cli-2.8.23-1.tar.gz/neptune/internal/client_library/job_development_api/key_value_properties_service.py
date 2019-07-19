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
import collections

import neptune.generated.swagger_client.models as api_models
from neptune.internal.common.models.key_value_properties_utils import (
    properties_from_dict,
    properties_to_dict
)
from neptune.internal.common.models.parameters_validation import validate, text_conv


class KeyValuePropertiesService(collections.MutableMapping):

    def __init__(self, experiment_id, neptune_api_handler):
        self._experiment_id = experiment_id
        self._rest_client = neptune_api_handler

    @validate(key=text_conv)
    def __getitem__(self, key):
        return self.__all_properties()[key]

    @validate(key=text_conv, value=text_conv)
    def __setitem__(self, key, value):
        properties_dict = self.__all_properties()
        properties_dict[key] = value
        self.__post_changes(properties_dict)

    @validate(key=text_conv)
    def __delitem__(self, key):
        properties_dict = self.__all_properties()
        if key in properties_dict:
            del properties_dict[key]
        self.__post_changes(properties_dict)

    def __iter__(self):
        return iter(self.__all_properties())

    def __len__(self):
        return len(self.__all_properties())

    def __all_properties(self):
        job_properties = self._rest_client.get_experiment(self._experiment_id)\
            .properties
        return properties_to_dict(job_properties[:])

    def __post_changes(self, properties_dict):
        edit_job_params = api_models.EditExperimentParams()
        edit_job_params.properties = properties_from_dict(properties_dict)
        self._rest_client.update_experiment(self._experiment_id, edit_job_params)
