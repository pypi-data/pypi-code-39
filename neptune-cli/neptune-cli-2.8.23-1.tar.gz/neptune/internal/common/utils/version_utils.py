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
import re
from neptune import server


def cli_major_version():
    matched_major_version = re.search(r'(\d+\.\d+)\..*', server.__version__)
    if matched_major_version:
        return matched_major_version.group(1)
    else:
        raise Exception('Wrong CLI version {}'.format(server.__version__))
