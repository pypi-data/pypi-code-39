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
from __future__ import print_function

from neptune.internal.cli.commands.utils.git_utils import get_git_info


def send_git_info_if_present(api_service, experiment_ids):
    git_history_params = get_git_info(experiment_ids)
    if git_history_params:
        try:
            api_service.add_experiment_git_history(git_history_params=git_history_params)
        except Exception:
            print(u'Warning: Could not upload git history')
