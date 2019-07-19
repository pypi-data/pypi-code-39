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
import io
import os
import re
import time

from future.builtins import object
from future.builtins import PY3

from neptune.internal.common.threads.neptune_thread import NeptuneThread
from neptune.internal.common.utils.text import cut_if_too_long


class StreamWrapper(object):

    def __init__(self, stream, target_stream=None):
        self.stream = stream
        self.target_stream = target_stream

    def __iter__(self):
        last_line_buffer = b''
        last_byte = b''
        current_byte = self._tee_byte()
        if PY3:
            line_sep = bytes(os.linesep, 'utf-8')
        else:
            line_sep = os.linesep

        while current_byte != b'':
            if os.linesep == '\r\n' and last_byte == b'\r' and current_byte == b'\n':
                line = last_line_buffer[-1].decode('UTF-8', errors='replace')
                yield StreamWrapper._process_line(line)
                last_line_buffer = b''
            elif current_byte == line_sep:
                line = last_line_buffer.decode('UTF-8', errors='replace')
                yield StreamWrapper._process_line(line)
                last_line_buffer = b''
            else:
                last_line_buffer += current_byte

            last_byte = current_byte
            current_byte = self._tee_byte()

        if last_line_buffer != b'':
            yield StreamWrapper._process_line(last_line_buffer.decode('UTF-8', errors='replace'))

    def _tee_byte(self):
        read_byte = os.read(self.stream.fileno(), 1)
        if self.target_stream is not None:
            os.write(self.target_stream.fileno(), read_byte)
        return read_byte

    @staticmethod
    def _process_line(line):
        return line.split('\r')[-1] + '\n'


class StreamRedirectingThread(NeptuneThread):

    def __init__(self, input_stream, handlers, target_stream=None):
        super(StreamRedirectingThread, self).__init__(is_daemon=True)
        self._input_stream = StreamWrapper(input_stream, target_stream)
        self.handlers = handlers

    def run(self):

        for line in self._input_stream:
            for handler in self.handlers:
                handler.handle(line)

        for handler in self.handlers:
            handler.cleanup()


class LineHandler(object):

    def handle(self, line):
        pass

    def cleanup(self):
        pass


class FileHandler(LineHandler):

    def __init__(self, filepath):
        self.file = io.open(filepath, 'a', encoding='UTF-8')

    def handle(self, line):
        self.file.write(line)
        self.file.flush()

    def cleanup(self):
        self.file.flush()
        self.file.close()


class QueueHandler(LineHandler):

    def __init__(self, queue):
        self.queue = queue

    def handle(self, line):
        self.queue.append(line)


class CroppingHandler(LineHandler):

    def __init__(self, handler):
        self.handler = handler

    def handle(self, line):
        self.handler.handle(cut_if_too_long(line.rstrip(), max_len=256, tail=True))


class LogChannelHandler(LineHandler):
    def __init__(self, channels, verbose=True):
        self.channels = channels
        # Prepare regex automates to save compute resources during furher processing
        self._regexes = {}
        for prefix in self.channels:
            whitespaces_pattern = r'[\ \t]*'
            number_pattern = r'[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?'
            pattern = r'(?u){}{}(?P<number>{})'.format(re.escape(prefix), whitespaces_pattern, number_pattern)
            self._regexes[prefix] = re.compile(pattern)
        self.verbose = verbose

    def handle(self, line):
        for (prefix, regex) in iter(self._regexes.items()):
            for match in regex.finditer(line):
                value = float(match.group('number'))
                self.channels[prefix].send(value)


class ChannelHandler(LineHandler):

    def __init__(self, channel):
        self.time_started = time.time() * 1000
        self.channel = channel

    def handle(self, line):
        self.channel.send(time.time() * 1000 - self.time_started, line)
