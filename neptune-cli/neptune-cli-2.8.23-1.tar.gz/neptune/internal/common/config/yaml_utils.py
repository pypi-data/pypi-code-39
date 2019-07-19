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
import yaml

from neptune.internal.common import NeptuneException


class SimpleYamlEditor(object):

    def __init__(self):
        self._content = ''

    def set(self, key, value):
        start, end = self.find(key)
        key_value_str = u'{key}: {value}'.format(key=key, value=value)
        if start and end:
            self._content = self.replace(start, end, key_value_str)
        else:
            self._content = self._content + u'\n' + key_value_str + u'\n'
        try:
            yaml.load(self._content)
        except:
            raise NeptuneException(u'Wrong yaml content')


    def set_content(self, content):
        self._content = content

    def get_content(self):
        return self._content

    def read(self, path):
        with open(path) as infile:
            self._content = infile.read()

    def write(self, path):
        with open(path, 'w+') as outfile:
            outfile.write(self._content)

    def find(self, key):
        start = None
        for token in yaml.scan(self._content):
            if isinstance(token, yaml.ScalarToken) and start:
                end = (token.end_mark.line, token.end_mark.column)
                return start, end

            if isinstance(token, yaml.ScalarToken) and token.value == key:
                start = (token.start_mark.line, token.start_mark.column)

        return None, None

    def replace(self, start_pos, end_pos, text):
        ret = u''
        start_line, start_column = start_pos
        end_line, end_column = end_pos
        for i, line in enumerate(self._content.splitlines()):
            if i < start_line or i > end_line:
                ret += line
                ret += u'\n'
            if i == start_line:
                ret += line[0:start_column]
                ret += text
            if i == end_line:
                ret += line[end_column:]
                ret += u'\n'

        return ret
