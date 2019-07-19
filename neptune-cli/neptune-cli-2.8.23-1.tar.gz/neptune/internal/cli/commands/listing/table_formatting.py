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
import functools
import textwrap

from future.builtins import object, zip
from terminaltables import AsciiTable

from neptune.internal.cli.commands.listing import field_formatting as fmt

fold = functools.partial(textwrap.fill, break_long_words=False)
fold_and_break = functools.partial(textwrap.fill, break_long_words=True)


FIELD_SETTINGS = {
    # Experiment related
    u'No.': (5, fold_and_break),
    u'entry_type': (12, fold_and_break),
    u'id': (36, fold_and_break),
    u'short_id': (12, fold_and_break),
    u'name': (50, fold_and_break),
    u'description': (30, fold_and_break),
    u'project': (30, fold_and_break),
    u'owner': (30, fold_and_break),
    u'time_of_creation': (16, fold_and_break),
    u'time_of_completion': (18, fold_and_break),
    u'state': (15, fold_and_break),
    u'tags': (36, fold_and_break),
    u'requirements': (36, fold_and_break),
    u'size': (8, fold_and_break),
    u'experiment_states': (15, fold),

    # Action related.
    u'action_name': (10, fold_and_break),
    u'action_invocation_id': (36, fold_and_break),
    u'action_invocation_state': (15, fold_and_break),
    u'argument': (12, fold_and_break),
    u'started': (12, fold_and_break),
    u'finished': (12, fold_and_break),
    u'result': (12, fold_and_break),
    u'timestamp': (12, fold_and_break),
    u'action_id': (12, fold_and_break),
    u'event_type': (15, fold_and_break),
    u'data': (12, fold_and_break),
    u'running_time': (6, fold_and_break),
    u'environment': (12, fold_and_break),
    u'worker_type': (12, fold_and_break),
    u'source_size': (8, fold_and_break),
    u'source_md5': (8, fold_and_break),
    u'commit_id': (8, fold_and_break),
    u'trashed': (8, fold_and_break),
    u'best_experiment': (36, fold_and_break),
    u'metric': (12, fold_and_break),
}


class AsciiTableFactory(object):

    @classmethod
    def create_horizontal_table(cls, selected_fields, formatted_models, heading=True):

        table_data = []

        for values in formatted_models:
            row = []
            for field, value in zip(selected_fields, values):
                width, transformation = FIELD_SETTINGS[field]
                row.append(transformation(value, width).ljust(width))

            table_data.append(row)

        if heading:
            table_data = [selected_fields] + table_data

        table = AsciiTable(table_data)

        table.inner_row_border = False
        table.outer_border = False

        if not heading:
            table.inner_heading_row_border = False

        return table.table


ENTRY_DEFAULT_FIELDS = ['No.', 'short_id', 'name', 'owner', 'time_of_creation', 'state']


class SimpleFormatter(object):

    def __init__(self, formatters):
        self.formatters = formatters

    def create_row(self, container, fields, **ctx):

        row = []

        for field in fields:
            row.append(self.formatters[field](field, container, ctx))

        return row


def LeaderboardRowFormatter():

    return SimpleFormatter(
        formatters=dict([
            ('No.', fmt.extract_to_unicode),
            ('entry_type', fmt.extract_to_unicode),
            ('id', fmt.extract_to_unicode),
            ('short_id', fmt.extract_to_unicode),
            ('name', fmt.extract_to_unicode),
            ('description', fmt.extract_to_unicode),
            ('owner', fmt.extract_to_unicode),
            ('time_of_creation', fmt.extract_to_datetime),
            ('time_of_completion', fmt.extract_to_datetime),
            ('state', fmt.format_state),
            ('tags', fmt.format_tags),
            ('trashed', fmt.extract_to_unicode),
            ('size', fmt.format_bytes),
            ('experiment_states', fmt.format_experiment_states),
            ('running_time', fmt.format_time),
            ('environment', fmt.extract_to_unicode),
            ('worker_type', fmt.extract_to_unicode),
            ('source_size', fmt.format_bytes),
            ('source_md5', fmt.extract_to_unicode),
            ('commit_id', fmt.extract_to_unicode),
            ('best_experiment', fmt.format_best_experiment),
            ('metric', fmt.format_metric),
            ])
        )
