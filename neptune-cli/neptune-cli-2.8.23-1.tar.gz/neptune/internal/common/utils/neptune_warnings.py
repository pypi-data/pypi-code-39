#
# Copyright (c) 2017, deepsense.io
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

from functools import wraps

import warnings


class JobDeprecationWarning(DeprecationWarning):
    pass


class JobPropertyDeprecationWarning(DeprecationWarning):
    pass


def ignore_deprecated(func):
    """
    This is a decorator which can be used to ignore all
    deprecated warnings for methods, that are called underneath it.
    """

    @wraps(func)
    def new_func(*args, **kwargs):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter('ignore', DeprecationWarning)
            return func(*args, **kwargs)

    return new_func


def neptune_warn(message, warning_type=UserWarning):
    # pylint: disable=unused-argument
    def custom_formatwarning(msg, *args, **kwargs):
        return str(msg) + '\n'

    default_formatwarning = warnings.formatwarning
    warnings.formatwarning = custom_formatwarning
    warnings.warn(message, warning_type)
    warnings.formatwarning = default_formatwarning
