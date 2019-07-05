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
from deckhand.util.pip import pip_install, pip_config_set, pip_config_unset, pip_config_list

"""Modify pip configurations."""

def configure_dev(arguments=None):
    """Install development pip configuration."""
    logging.info(colored('Installing development pip configuration', 'blue'))
    pip_config_set('global.index_url', 'https://pypi.mindcloud.tools/mindcloud/experimental/+simple/')
    pip_config_set('global.extra_index_url', 'https://pypi.mindcloud.tools/easel/experimental/+simple/\nhttps://pypi.mindcloud.tools/root/pypi/+simple/')
    pip_config_set('search.index', 'https://pypi.mindcloud.tools/easel/experimental/')

def configure_stable(arguments=None):
    """Install stable pip configuration."""
    logging.info(colored('Installing stable pip configuration', 'blue'))
    pip_config_set('global.index_url', 'https://pypi.mindcloud.tools/mindcloud/release/+simple/')
    pip_config_set('global.extra_index_url', 'https://pypi.mindcloud.tools/easel/release/+simple/\nhttps://pypi.mindcloud.tools/root/pypi/+simple/')
    pip_config_set('search.index', 'https://pypi.mindcloud.tools/easel/release/')

def configure_clear(arguments=None):
    """Clear pip configuration."""
    logging.info(colored('Clearing pip configuration', 'blue'))

    pip_config_set('global.index_url', 'https://pypi.python.org/simple/')
    pip_config_set('global.extra_index_url', 'https://pypi.python.org/')
    pip_config_unset('search.index')

def configure_list(arguments=None):
    """Show current pip configuration."""
    logging.info(colored('Displaying pip configuration', 'blue'))

    pip_config_list()
