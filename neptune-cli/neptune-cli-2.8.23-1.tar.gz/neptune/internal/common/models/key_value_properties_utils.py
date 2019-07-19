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
from collections import OrderedDict
from future.utils import iteritems, listvalues

from neptune.generated.swagger_client.models.key_value_property import KeyValueProperty

PROPERTY_KEY = 'key'
PROPERTY_VALUE = 'value'


def properties_to_dict(properties):
    return {p.key: p.value for p in properties}


def properties_from_dict(properties_dict):
    return [KeyValueProperty(k, v) for k, v in iteritems(properties_dict)]


def properties_maps_to_dict(properties):
    if properties:
        return OrderedDict((p[PROPERTY_KEY], p[PROPERTY_VALUE]) for p in properties)
    else:
        return {}


def properties_from_config_file(config_properties):
    return properties_from_dict(properties_maps_to_dict(config_properties))


def merge_properties_lists(p1, p2):

    def to_dict(properties):
        return OrderedDict((p.key, p) for p in properties)

    def from_dict(d):
        return listvalues(d)

    d1 = to_dict(p1)
    d1.update(to_dict(p2))
    return from_dict(d1)
