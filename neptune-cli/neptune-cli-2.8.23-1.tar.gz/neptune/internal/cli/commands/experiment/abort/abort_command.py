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

from neptune.internal.cli.commands.command_names import CommandNames
from neptune.internal.cli.commands.framework import CommandUnsuccessfulError
from neptune.internal.cli.commands.neptune_command import MethodNames, NeptuneCommand
from neptune.internal.common.models.rich_project import ProjectNotFoundError, ProjectResolver


class NeptuneExperimentAbort(NeptuneCommand):
    ABORT_GET_EXPERIMENTS_FILTERS = {u'states': [u'creating', u'waiting', u'initializing', u'running']}

    def __init__(self, config, api_service, short_id_converter, organization_name, project_name):
        super(NeptuneExperimentAbort, self).__init__(CommandNames.ABORT, config, api_service)
        self._method_names = MethodNames('Abort', 'Aborting', 'Aborted')
        self._short_id_converter = short_id_converter
        self._organization_name = organization_name
        self._project_name = project_name

    def run(self, args):
        try:
            project = ProjectResolver.resolve(
                api_service=self.api_service,
                organization_name=self._organization_name,
                project_name=self._project_name)
        except ProjectNotFoundError as exc:
            raise CommandUnsuccessfulError(str(exc))

        experiment_short_ids = args.known_args.experiment_ids
        experiments_uuids = self._short_id_converter.convert_to_uuids(project.id, experiment_short_ids,
                                                                      **self.ABORT_GET_EXPERIMENTS_FILTERS)

        batch_results = self.api_service.abort_experiments(list(experiments_uuids))

        ok_flag = all(not result.error for result in batch_results)
        if not ok_flag:
            self._exit_code = self.UNKNOWN_EXCEPTION_EXIT_CODE

        print(self.prepare_output(args, batch_results, experiments_uuids))

    def prepare_output(self, args, batch_results, experiments_uuids):
        self.logger.debug(
            "%s experiments for arguments: %s", self._method_names.active, args.raw_args)
        return self._prepare_batch_report_output(batch_results, experiments_uuids)

    def _prepare_batch_report_output(self, batch_results, experiments_uuids):
        """
        Formats list of BatchEntityUpdateResult into printable output

        :param batch_results: list of BatchEntityUpdateResult
        :return: formatted_output
        """
        row_msg = u"{id}    {status}"
        results_prepared = []
        ok_counter = 0
        error_counter = 0
        for result in batch_results:
            if not result.error:
                status = u"OK"
                ok_counter += 1
            else:
                status = "ERROR: " + result.error.message
                error_counter += 1
            results_prepared.append(row_msg.format(id=experiments_uuids.get(result.experiment_id), status=status))

        output = u"{method_name_doing}:\n{reports}\n{method_name_done} {oks} experiments." \
            .format(
                method_name_doing=self._method_names.active,
                method_name_done=self._method_names.done,
                reports="\n".join(results_prepared),
                oks=ok_counter
            )
        if error_counter > 0:
            output += u" Failed to {method_name} {error_nr} experiments.".format(
                error_nr=error_counter,
                method_name=self._method_names.name.lower())

        return output
