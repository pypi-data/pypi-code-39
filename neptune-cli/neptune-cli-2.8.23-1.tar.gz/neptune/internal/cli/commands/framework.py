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

import abc

import collections
from future.builtins import str
from future.utils import with_metaclass

from neptune.internal.cli.commands.neptune_command import OK_EXIT_CODE
from neptune.internal.common import NeptuneException
from neptune.internal.common.api.exceptions import NeptuneServerResponseErrorException

EXIT_CODE_UNSUCCESSFUL = 1


class Command(object):

    exit_code = OK_EXIT_CODE

    def abort(self):
        pass


class GenericCommand(with_metaclass(abc.ABCMeta), object):

    exit_code = OK_EXIT_CODE

    @abc.abstractmethod
    def execute(self, ctx, *args):
        raise NotImplementedError

    def abort(self):
        pass


class NeptuneCommandAdapter(object):
    ''' Adapter to make GenericCommand classes compatible with INeptuneCommand interface. '''

    def __init__(self, command, ctx):
        self.command = command
        self.ctx = ctx

    def run(self, *_):
        self.command.execute(self.ctx)

    @property
    def name(self):
        return self.command.name

    @property
    def exit_code(self):
        return self.command.exit_code

    def abort(self):
        self.command.abort()


class HandleCommandErrors(GenericCommand):

    ''' Catch CommandUnsuccessfulError exceptions and print them and care of the exit code. '''

    def __init__(self, command):
        self.command = command
        self._exit_code = OK_EXIT_CODE

    def execute(self, ctx, *args):

        try:
            self.command.execute(ctx, *args)
        except CommandUnsuccessfulError as error:
            self._exit_code = error.exit_code
            print(str(error))
        except NeptuneServerResponseErrorException as e:
            self._exit_code = EXIT_CODE_UNSUCCESSFUL
            if e.status == 400:
                print(e.response_message)
            elif e.status == 401 or e.status == 403:
                print(u'neptune: Not authorized')
            else:
                raise e
        except:
            self._exit_code = EXIT_CODE_UNSUCCESSFUL
            raise

    @property
    def name(self):
        return self.command.name

    @property
    def exit_code(self):
        return self._exit_code


class CommandUnsuccessfulError(NeptuneException):
    ''' Raise this exception in commands. '''

    def __init__(self, message, exit_code=EXIT_CODE_UNSUCCESSFUL):
        super(CommandUnsuccessfulError, self).__init__(message)
        self.exit_code = exit_code


CommandExecutionContext = collections.namedtuple(
    'CommandExecutionContext',
    ['api_service', 'config', 'session'])
