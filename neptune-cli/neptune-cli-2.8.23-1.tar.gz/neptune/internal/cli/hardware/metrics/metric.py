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
from neptune.generated.swagger_client import SystemMetricParams


class Metric(object):
    def __init__(self, name, description, resource_type, unit, min_value, max_value, gauges):
        self.__name = name
        self.__description = description
        self.__resource_type = resource_type
        self.__unit = unit
        self.__min_value = min_value
        self.__max_value = max_value
        self.__gauges = gauges

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def resource_type(self):
        return self.__resource_type

    @property
    def unit(self):
        return self.__unit

    @property
    def min_value(self):
        return self.__min_value

    @property
    def max_value(self):
        return self.__max_value

    @property
    def gauges(self):
        return self.__gauges

    def __repr__(self):
        return 'Metric(name={}, description={}, resource_type={}, unit={}, min_value={}, max_value={}, gauges={})' \
            .format(self.name, self.description, self.resource_type, self.unit,
                    self.min_value, self.max_value, self.gauges)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and repr(self) == repr(other)

    def to_api_model(self):
        series = [gauge.name() for gauge in self.gauges]
        return SystemMetricParams(name=self.name, description=self.description, resource_type=self.resource_type,
                                  unit=self.unit, min=self.min_value, max=self.max_value, series=series)
