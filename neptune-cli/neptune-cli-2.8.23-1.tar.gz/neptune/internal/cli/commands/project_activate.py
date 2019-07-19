# -*- coding: utf-8 -*-
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

from neptune.internal.cli.commands.framework import GenericCommand
from neptune.internal.common.config.neptune_config import get_global_config_file
from neptune.internal.common.config.yaml_utils import SimpleYamlEditor
from neptune.internal.common.models.rich_project import ProjectResolver


class ProjectActivate(GenericCommand):

    name = u'project activate'

    project_activated = u'Project activated: {organization}/{project}.'

    def __init__(self, api_service, organization_name, project_name, profile):
        self.api_service = api_service
        self.organization_name = organization_name
        self.project_name = project_name
        self.profile = profile

    def execute(self, ctx, *args):
        ProjectResolver.resolve(organization_name=self.organization_name,
                                project_name=self.project_name,
                                api_service=self.api_service)
        config_path = get_global_config_file(self.profile)
        self.set_project_in_config_file(self.organization_name, self.project_name, config_path)

        print(self.project_activated.format(
            organization=self.organization_name,
            project=self.project_name))

    @staticmethod
    def set_project_in_config_file(organization_name, project_name, config_path):
        yaml_parser = SimpleYamlEditor()
        yaml_parser.read(config_path)
        yaml_parser.set(u'project', "{}/{}".format(organization_name, project_name))
        yaml_parser.write(config_path)
