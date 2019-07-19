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
import argparse


class NeptuneRawDescriptionHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def __init__(self, *args, **kwargs):
        super(NeptuneRawDescriptionHelpFormatter, self).__init__(width=100, *args, **kwargs)

    def _split_lines(self, text, width):
        return [item for sublist in [self._split_line(x, width) for x in text.splitlines()]
                for item in sublist]

    def _split_line(self, line, width):
        if len(line) > width:
            return super(NeptuneRawDescriptionHelpFormatter, self)._split_lines(line, width)
        else:
            return [line]


class RawDescriptionOnlyHeaderHelpFormatter(NeptuneRawDescriptionHelpFormatter):
    def __init__(self, *args, **kwargs):
        super(RawDescriptionOnlyHeaderHelpFormatter, self).__init__(*args, **kwargs)

    def _format_usage(self, usage, actions, groups, prefix):
        return None

    def _format_action(self, action):
        return None
