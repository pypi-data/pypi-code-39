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


from future.builtins import object


class Metric(object):
    """
    Represents a metric used to compare jobs.
    """

    def __init__(self, channel_name, direction):
        """
        Creates a new metric.

        .. warning:: For internal use only.

        :param name: The name of the metric.
        :param channel_name: The name of the channel that contains metric values.
        :param direction: Either "minimize" or "maximize" -
                          the direction of metric values considered as better.
        """
        self.channel_name = channel_name
        self.direction = direction
