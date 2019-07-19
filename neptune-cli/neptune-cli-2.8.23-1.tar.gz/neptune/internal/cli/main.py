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

from future.utils import PY3
from distutils.version import LooseVersion  # pylint: disable=no-name-in-module, import-error
import sys

PYTHON_VERSION = LooseVersion(sys.version.split()[0])


def is_python_version_supported():
    if PY3:
        return PYTHON_VERSION >= LooseVersion('3.4.0')
    else:
        return PYTHON_VERSION >= LooseVersion('2.7.0')


def main():
    if is_python_version_supported():
        from neptune.internal.cli.run import run
        run(sys.argv[1:], version_update_suggestion_on=True)
    else:
        sys.exit(
            "Sorry, Neptune CLI was run with not supported Python {actual_version}. "
            "Currently we support Python 3.5.2+ and Python 2.7.12+.\n"
            "Please make sure that `python --version` returns supported version.\n".format(
                actual_version=PYTHON_VERSION))


if __name__ == '__main__':
    main()
