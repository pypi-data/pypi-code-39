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
import argparse

from neptune.internal.cli.commands.command_names import CommandNames
from neptune.internal.cli.commands.parsers.abstract_neptune_command_parser import AbstractNeptuneCommandParser
from neptune.internal.cli.commands.parsers.utils.validators import (
    CombinedArgumentsValidator,
    SubcommandValidator)
from neptune.internal.common.parsers.common_parameters_configurator import CommonParametersConfigurator


class AccountParser(AbstractNeptuneCommandParser):

    def __init__(self, parent):
        super(AccountParser, self).__init__(parent)
        self.subparsers = self.argparse_parser.add_subparsers(title='Subcommands', dest="subcommand")

        # Required for Python 3.
        # http://bugs.python.org/issue9253#msg186387
        self.subparsers.required = True

        self.account_login_parser = AccountLoginParser(parent=self)
        self.account_logout_parser = AccountLogoutParser(parent=self)
        self.account_token_parser = AccountTokenParser(parent=self)

    @staticmethod
    def command_name():
        return CommandNames.ACCOUNT

    def help(self):
        return u'You can log in and out of Neptune using this command family.'

    def get_validator(self):
        return CombinedArgumentsValidator([
            SubcommandValidator([
                self.account_login_parser,
                self.account_logout_parser,
                self.account_token_parser
            ])
        ])


class AccountLoginParser(AbstractNeptuneCommandParser):

    @staticmethod
    def command_name():
        return CommandNames.LOGIN

    def help(self):
        return u'Login to Neptune.'

    def _config_named_args(self):
        self.add_argument('url', nargs='?', type=str, help=argparse.SUPPRESS)
        self.add_open_webbrowser_param()


    def add_open_webbrowser_param(self):
        name = CommonParametersConfigurator.OPEN_WEBBROWSER_PARAMETER
        self.add_argument('--' + name, dest=name, metavar='true|false', nargs='?', const='true', default='true',
                          help='Log in using browser session, otherwise print out a link and await auth code input')


class AccountTokenParser(AbstractNeptuneCommandParser):


    def __init__(self, parent):
        super(AccountTokenParser, self).__init__(parent)
        self.subparsers = self.argparse_parser.add_subparsers(title='Subcommand', dest="subsubcommand")

        # Required for Python 3.
        # http://bugs.python.org/issue9253#msg186387
        self.subparsers.required = True

        self.account_token_get_parser = AccountTokenGetParser(parent=self)

    @staticmethod
    def command_name():
        return CommandNames.API_TOKEN

    def help(self):
        return u'Manage tokens for Neptune API.'

    def get_validator(self):
        return CombinedArgumentsValidator([
            SubcommandValidator([
                self.account_token_get_parser
            ])
        ])


class AccountTokenGetParser(AbstractNeptuneCommandParser):

    @staticmethod
    def command_name():
        return CommandNames.GET

    def help(self):
        return u'Get token for Neptune API.'


class AccountLogoutParser(AbstractNeptuneCommandParser):

    @staticmethod
    def command_name():
        return CommandNames.LOGOUT

    def help(self):
        return u'Logout the CLI from Neptune.'
