# -*- coding: utf-8 -*-
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


from __future__ import print_function

from neptune.internal.cli.commands.command_names import CommandNames
from neptune.internal.cli.commands.data.utils.api_wrapper import DataApiWrapper
from neptune.internal.cli.commands.framework import CommandUnsuccessfulError
from neptune.internal.cli.commands.neptune_command import NeptuneCommand
from neptune.internal.common.models.rich_project import ProjectNotFoundError, ProjectResolver

class DataList(NeptuneCommand):

    def __init__(self,
                 config,
                 api_service,
                 organization_name,
                 project_name,
                 path,
                 recursive):
        super(DataList, self).__init__(CommandNames.LS, config, api_service)
        self.organization_name = organization_name
        self.project_name = project_name
        self.path = path
        self.recursive = recursive
        self.config = config

    def __sizeof_fmt(self, num, suffix='B'):
        for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Yi', suffix)

    def run(self, args):
        try:
            project_id = ProjectResolver.resolve(
                api_service=self.api_service,
                organization_name=self.organization_name,
                project_name=self.project_name).id
        except ProjectNotFoundError as exc:
            raise CommandUnsuccessfulError(str(exc))
        ret = DataApiWrapper.execute(self.api_service.ls_data, project_id=project_id,
                                     path_param=self.path, recursive=self.recursive)
        for entry in ret:
            print("%s\t%s\t%s\t%s" % (
                entry.permissions,
                self.__sizeof_fmt(entry.size, ''),
                str(entry.mtime),
                entry.name))
