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


from future.builtins import object


class CommandNames(object):
    # Neptune 3.0 commands
    EXPERIMENT = u'experiment'
    EX = u'ex'
    DATA = u'data'
    PROJECT = u'project'
    ACCOUNT = u'account'

    EXPERIMENT_CMDS = [EX, EXPERIMENT]

    # Neptune 3.0 subcommands

    # general purpose
    LIST = u'list'

    # experiment
    RUN = u'run'
    SEND = u'send'
    SEND_NOTEBOOK = u'send-notebook'
    ABORT = u'abort'

    # data
    LS = u'ls'
    UPLOAD = u'upload'
    DOWNLOAD = u'download'
    RM = u'rm'

    # project
    ACTIVATE = u'activate'

    # account
    LOGIN = u'login'
    LOGOUT = u'logout'
    API_TOKEN = u'api-token'

    # api-token
    GET = u'get'

    # Old command names
    EXEC = u'exec'
