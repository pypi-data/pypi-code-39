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

import io
import os

from neptune.internal.cli.commands.command_names import CommandNames
from neptune.internal.cli.commands.data.utils.api_wrapper import DataApiWrapper
from neptune.internal.cli.commands.exceptions.data_exceptions import NeptuneNonRecursiveDirectoryDownload, \
    InsufficientFundsError
from neptune.internal.cli.commands.framework import CommandUnsuccessfulError
from neptune.internal.cli.commands.neptune_command import NeptuneCommand
from neptune.internal.cli.commands.utils.payments_utils import PaymentsUtils
from neptune.internal.cli.storage.populate_storage_utils import CopyProgressBar
from neptune.internal.common.models.rich_project import ProjectNotFoundError, ProjectResolver


class DataDownload(NeptuneCommand):

    def __init__(self,
                 config,
                 api_service,
                 session,
                 organization_name,
                 project_name,
                 path,
                 destination,
                 recursive=False
                ):
        super(DataDownload, self).__init__(CommandNames.DOWNLOAD, config, api_service)
        self.organization_name = organization_name
        self.project_name = project_name
        self.path = path
        self.session = session
        self.destination = destination
        self.config = config
        self.recursive = recursive

    def _walk(self, path='', dst='.', dry_run=0):
        file_entries = self.api_service.ls_path(path)
        if not os.path.exists(dst) and dry_run:
            os.makedirs(dst)
        for entry in file_entries:
            if entry.file_type == u"directory":
                for f in self._walk(path + entry.name + '/', dst + u'/' + entry.name, dry_run):
                    yield f
            if entry.file_type == u"file":
                yield path, entry.name, entry.size

    def _download_file(self, path, destination, copy_progress_bar=None):
        filename = os.path.basename(path)
        file_path = os.path.join(destination, filename)

        if os.path.exists(file_path) and self.destination is None:
            print(u"Cannot download {}: File already exists".format(path))
            return

        if not os.path.exists(destination):
            os.makedirs(destination)

        try:
            response = self.api_service.download_path(self.session, self.config.http_url, path)
        except InsufficientFundsError:
            PaymentsUtils(self.config).print_insufficient_funds()
            raise

        info = (filename[:16] + '..') if len(filename) > 16 else filename.ljust(16)
        copy_progress_bar.set_description(u"Downloading " + info)

        with io.open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024 * 10):
                f.write(chunk)
                copy_progress_bar.update(len(chunk))

    def _download_dir(self, path, destination, dry_run=0, copy_progress_bar=None):
        total_size = 0
        for directory, filename, size in self._walk(path, destination, dry_run):
            total_size += size
            if not dry_run:
                self._download_file(u"{}{}".format(directory, filename),
                                    u"{}/{}".format(destination, directory[len(path):]),
                                    copy_progress_bar)
        return total_size

    def run(self, args):
        try:
            project = ProjectResolver.resolve(
                api_service=self.api_service,
                organization_name=self.organization_name,
                project_name=self.project_name)
        except ProjectNotFoundError as exc:
            raise CommandUnsuccessfulError(str(exc))
        ret = DataApiWrapper.execute(self.api_service.ls_data, project_id=project.id, path_param=self.path,
                                     recursive=False)
        prefix = u"/uploads"
        if self.path.startswith("/"):
            prefix = ""

        destination = self.destination or u"."
        if len(ret) == 1 and ret[0].permissions[0] != u'd':
            path = u"/{}/{}{}/{}".format(project.organization_id,
                                         project.project_key,
                                         prefix,
                                         self.path)
            copy_progress_bar = CopyProgressBar(ret[0].size,
                                                u"Downloading file from server")
            try:
                self._download_file(path, destination, copy_progress_bar)
            finally:
                copy_progress_bar.finalize()
        else:
            if not self.recursive:
                raise NeptuneNonRecursiveDirectoryDownload(self.path)
            path = u"/{}/{}{}/{}/".format(project.organization_id,
                                          project.project_key,
                                          prefix,
                                          self.path)
            dst = os.path.join(destination, self.path.rstrip(u'/').split(u'/')[-1])
            size = self._download_dir(path, dst, 1)
            copy_progress_bar = CopyProgressBar(size, u"Downloading files from server")
            try:
                self._download_dir(path, dst, 0, copy_progress_bar)
            finally:
                copy_progress_bar.finalize()
