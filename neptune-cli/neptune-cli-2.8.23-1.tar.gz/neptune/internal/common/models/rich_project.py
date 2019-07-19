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

from neptune.internal.common import NeptuneException
from neptune.internal.common.api.exceptions import NeptuneEntityNotFoundException, NeptuneServerResponseErrorException


class ProjectNotFoundError(NeptuneException):
    pass


class ProjectUnauthorizedError(NeptuneException):
    pass


class ProjectResolver(object):
    project_not_defined = u"Project is not defined."
    project_not_found = u"Project '{}/{}' not found."
    project_unauthorized = u"Unauthorized to access project {}/{}."
    multiple_project_info = u"You have access to more than one project.\n"
    no_project_set = u"Please set the project name using either config file" \
                     u" or --project argument."
    deprecated_project_key_in_default_organization = u"Warning: 'project: {project_key}' definition is deprecated, " \
                                                     u"use 'project: {project_name}' instead."
    deprecated_project_key_in_specified_organization = u"Warning: 'project: {project_key}' definition is deprecated, " \
                                                       u"use 'project: 'project: {organization_name}/{project_name}' " \
                                                       u"instead."

    def __init__(self):
        pass

    @classmethod
    def resolve(cls, api_service, organization_name, project_name):
        project = ProjectResolver.__get_project(api_service, organization_name, project_name)
        ProjectResolver.__print_project_info(project)
        return project

    @classmethod
    def __get_project(cls, api_service, organization_name, project_name):
        if project_name:
            try:
                return api_service.get_project_by_name(organization_name=organization_name,
                                                       project_name=project_name)
            except NeptuneEntityNotFoundException:
                try:
                    project = api_service.guess_project(project_key=project_name)
                    if organization_name == project.organization_name:
                        print(ProjectResolver.deprecated_project_key_in_default_organization
                              .format(project_key=project.project_key,
                                      project_name=project.name))
                    else:
                        print(ProjectResolver.deprecated_project_key_in_specified_organization
                              .format(project_key=project.project_key,
                                      project_name=project.name,
                                      organization_name=project.organization_name))
                    return project
                except:
                    raise ProjectNotFoundError(cls.project_not_found.format(organization_name, project_name))
            except NeptuneServerResponseErrorException as e:
                if e.status == 401:
                    raise ProjectUnauthorizedError(cls.project_unauthorized.format(organization_name, project_name))
                else:
                    raise
        else:
            try:
                return api_service.guess_project()
            except:
                raise ProjectNotFoundError(cls.multiple_project_info + cls.no_project_set)

    @classmethod
    def __print_project_info(cls, project):
        if project is None:
            raise ProjectNotFoundError(ProjectResolver.project_not_defined + u'\n' + ProjectResolver.no_project_set)
        print(u"Current project: {}/{}".format(project.organization_name, project.name))
