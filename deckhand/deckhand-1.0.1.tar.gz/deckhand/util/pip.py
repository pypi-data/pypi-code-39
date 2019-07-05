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
import subprocess
import sys

from termcolor import colored

"""Update extra tools."""

def pip_update(package=None):
    """Update pip package."""
    logging.info(colored('Updating ' + package, 'blue'))
    subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", package])

def pip_install(package=None):
    """Update pip package."""
    logging.info(colored('Installing ' + package, 'blue'))
    subprocess.call([sys.executable, "-m", "pip", "install", package])

def pip_config_set(key, value):
    """Update pip configuration."""
    logging.info(colored('Updating ' + key + 'in pip configuration', 'blue'))
    subprocess.call([sys.executable, "-m", "pip", "config", "set", key, value])

def pip_config_unset(key):
    """Update pip configuration."""
    logging.info(colored('Removing ' + key + 'in pip configuration', 'blue'))
    subprocess.call([sys.executable, "-m", "pip", "config", "unset", key])

def pip_config_list():
    """Show pip configuration."""
    logging.info(colored('Calling pip configuration list', 'blue'))
    subprocess.call([sys.executable, "-m", "pip", "config", "list"])
