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
from future.builtins import object

import os

from pykwalify.core import Core

from neptune.internal.cli.exceptions.job_config_exceptions import \
    JobConfigValidationFailException


class NeptuneConfigValidator(object):

    def __init__(self, neptune_config_identifier):
        self.neptune_config_identifier = neptune_config_identifier

    def validate(self, schema_config_filename, source_file=None, source_data=None):
        dirpath = os.path.dirname(__file__)
        schema_file = os.path.join(dirpath, 'resources/' + schema_config_filename)

        validation_rules_filepath = os.path.join(dirpath, 'validation_rules.py')

        try:
            c = Core(
                source_file=source_file,
                schema_files=[schema_file],
                source_data=source_data,
                extensions=[validation_rules_filepath])
            c.validate(raise_exception=False)

        except AssertionError as error:
            raise JobConfigValidationFailException(self.neptune_config_identifier, [error])

        if c.validation_errors:
            raise JobConfigValidationFailException(self.neptune_config_identifier, c.validation_errors)
