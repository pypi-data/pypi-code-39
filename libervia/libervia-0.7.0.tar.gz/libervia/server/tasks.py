#!/usr/bin/python
# -*- coding: utf-8 -*-

# Libervia: a Salut à Toi frontend
# Copyright (C) 2011-2019 Jérôme Poisson <goffi@goffi.org>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import os.path
from twisted.internet import defer
from twisted.python.procutils import which
from sat.core import exceptions
from sat.core.i18n import _
from libervia.server.constants import Const as C
from collections import OrderedDict
from sat.core.log import getLogger
from sat.tools.common import async_process

log = getLogger(__name__)


class TasksManager(object):
    """Handle tasks of a Libervia site"""
    FILE_EXTS = {u'py'}

    def __init__(self, host, site_resource):
        """
        @param site_resource(LiberviaRootResource): root resource of the site to manage
        """
        self.host = host
        self.resource = site_resource
        self.tasks_dir = os.path.join(self.resource.site_path, C.TASKS_DIR)
        self.tasks = OrderedDict()
        self.parseTasks()
        self._build_path = None
        self._current_task = None

    @property
    def site_path(self):
        return self.resource.site_path

    @property
    def build_path(self):
        """path where generated files will be build for this site"""
        if self._build_path is None:
            self._build_path = self.host.getBuildPath(self.site_name)
        return self._build_path

    def getConfig(self, key, default=None, value_type=None):
        return self.host.getConfig(self.resource, key=key, default=default,
                                   value_type=value_type)

    @property
    def site_name(self):
        return self.resource.site_name

    @property
    def task_data(self):
        return self.tasks[self._current_task][u'data']

    def validateData(self, data):
        """Check values in data"""

        for var, default, allowed in ((u"ON_ERROR", u"stop", (u"continue", u"stop")),
                                      (u"LOG_OUTPUT", True, bool),
                                      (u"WATCH_DIRS", [], list)):
            value = data.setdefault(var, default)
            if isinstance(allowed, type):
                if not isinstance(value, allowed):
                    raise ValueError(
                        _(u"Unexpected value for {var}, {allowed} is expected.")
                        .format(var = var, allowed = allowed))
            else:
                if not value in allowed:
                    raise ValueError(_(u"Unexpected value for {var}: {value}").format(
                        var = var, value = value))

        for var, default, allowed in [[u"ON_ERROR", u"stop", (u"continue", u"stop")]]:
            value = data.setdefault(var, default)
            if not value in allowed:
                raise ValueError(_(u"Unexpected value for {var}: {value}").format(
                    var = var, value = value))

    def parseTasks(self):
        if not os.path.isdir(self.tasks_dir):
            log.debug(_(u"{name} has no task to launch.").format(
                name = self.resource.site_name or u"default site"))
            return
        filenames = os.listdir(self.tasks_dir)
        filenames.sort()
        for filename in filenames:
            filepath = os.path.join(self.tasks_dir, filename)
            if not filename.startswith(u'task_') or not os.path.isfile(filepath):
                continue
            task_name, ext = os.path.splitext(filename)
            task_name = task_name[5:].lower().strip()
            if not task_name:
                continue
            if ext[1:] not in self.FILE_EXTS:
                continue
            if task_name in self.tasks:
                raise exceptions.ConflictError(
                    u"A task with the name [{name}] already exists".format(
                        name=task_name))
            task_data = {u"__name__": "{site_name}.task.{name}".format(
                site_name=self.site_name, name=task_name)}
            self.tasks[task_name] = {
                u'path': filepath,
                u'data': task_data,
            }
            execfile(filepath, task_data)
            # we launch prepare, which is a method used to prepare
            # data at runtime (e.g. set WATCH_DIRS using config)
            try:
                prepare = task_data['prepare']
            except KeyError:
                pass
            else:
                prepare(self)
            self.validateData(task_data)
            if self.host.options['dev_mode']:
                dirs = task_data.get('WATCH_DIRS', [])
                for dir_ in dirs:
                    self.host.files_watcher.watchDir(
                        dir_, auto_add=True, recursive=True,
                        callback=self._autorunTask, task_name=task_name)

    def _autorunTask(self, host, filepath, flags, task_name):
        """Called when an event is received from a watched directory"""
        if flags == ['create']:
            return
        return self.runTask(task_name)

    @defer.inlineCallbacks
    def runTask(self, task_name):
        """Run a single task

        @param task_name(unicode): name of the task to run
        """
        task_value = self.tasks[task_name]
        self._current_task = task_name
        log.info(_(u'== running task "{task_name}" for {site_name} =='.format(
            task_name=task_name, site_name=self.site_name)))
        data = task_value[u'data']
        os.chdir(self.site_path)
        try:
            yield data['start'](self)
        except Exception as e:
            on_error = data[u'ON_ERROR']
            if on_error == u'stop':
                raise e
            elif on_error == u'continue':
                log.warning(_(u'Task "{task_name}" failed for {site_name}: {reason}')
                    .format(task_name=task_name, site_name=self.site_name, reason=e))
            else:
                raise exceptions.InternalError(u"we should never reach this point")
        self._current_task = None

    @defer.inlineCallbacks
    def runTasks(self):
        """Run all the tasks found"""
        old_path = os.getcwd()
        for task_name, task_value in self.tasks.iteritems():
            yield self.runTask(task_name)
        os.chdir(old_path)

    def findCommand(self, name, *args):
        """Find full path of a shell command

        @param name(unicode): name of the command to find
        @param *args(unicode): extra names the command may have
        @return (unicode): full path of the command
        @raise exceptions.NotFound: can't find this command
        """
        names = (name,) + args
        for n in names:
            try:
                cmd_path = which(n)[0].encode('utf-8')
            except IndexError:
                pass
            else:
                return cmd_path
        raise exceptions.NotFound(_(
            u"Can't find {name} command, did you install it?").format(name=name))

    def runCommand(self, command, *args, **kwargs):
        kwargs['verbose'] = self.task_data[u"LOG_OUTPUT"]
        return async_process.CommandProtocol.run(command, *args, **kwargs)
