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
from neptune.internal.client_library.background_services.service import Service
from neptune.internal.client_library.threads.channel_values_thread import ChannelValuesThread


class ChannelValuesService(Service):
    def __init__(self, experiment_id, job_api_service, max_form_content_size):
        super(ChannelValuesService, self).__init__(u"ChannelValuesService")
        self.channel_values_thread = ChannelValuesThread(
            experiment_id,
            job_api_service,
            max_form_content_size,
            self._done_event,
            self._shutdown_event
        )
        self.channel_values_thread.start()

    def send(self, channel, x, y):
        self.channel_values_thread.send(channel, x, y)

    def await_termination(self):
        self.channel_values_thread.join()

    def reset_channel(self, channel):
        self.channel_values_thread.reset_channel(channel=channel)

    def delete_channel(self, channel):
        self.channel_values_thread.delete_channel(channel=channel)

    def wait_for_threads(self):
        self.shutdown()
        self.done.wait()
