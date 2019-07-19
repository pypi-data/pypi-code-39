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
from __future__ import print_function

import collections
import logging
import os
import subprocess
import sys

from future.builtins import object, str
from future.utils import PY3

from neptune.internal.cli.commands.exceptions.enqueue_exceptions import NeptuneFailedToExecute
from neptune.internal.cli.processes import build_process_command, recognize_execution_command
from neptune.internal.cli.processes.aborting import Aborting
from neptune.internal.cli.threads.stream_redirecting_thread import (
    ChannelHandler,
    CroppingHandler,
    FileHandler,
    LogChannelHandler,
    QueueHandler,
    StreamRedirectingThread
)
from neptune.internal.common.utils.str import to_bytestring
from neptune.internal.common.utils.system import IS_WINDOWS

logger = logging.getLogger(__name__)


class JobSpawner(object):

    def spawn(self,
              command,
              config=None,
              cwd=None,
              env=None,
              memorized_stderr_line_count=100,
              stdout_filepath=None,
              stderr_filepath=None,
              channel_factory=None,
              redirect_output_to_console=True,
              online=True):

        cwd = cwd or os.getcwd()

        env = env or os.environ
        env = env.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        if 'PATH' not in env:
            env['PATH'] = ''

        if online:
            env['NEPTUNE_ONLINE_CONTEXT'] = "yes"

        if not PY3 and IS_WINDOWS:

            # In Python 2.7, fetching non-string (non-bytes) env into subprocess.Popen results in
            # `TypeError: environment can only contain strings.` error.
            env = {to_bytestring(k): to_bytestring(v) for k, v in env.items()}

            # FIXME: We should create these commands in unicode way before.
            cmd = []

            for arg in command:
                if not isinstance(arg, str):
                    str(cmd.append(arg.decode('UTF-8')))
                else:
                    cmd.append(arg)

        else:
            cmd = command

        logger.debug("SPAWNING: %s", command)

        try:
            process = self._start_process(cmd=cmd, cwd=cwd, env=env)
        except OSError as e:
            raise NeptuneFailedToExecute(cmd, e)

        stderr_buffer = collections.deque(maxlen=memorized_stderr_line_count)

        stdout_handlers = []
        stderr_handlers = [CroppingHandler(QueueHandler(stderr_buffer))]

        if stdout_filepath:
            try:
                stdout_handlers.append(FileHandler(stdout_filepath))
            except IOError:
                print(u'Could not create {}'.format(stdout_filepath))

        if stderr_filepath:
            try:
                stderr_handlers.append(FileHandler(stderr_filepath))
            except IOError:
                print(u'Could not create {}'.format(stderr_filepath))

        if channel_factory and config:

            log_channels = dict()

            for log_channel in config.log_channels:
                log_channels[log_channel.prefix] = channel_factory.create(log_channel.name)

            if log_channels:
                stdout_handlers.append(LogChannelHandler(log_channels))
                stderr_handlers.append(LogChannelHandler(log_channels))

            if config.stdout_channel:
                stdout_handlers.append(ChannelHandler(channel_factory.get_or_create_stdout_channel()))

            if config.stderr_channel:
                stderr_handlers.append(ChannelHandler(channel_factory.get_or_create_stderr_channel()))

        stdout_thread = StreamRedirectingThread(
            input_stream=process.stdout,
            handlers=stdout_handlers,
            target_stream=sys.stdout if redirect_output_to_console else None)

        stderr_thread = StreamRedirectingThread(
            input_stream=process.stderr,
            handlers=stderr_handlers,
            target_stream=sys.stderr if redirect_output_to_console else None)

        return RunningJob(process, stdout_thread, stderr_thread, stderr_buffer)

    def _start_process(self, cmd, env, cwd):
        logger.info('Starting process')
        logger.info('Command: ' + str(cmd))
        logger.info('OS environment variables staring with \'NEPTUNE\': ' +
                    '; '.join([env_name + ": " + str(env_value)
                               for env_name, env_value in env.items()
                               if env_name.startswith('NEPTUNE')]))
        return subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                env=env,
                                cwd=cwd,
                                bufsize=1)

    @classmethod
    def execute(cls, script, params=None, additional_env=None, **kwargs):

        language = recognize_execution_command(script)
        command = build_process_command(language, script, [] if params is None else params)

        env = os.environ.copy()

        if additional_env is not None:
            env.update(additional_env)

        experiment = cls().spawn(command=command, env=env, online=False, **kwargs)

        return experiment.wait_for_finish()


class RunningJob(object):
    def __init__(self,
                 process,
                 stdout_thread,
                 stderr_thread,
                 stderr_buffer):

        self.process = process
        self._stderr_buffer = stderr_buffer
        self._stdout_thread = stdout_thread
        self._stderr_thread = stderr_thread

        self._stdout_thread.start()
        self._stderr_thread.start()

    def wait_for_finish(self):
        """
        This method waits for experiment execution and for threads that are responsible for a realtime
        output redirection from the experiment to sys.stdout and stdout/stderr files.
        :return: Return code from the experiment process.
        """
        while True:
            try:
                return_code = self.process.wait()
                self._cleanup()
                return return_code
            except KeyboardInterrupt:
                logger.debug("Received SIGINT. Killing subprocess.")
                self.process.kill()

    def abort(self):
        Aborting(self.process.pid).abort()
        self._cleanup()

    def _cleanup(self):
        # Don't interrupt stdout/stderr handlers here.
        # They should terminate right after they finish
        # processing buffered subprocess' output.
        # Better just join and wait for them to terminate.

        logger.debug("Waiting for stream redirecting threads to terminate.")
        self._stdout_thread.join()
        self._stderr_thread.join()

    def memorized_stderr(self):
        joined_stderr = '\n'.join(self._stderr_buffer)
        return joined_stderr + '\n' if joined_stderr else joined_stderr
