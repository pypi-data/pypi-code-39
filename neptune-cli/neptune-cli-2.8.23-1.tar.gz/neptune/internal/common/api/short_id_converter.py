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
from neptune.internal.common import NeptuneException


class ShortIdConverter(object):
    def __init__(self, api_service):
        self._api_service = api_service

    def convert_to_uuids(self, project_id, short_ids, **get_experiment_filters):
        params = self._merge_dicts({
            u'projectId': project_id,
        }, get_experiment_filters)
        experiments_in_project = self._api_service.get_experiments(params)

        experiments_by_short_id = {exp[u'shortId']: exp for exp in experiments_in_project[u'entries']}
        experiments_matching_short_ids = [experiments_by_short_id.get(short_id) for short_id in short_ids]

        if None not in experiments_matching_short_ids:
            return dict((exp[u'id'], exp[u'shortId']) for exp in experiments_matching_short_ids)
        else:
            non_existent_short_ids = [
                short_id
                for (short_id, experiment)
                in zip(short_ids, experiments_matching_short_ids)
                if experiment is None
            ]
            raise NeptuneException('Experiment {} not found.'.format(', '.join(non_existent_short_ids)))

    @staticmethod
    def _merge_dicts(d1, d2):
        result = d1.copy()
        result.update(d2)
        return result
