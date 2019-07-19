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

def retry_by_default(decorated):
    return _retry_decorator(decorated, default_with_retries=True)


def no_retry_by_default(decorated):
    return _retry_decorator(decorated, default_with_retries=False)


def _retry_decorator(decorated, default_with_retries):
    def wrapper(*args, **kwargs):
        if u'with_retries' not in kwargs:
            return decorated(*args, **dict(kwargs, with_retries=default_with_retries))
        else:
            return decorated(*args, **kwargs)

    return wrapper
