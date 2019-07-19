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

import os

from neptune.internal.cli.commands.command_names import CommandNames
from neptune.internal.cli.commands.exceptions.data_exceptions import (
    NeptuneCreateFileFromDirectoryException,
    NeptuneNonRecursiveDirectoryUpload,
    NeptuneCannotOverrideFileWithDirectory,
    NeptuneCannotOverrideDirectory,
    NeptuneCannotOverrideFile
)
from neptune.internal.cli.commands.framework import CommandUnsuccessfulError
from neptune.internal.cli.commands.neptune_command import NeptuneCommand
from neptune.internal.cli.storage.populate_storage_utils import (
    collect_files,
    CopyProgressBar)
from neptune.internal.cli.storage.upload_storage_utils import upload_to_storage
from neptune.internal.common.models.rich_project import ProjectNotFoundError, ProjectResolver
from neptune.internal.common.utils.paths import normalize_path, join_paths, getcwd

class DataUpload(NeptuneCommand):
    DIRECTORY = u'dir'
    FILE = u'file'

    def __init__(self,
                 config,
                 api_service,
                 organization_name,
                 project_name,
                 path,
                 destination,
                 recursive=False):
        super(DataUpload, self).__init__(CommandNames.UPLOAD, config, api_service)
        self.organization_name = organization_name
        self.project_name = project_name
        self.path = normalize_path(path.rstrip(os.sep))
        self.recursive = recursive
        self.destination = destination
        self.config = config

    @staticmethod
    def _replace_last_occurence(path, to_replace, replacement):
        path_splitted = path.split(to_replace)
        return to_replace.join(path_splitted[:-1]) + replacement + path_splitted[-1]

    def run(self, args):
        try:
            project = ProjectResolver.resolve(
                api_service=self.api_service,
                organization_name=self.organization_name,
                project_name=self.project_name)
        except ProjectNotFoundError as exc:
            raise CommandUnsuccessfulError(str(exc))


        if not self.recursive:
            normpath = join_paths(getcwd(), self.path)
            if os.path.isdir(normpath) and len(os.listdir(normpath)) > 0:
                raise NeptuneNonRecursiveDirectoryUpload(self.path)

        files_list, size, empty_dir_list = collect_files(p=self.path, description=u"data")

        src = join_paths(getcwd(), self.path)
        copy_progress_bar = CopyProgressBar(size, u"Uploading data to server")
        path_last_component = src.split(os.sep)[-1]

        if self.destination is not None:
            (dst_ls_len, dst_type) = self._get_dst_ls_with_file_type(project.id, self.destination)
            if self.destination.endswith(os.sep) and \
                    os.path.isfile(join_paths(getcwd(), self.path)):
                raise NeptuneCreateFileFromDirectoryException(self.destination)

            dst = self.destination.rstrip(os.sep)

            if dst_ls_len >= 0:
                if dst_type == self.FILE and os.path.isdir(src):
                    raise NeptuneCannotOverrideFileWithDirectory(self.path, self.destination)
                empty_dest = dst + os.sep + path_last_component
                if dst_type == self.DIRECTORY:
                    file_dest = dst + os.sep + path_last_component
                else:
                    file_dest = dst
                files_list = [(x, self._replace_last_occurence(x, src, file_dest))
                              for x, _ in files_list]
                empty_dir_list = [(x, self._replace_last_occurence(x, src, empty_dest))
                                  for x, _ in empty_dir_list]
            else:
                files_list = [(x, self._replace_last_occurence(x, src, dst)) for x, _ in files_list]
                empty_dir_list = [(x, self._replace_last_occurence(x, src, dst)) for x, _ in empty_dir_list]
        else:
            (dst_ls_len, dst_type) = self._get_dst_ls_with_file_type(project.id, self.path.split(os.sep)[-1])

            if dst_ls_len >= 0:
                dst_path = self.path.split(os.sep)[-1]
                if dst_type == self.FILE:
                    if os.path.isdir(src):
                        raise NeptuneCannotOverrideFileWithDirectory(self.path, dst_path)
                    raise NeptuneCannotOverrideFile(self.path, dst_path)
                raise NeptuneCannotOverrideDirectory(self.path, dst_path)

            if not os.path.isfile(src):
                files_list = [(x,
                               x[(x.find(src) + len(os.sep.join(src.split(os.sep)[:-1]))):]
                               if os.sep in src else x[(x.find(src) + len(src))])
                              for x, _ in files_list]
                files_list = [(x, y[1:] if y.startswith(os.sep) else y) for x, y in files_list]
                empty_dir_list = [(x,
                                   x[(x.find(src) + len(os.sep.join(src.split(os.sep)[:-1]))):]
                                   if os.sep in src else x[(x.find(src) + len(src))])
                                  for x, _ in empty_dir_list]
                empty_dir_list = [(x, y[1:] if y.startswith(os.sep) else y) for x, y in empty_dir_list]
            else:
                files_list = [(x, y) for x, y in files_list]
                empty_dir_list = [(x, y) for x, y in empty_dir_list]

        upload_to_storage(files_list=files_list,
                          dir_list=empty_dir_list,
                          upload_api_fun=self.api_service.upload_data,
                          upload_tarstream_api_fun=self.api_service.upload_data_as_tarstream,
                          callback=copy_progress_bar.update,
                          project_id=project.id)

        copy_progress_bar.finalize()

    def _get_dst_ls_with_file_type(self, project_id, dst_path):
        try:
            ls_data = self.api_service.ls_data(project_id=project_id, path_param=dst_path, recursive=False)
            file_type = self.DIRECTORY
            if len(ls_data) == 1 and ls_data[0].file_type == self.FILE:
                dst_path_parent = '.' if os.sep not in dst_path else join_paths(dst_path.split(os.sep)[:-1])
                ls_data_parent = self.api_service.ls_data(project_id=project_id,
                                                          path_param=dst_path_parent,
                                                          recursive=False)
                filtered_ls_data_parent = [x for x in ls_data_parent if x.name == dst_path.split(os.sep)[-1]]
                if len(filtered_ls_data_parent) == 1 and filtered_ls_data_parent[0].file_type == self.FILE:
                    file_type = self.FILE
            return len(ls_data), file_type
        except Exception as _:
            return -1, None
