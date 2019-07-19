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

# pylint: disable=wrong-import-position

from future import standard_library

standard_library.install_aliases()

from future.builtins import object, range

import logging
import math
import time
from collections import defaultdict, deque

import datetime
from queue import Empty, Full, Queue
from threading import Lock


from neptune.generated.swagger_client import InputChannelValues, Point, Y
from neptune.internal.client_library.job_development_api.channel import AutoIncrementType
from neptune.internal.client_library.job_development_api.channel_type import ChannelType
from neptune.internal.client_library.threads.job_internal_thread import JobInternalThread
from neptune.internal.common.api.exceptions import NeptuneUnprocessableEntityException
from neptune.internal.common.api.utils import swagger_model_to_json
from neptune.internal.common.models.rich_input_channel_values import RichInputChannelValues
from neptune.internal.common.utils.memory_units import bytes_to_megabytes, get_object_size


class ChannelValuesBuffer(object):

    def __init__(self):
        self._buf = []

    def append(self, value):
        self._buf.append(value)

    def __len__(self):
        return len(self._buf)

    def __iter__(self):
        return iter(self._buf)

    def __contains__(self, value):
        return value in self._buf

    def clear(self, channel=None):

        if channel is not None:
            self._buf = [x for x in self._buf if x[0].id != channel.id]
        else:
            self._buf = []


class ChannelValuesSender(object):

    def __init__(self, experiment_id, api_service, max_interval, max_amount, max_content_size):
        self._logger = logging.getLogger(__name__)
        self.experiment_id = experiment_id
        self.api_service = api_service
        self.max_interval = max_interval
        self.max_content_size = max_content_size
        self.max_amount = max_amount
        self.buffer = ChannelValuesBuffer()
        self.size = 0
        self.last_send = time.time()

    def send_or_aggregate(self, channel, point):

        channel_value_size = get_object_size(point)
        if channel_value_size > self.max_content_size:
            self._log_channel_value_too_large(channel, point, channel_value_size)
            return 1
        elif self._can_be_appended_to_buffer(channel_value_size):
            if len(self.buffer) == 0:
                self._reset_last_send_timestamp()  # Prevents sending first value of a burst.
            self._append(channel, point, channel_value_size)
            return self._maybe_send_buffered()
        else:
            sent_values = self.send_buffered()
            self._append(channel, point, channel_value_size)
            return sent_values

    def reset_channel(self, channel):
        self.buffer.clear(channel)
        self.api_service.delete_channel_values(experiment_id=self.experiment_id, channel_id=channel.id)

    def delete_channel(self, channel):
        self.buffer.clear(channel)
        self.api_service.delete_channel(experiment_id=self.experiment_id, channel_id=channel.id)

    def _maybe_send_buffered(self):
        if self._should_send():
            return self.send_buffered()
        else:
            return 0

    def send_buffered(self):

        if self.buffer:
            self._reset_last_send_timestamp()
            to_send = self._group_channel_values()
            number_of_values_to_send = len(self.buffer)
            channel_id_to_name_mapping = {channel.id: channel.name for channel, _ in self.buffer}
            self.buffer.clear()
            self.size = 0

            try:
                channel_values_errors = self.api_service.send_channel_values(
                    experiment_id=self.experiment_id, channel_values=to_send)
                self._log_channel_value_errors(channel_id_to_name_mapping, channel_values_errors)

                return number_of_values_to_send
            except Exception as e:
                self._logger.error(e)
                return 0
        else:
            return 0

    def _reset_last_send_timestamp(self):
        self.last_send = time.time()

    def _group_channel_values(self):

        groups = defaultdict(list)

        for channel, point in self.buffer:
            groups[channel.id].append(point)
        return [
            RichInputChannelValues(
                InputChannelValues(
                    channel_id=channel_id,
                    values=groups[channel_id])) for channel_id in groups
        ]

    def _append(self, channel, point, channel_value_size):
        self.buffer.append((channel, point))
        self.size += channel_value_size

    def _can_be_appended_to_buffer(self, channel_value_size):
        return (len(self.buffer) < self.max_amount) and\
               (self.size + channel_value_size <= self.max_content_size)

    def _should_send(self):
        return (self.buffer and (self.last_send + self.max_interval < time.time())) or\
               (len(self.buffer) == self.max_amount)

    def _log_channel_value_too_large(self, channel, point, channel_value_size):
        reason = "Size of data is {size}MB and exceeds {limit}MB limit.".format(
            size=round(bytes_to_megabytes(channel_value_size), 2),
            limit=round(bytes_to_megabytes(self.max_content_size), 2))
        self._log_send_failure(channel.name, point.x, reason)

    def _log_channel_value_errors(self, channel_id_to_name_mapping, channel_value_errors):
        for channel_value_error in channel_value_errors:
            channel_name = channel_id_to_name_mapping[channel_value_error.channel_id]
            x = channel_value_error.x
            self._log_send_failure(channel_name, x, channel_value_error.error.message)

    def _log_send_failure(self, channel_name, x, reason):
        self._logger.warning("Failed to send value to '%s' channel in x=%s. %s", channel_name, x,
                             reason)


POINT = 1
RESET = 2
DELETE = 3


class ChannelValuesQueue(Queue):

    # pylint:disable=attribute-defined-outside-init

    def clear_channel(self, channel):
        with self.mutex:
            cleared = []

            for e in self.queue:
                if e[0] == POINT and e[1][0].id == channel.id:
                    continue
                cleared.append(e)

            self.queue = deque(cleared)


class ChannelValuesThread(JobInternalThread):
    IDLE_TIME_SECS = 0.1
    MAX_INTERVAL_BETWEEN_REQUESTS = 1.0
    MAX_AMOUNT_PER_REQUEST = 100
    OBJECT_SIZE_ESTIMATION_ERROR = 0.2
    MAX_CONTENT_FACTOR = (1 - OBJECT_SIZE_ESTIMATION_ERROR)
    MAX_QUEUE_SIZE = 100000

    def __init__(self, experiment_id, job_api_service, max_form_content_size, done_event, shutdown_event):
        super(ChannelValuesThread, self).__init__(name='channel-values-thread', is_daemon=True)
        self._lock = Lock()
        self._finished = False
        self._done_event = done_event
        done_event.set()
        self._shutdown_event = shutdown_event
        self._queue = ChannelValuesQueue(self.MAX_QUEUE_SIZE)
        self._sending_client = ChannelValuesSender(
            experiment_id=experiment_id,
            api_service=job_api_service,
            max_interval=self.MAX_INTERVAL_BETWEEN_REQUESTS,
            max_amount=self.MAX_AMOUNT_PER_REQUEST,
            max_content_size=self.MAX_CONTENT_FACTOR * max_form_content_size)

        self._auto_incrementer = AutoIncrementer()

    def send(self, channel, x, y):

        try:
            self._not_done()
            self._queue.put_nowait((POINT, (channel, x, y)))
        except Full:

            self._logger.warning(("Skipped value in x=%s for channel '%s' ",
                                  "The message queue has been filled up."), x, channel.name)

    def reset_channel(self, channel):

        self._queue.clear_channel(channel)
        self._queue.put_nowait((RESET, channel))

    def delete_channel(self, channel):
        self._queue.clear_channel(channel)
        self._queue.put_nowait((DELETE, channel))

    def _to_y(self, channel, y):
        value = Y()
        if channel.type == ChannelType.NUMERIC:
            value.numeric_value = y
        elif channel.type == ChannelType.TEXT:
            value.text_value = y
        elif channel.type == ChannelType.IMAGE:
            value.input_image_value = y.to_input_image()
        else:
            raise ValueError(u'Unexpected channel type: {}'.format(channel.type))
        return value

    def run(self):
        try:
            while (not self.is_interrupted()) and not self._shutdown_event.is_set():
                self._inner_run()
            self._send_remaining_messages()
        except NeptuneUnprocessableEntityException as exc:
            self._logger.debug(exc)
        finally:
            self._done()

    def _not_done(self):
        with self._lock:
            if not self._finished:
                self._done_event.clear()

    def _done(self):
        with self._lock:
            self._finished = True
        self._done_event.set()

    def _inner_run(self):
        if not self._process_queue():
            time.sleep(self.IDLE_TIME_SECS)

    def _send_remaining_messages(self):
        while self._process_queue():
            pass

    def _process_queue(self):

        non_empty = True

        try:
            cmd, args = self._queue.get_nowait()

            processed_values = 0

            if cmd == RESET:

                channel = args
                self._auto_incrementer.reset(channel)
                self._sending_client.reset_channel(channel)
                processed_values = 1

            elif cmd == DELETE:

                channel = args
                self._auto_incrementer.delete(channel)
                self._sending_client.delete_channel(channel)
                processed_values = 1

            elif cmd == POINT:

                channel, x, y = args

                x, valid = self._auto_incrementer.next_value(channel, x, y)

                if not valid:
                    processed_values = 1

                else:
                    y = swagger_model_to_json(self._to_y(channel, y))
                    point = Point(x, y)

                    processed_values = self._sending_client.send_or_aggregate(channel, point)

        except Empty:
            processed_values = self._sending_client.send_buffered()
            non_empty = False

        for _ in range(processed_values):
            self._queue.task_done()

        return non_empty


MAX_COLLISION_WARNINGS_FOR_CHANNEL = 10

class AutoIncrementer(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._last_x = dict()
        self._start_time = datetime.datetime.now()
        self._lock = Lock()

    def next_value(self, channel, x, y):
        with self._lock:
            if x is None:
                if channel.auto_increment_type is AutoIncrementType.Int:
                    x = self._next_natural_number(channel)
                elif channel.auto_increment_type is AutoIncrementType.Micro:
                    x = self._micors_since_start(channel)
                else:
                    raise Exception("x is None and no auto increment algorithm specified for channel " + channel.name)

            valid = self._validate(channel, x, y)
            if valid:
                self._last_x[channel] = x

            return x, valid

    def reset(self, channel):
        if channel in self._last_x:
            del self._last_x[channel]

    def delete(self, channel):
        if channel in self._last_x:
            del self._last_x[channel]

    def _next_natural_number(self, channel):
        if channel not in self._last_x:
            x = 1.0
        else:
            x = math.floor(self._last_x[channel]) + 1.0
        return x

    def _micors_since_start(self, channel):
        if channel not in self._last_x:
            x = self._time_delta_to_micros(
                datetime.datetime.now() - self._start_time)
        else:
            x = self._time_delta_to_micros(
                datetime.datetime.now() - self._start_time)
            if x == self._last_x[channel]:
                x += 0.000001
        return x

    def _validate(self, channel, x, y):
        valid = True
        if channel in self._last_x and x <= self._last_x[channel]:
            channel.collision_count = channel.collision_count + 1
            collision_warning = ("X-coordinate %s is not greater than the previous one %s. "
                                 "Dropping point (x=%s, y=%s) for channel %s. "
                                 "X-coordinates must be strictly increasing for each channel.")
            if channel.collision_count <= MAX_COLLISION_WARNINGS_FOR_CHANNEL:
                self._logger.warning(collision_warning,
                                     x, self._last_x[channel], x, y, channel.name)
            if channel.collision_count == MAX_COLLISION_WARNINGS_FOR_CHANNEL:
                self._logger.warning("Any further X-coordinates collisions will be silently ignored for this channel")

            valid = False

        return valid

    def _time_delta_to_micros(self, delta):
        return (delta.days * 24 * 3600 * 1000000 + delta.seconds * 1000000 + delta.microseconds * 1.0) / 1000000.0
