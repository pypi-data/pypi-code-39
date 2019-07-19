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

import os
import socket
import sys
import webbrowser

from subprocess import check_output, STDOUT


class Browser(object):

    def open(self, url):
        raise NotImplementedError


class SilentBrowser(Browser):

    def open(self, url):
        check_output([sys.executable, '-m', 'webbrowser', url], stderr=STDOUT)


class WebBrowser(Browser):

    def open(self, url):

        """ Open given url and supress browser's stdout.

        Supressing stdout is required to avoid `Created new window in existing browser session.`
        message showing up in the terminal.

        http://stackoverflow.com/a/2323563
        """

        fd = sys.stdout.fileno()

        savout = os.dup(fd)
        os.close(fd)
        os.open(os.devnull, os.O_RDWR)
        try:
            webbrowser.open(url)
        finally:
            os.dup2(savout, fd)


class NullBrowser(Browser):

    def open(self, url):
        pass


def is_webbrowser_operable():

    try:
        webbrowser.get()
    except webbrowser.Error:
        return False

    return True


def is_able_to_open_socket():

    try:
        s = socket.socket()
        s.bind(('localhost', 0))
    except socket.error:
        return False
    else:
        return True
    finally:
        s.close()
