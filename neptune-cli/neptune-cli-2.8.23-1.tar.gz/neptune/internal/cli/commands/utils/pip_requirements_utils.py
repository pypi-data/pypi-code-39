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

import os
import subprocess

from neptune.generated.swagger_client import StringParam
from neptune.internal.common.config.job_config import ConfigKeys
from neptune.internal.common.utils.docker import convert_to_docker


def create_string_param(pip_requirements_file):
    if pip_requirements_file is not None:
        return StringParam(
            name='pip-requirements-file',
            value=pip_requirements_file
        )
    else:
        return None


def install_pip_requirements(pip_requirements_file):
    return subprocess.call(["pip", "install", "-r", pip_requirements_file])


def prepare_docker_mount_options_array(pip_requirements_file):
    if pip_requirements_file is not None:
        abs_requirements_file = os.path.abspath(pip_requirements_file)
        docker_path = convert_to_docker(abs_requirements_file)
        return ['-v', '{local}:{docker}'.format(
            local=abs_requirements_file,
            docker=docker_path)]
    else:
        return []


def prepare_in_docker_pip_requirements_option(pip_requirements_file):
    if pip_requirements_file is not None:
        docker_file = convert_to_docker(os.path.abspath(pip_requirements_file))
        return ['--' + ConfigKeys.PIP_REQUIREMENTS_FILE, docker_file]
    else:
        return []
