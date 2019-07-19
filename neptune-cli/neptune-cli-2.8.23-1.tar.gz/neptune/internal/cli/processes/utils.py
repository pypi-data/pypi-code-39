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

import enum
import os
import sys

from neptune import job_wrapper
from neptune.internal.common.utils.command_line import split_arguments

class ExecutionCommand(enum.Enum):
    PYTHON = 'python'
    JAVA = 'java'
    R = 'r'
    BASH_COMMAND = 'other'
    JUPYTER_NOTEBOOK = 'jupyter notebook'


def recognize_execution_command(entrypoint):

    if entrypoint.lower().endswith('.jar'):
        return ExecutionCommand.JAVA
    elif entrypoint.lower().endswith('.r'):
        return ExecutionCommand.R
    elif entrypoint.lower().endswith(".py"):
        return ExecutionCommand.PYTHON
    elif entrypoint.lower().endswith(".ipynb"):
        return ExecutionCommand.JUPYTER_NOTEBOOK
    else:
        return ExecutionCommand.BASH_COMMAND


def supports_integration(entrypoint):
    language = recognize_execution_command(entrypoint)
    return language in [
        ExecutionCommand.PYTHON,
        ExecutionCommand.JAVA,
        ExecutionCommand.R,
        ExecutionCommand.JUPYTER_NOTEBOOK
    ]


def supports_notebook_integration(entrypoint):
    language = recognize_execution_command(entrypoint)
    return language in [ExecutionCommand.JUPYTER_NOTEBOOK]


def get_env_or_raise(env):
    if env in os.environ:
        return os.environ[env]
    else:
        raise RuntimeError("Environment variable {0} does not present.".format(env))


def build_process_command(language, entrypoint, args):
    if language == ExecutionCommand.PYTHON:
        return [sys.executable, '-u', job_wrapper.__file__.rstrip('c'), entrypoint] + args
    elif language == ExecutionCommand.JAVA:
        return ['java', '-jar', entrypoint] + args
    elif language == ExecutionCommand.R:
        return ['Rscript', '--vanilla', entrypoint] + args
    elif language == ExecutionCommand.BASH_COMMAND:
        return split_arguments(entrypoint) + args
    elif language == ExecutionCommand.JUPYTER_NOTEBOOK:
        return [
            '/run_notebook.sh',
            get_env_or_raise('NEPTUNE_NOTEBOOK_TOKEN'),
            get_env_or_raise('NEPTUNE_NOTEBOOK_PORT'),
            get_env_or_raise('NEPTUNE_NOTEBOOK_BASE_URL')
        ]
    else:
        raise ValueError('Unsupported programming language: ' + str(language))
