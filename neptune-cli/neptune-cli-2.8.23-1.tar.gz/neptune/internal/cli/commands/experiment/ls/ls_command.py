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
from __future__ import print_function

from future.utils import raise_from

from neptune.internal.cli.commands.experiment.ls.exceptions import EntitySourceError
from neptune.internal.cli.commands.experiment.ls.formatting import decamelized
from neptune.internal.cli.commands.experiment.ls.http import paginated_http_request
from neptune.internal.cli.commands.framework import CommandUnsuccessfulError, GenericCommand
from neptune.internal.common.models.rich_project import ProjectNotFoundError, ProjectResolver


class NeptuneExperimentLs(GenericCommand):
    name = u'experiment list'

    error_message = u'There was an error during attempt to list experiments.'

    page_size = 100

    def __init__(self, row_factory):
        self.row_factory = row_factory

    def execute(self, ctx, *args):
        try:
            project = ProjectResolver.resolve(
                api_service=ctx.api_service,
                organization_name=ctx.config.organization_name,
                project_name=ctx.config.project_name)
        except ProjectNotFoundError as exc:
            raise CommandUnsuccessfulError(str(exc))

        params = {
            u'projectId': project.id,
            u'states': [u'creating', u'waiting', u'initializing', u'running', u'cleaning']
        }

        entries = paginated_http_request(
            request_call=ctx.api_service.get_experiments, params=params, page_size=self.page_size)

        try:
            for exp in self.row_factory.format(decamelized(entries)):
                print(exp)
        except EntitySourceError as error:
            raise_from(CommandUnsuccessfulError(self.error_message), error)
