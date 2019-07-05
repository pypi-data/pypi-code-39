# Copyright 2019 The Deckhand Authors
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

import logging
from termcolor import colored

"""List extra tools."""

def list_tools(arguments=None):
    """Print list of included tools to console."""
    logging.info(colored('Printing list of tools to the console', 'blue'))
    print(
        'tools:\n',
        '  neuropy'
    )
