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
from collections import OrderedDict

from neptune.internal.common.utils.data_utils import decamelize_keys


class RowFactory(object):
    def __init__(self, formatter, fields, table_factory):

        self.index = 1
        self.formatter = formatter
        self.fields = fields
        self.table_factory = table_factory

    def format(self, entities, **ctx):

        for i, entity in enumerate(entities, start=self.index):
            add_header = self.index == 1
            entity['No.'] = i
            entity = OrderedDict([(f, entity[f]) for f in self.fields if f in entity])
            entity = self.formatter.create_row(entity, self.fields, **ctx)
            entity = self.table_factory.create_horizontal_table(
                self.fields, [entity], heading=add_header)

            self.index += 1

            yield entity


def decamelized(dcts):
    for dct in dcts:
        yield decamelize_keys(dct)
