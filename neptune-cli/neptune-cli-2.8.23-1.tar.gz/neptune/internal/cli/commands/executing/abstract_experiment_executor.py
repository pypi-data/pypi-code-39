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

from __future__ import print_function

import traceback

from future.builtins import object

from neptune.internal.common import NeptuneException
from neptune.internal.common.sentry import get_sentry_client_instance
from neptune.internal.common.utils.str import to_unicode


class AbstractExperimentExecutor(object):
    ABORTED_RETURN_CODE = 10

    def __init__(self, logger, api_service, local_storage):
        self._logger = logger
        self._api_service = api_service
        self._local_storage = local_storage

    def execute(self, experiment, args):
        try:
            return self._execute(experiment, args)
        except NeptuneException:
            raise
        except SystemExit:
            raise
        except BaseException as exc:
            get_sentry_client_instance(self._local_storage).send_exception()
            self._logger.exception(exc)
            job_traceback = "\n".join(to_unicode(traceback.format_exc()).splitlines())
            self._api_service.mark_experiment_failed(experiment, job_traceback)
            return 1

    def _execute(self, experiment, args):
        raise NotImplementedError()

    def abort(self):
        raise NotImplementedError()
