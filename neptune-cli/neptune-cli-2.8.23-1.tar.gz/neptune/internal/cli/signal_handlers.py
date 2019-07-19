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

import signal
import sys

from neptune.internal.common.utils.system import IS_WINDOWS

_is_being_handled = False

ABORT_EXIT_CODE = 10


def setup_signal_handlers(command):

    def sigint_handler(*_):

        ''' SIGINT handler that calls command.abort exactly one time. '''

        global _is_being_handled  # pylint:disable=global-statement

        if not _is_being_handled:
            _is_being_handled = True
            command.abort()
            sys.exit(ABORT_EXIT_CODE)

    signal.signal(signal.SIGINT, sigint_handler)

    if IS_WINDOWS:
        signal.signal(signal.SIGBREAK, sigint_handler)  # pylint:disable=no-member


def setup_subprocess_signal_handlers():
    """
    Ignore sigint (sigbreak on Win) to avoid subprocesses to get SIGINT signal "at the same time" as parent process.
    Parent command signal handlers are responsible to finish subprocesses.
    """
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    if IS_WINDOWS:
        signal.signal(signal.SIGBREAK, signal.SIG_IGN)  # pylint:disable=no-member
