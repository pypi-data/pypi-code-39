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

"""Manage application logs."""

import os
import logging

from termcolor import colored

def start_logging(verbose=False):
    """
    Configure Python logging.

    :param verbose: A boolean which defines the status of verbose mode.
    :type verbose: boolean
    """
    log_file = os.path.expanduser('~/.oceanstack/deckhand.log')
    
    if not os.path.exists(os.path.dirname(log_file)):
        try:
            os.makedirs(os.path.dirname(log_file))
        except:
            exit(1)

    file_log = logging.FileHandler(log_file)
    file_log.setLevel(logging.DEBUG if (verbose) else logging.INFO)
    file_log.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

    term_log = logging.StreamHandler()
    term_log.setLevel(logging.INFO if (verbose) else logging.WARNING)
    term_log.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

    logging.basicConfig(level=logging.DEBUG, handlers=[file_log, term_log])

    logging.debug(colored('Initialized logger', 'green'))
    if verbose:
        logging.info(colored('Running in verbose mode', 'blue'))
    