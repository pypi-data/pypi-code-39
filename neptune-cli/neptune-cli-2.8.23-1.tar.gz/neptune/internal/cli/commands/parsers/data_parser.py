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

from neptune.internal.cli.commands.command_names import CommandNames
from neptune.internal.cli.commands.parsers.abstract_neptune_command_parser import AbstractNeptuneCommandParser
from neptune.internal.cli.commands.parsers.utils.validators import (
    CheckPositionalParamsFirst,
    CombinedArgumentsValidator,
    SubcommandValidator)


class DataParser(AbstractNeptuneCommandParser):

    def __init__(self, parent):
        super(DataParser, self).__init__(parent)
        self.subparsers = self.argparse_parser.add_subparsers(title='Subcommands', dest="subcommand")

        # Required for Python 3.
        # http://bugs.python.org/issue9253#msg186387
        self.subparsers.required = True

        self.data_upload_parser = DataUploadParser(parent=self)
        self.data_list_parser = DataListParser(parent=self)
        self.data_remove_parser = DataRemoveParser(parent=self)
        self.data_download_parser = DataDownloadParser(parent=self)

    @staticmethod
    def command_name():
        return CommandNames.DATA

    def help(self):
        return u'Using this command family you can manage your data on Neptune storage.'

    def get_validator(self):
        return CombinedArgumentsValidator([
            CheckPositionalParamsFirst(),
            SubcommandValidator([
                self.data_upload_parser,
                self.data_list_parser,
                self.data_remove_parser,
                self.data_download_parser
            ])
        ])


class DataDownloadParser(AbstractNeptuneCommandParser):

    @staticmethod
    def command_name():
        return CommandNames.DOWNLOAD

    def help(self):
        return u'Download data from Neptune storage.'

    def _config_positional_args(self):
        super(DataDownloadParser, self)._config_positional_args()
        download_options = self.get_parser().add_argument_group('Download Options')
        self.common_parameters.add_optional_recursive_parameters(download_options,
                                                                 help_msg=u'Download directory recursively.')
        configuration_options = self.get_parser().add_argument_group('Configuration')
        self.common_parameters.add_project_param(configuration_options)

        self.add_argument('path', type=str,
                          help='Path to file or directory on Neptune storage that you want to download.')
        self.add_argument('destination', nargs='?', type=str,
                          help='Destination on your local machine.')


class DataListParser(AbstractNeptuneCommandParser):

    @staticmethod
    def command_name():
        return CommandNames.LS

    def help(self):
        return u'Browse your datasets and results.'

    def _config_positional_args(self):
        super(DataListParser, self)._config_positional_args()
        listing_options = self.get_parser().add_argument_group('Listing Options')
        self.common_parameters.add_optional_recursive_parameters(listing_options,
                                                                 help_msg=u'List directory recursively.')
        configuration_options = self.get_parser().add_argument_group('Configuration')
        self.common_parameters.add_project_param(configuration_options)

        self.add_argument('path', nargs='?', type=str,
                          help='Path to file or directory on Neptune storage that you want to list.')


class DataRemoveParser(AbstractNeptuneCommandParser):

    @staticmethod
    def command_name():
        return CommandNames.RM

    def help(self):
        return u'Remove data from Neptune storage.'

    def _config_positional_args(self):
        super(DataRemoveParser, self)._config_positional_args()
        rm_options = self.get_parser().add_argument_group('Remove Options')
        self.common_parameters.add_optional_recursive_parameters(rm_options,
                                                                 help_msg=u'Remove directory recursively.')
        configuration_options = self.get_parser().add_argument_group('Configuration')
        self.common_parameters.add_project_param(configuration_options)

        self.add_argument('path', type=str,
                          help='Path to file or directory on Neptune storage that you want to remove.')


class DataUploadParser(AbstractNeptuneCommandParser):

    @staticmethod
    def command_name():
        return CommandNames.UPLOAD

    def help(self):
        return u'Upload data to Neptune storage.'

    def _config_positional_args(self):
        super(DataUploadParser, self)._config_positional_args()
        upload_options = self.get_parser().add_argument_group('Upload Options')
        self.common_parameters.add_optional_recursive_parameters(upload_options,
                                                                 help_msg=u'Upload directory recursively.')
        configuration_options = self.get_parser().add_argument_group('Configuration')
        self.common_parameters.add_project_param(configuration_options)

        self.add_argument('path', type=str,
                          help='Path to your local file or directory that you want to upload to Neptune storage.')

        self.add_argument('destination', nargs='?', type=str,
                          help='Destination on Neptune storage.')
