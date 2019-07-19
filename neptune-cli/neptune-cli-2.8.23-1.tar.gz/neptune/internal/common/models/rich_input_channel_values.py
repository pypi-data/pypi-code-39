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

from future.builtins import str

from neptune.generated.swagger_client import InputChannelValues


class RichInputChannelValues(InputChannelValues):

    # pylint:disable=super-init-not-called
    def __init__(self, input_channel_values):
        self.__dict__.update(vars(input_channel_values))

    def __eq__(self, other):

        if isinstance(other, RichInputChannelValues):
            return (self.channel_id == other.channel_id) and (self.values == other.values)
        else:
            return NotImplemented

    def __hash__(self):
        return hash(str(self.channel_id) + str(self.values))
