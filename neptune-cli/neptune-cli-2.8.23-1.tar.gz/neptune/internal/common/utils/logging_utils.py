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

import logging
import os
import sys

from neptune.internal.common import NeptuneException
from neptune.internal.common.parsers.common_parameters_configurator import \
    CommonParametersConfigurator
from neptune.internal.common.utils.paths import join_paths


class LogFileOpenError(NeptuneException):

    def __init__(self, path):
        super(LogFileOpenError, self).__init__('Could not open the file {}'.format(path))
        self.path = path


class NeptuneLogger(object):
    LOGS_PATH = 'logs'

    log_filename = None
    log_filepath = None
    formatter = logging.Formatter(
        '%(asctime)s %(name)-8s %(levelname)-8s %(filename)s:%(lineno)s'
        ' - %(funcName)s() %(message)s')
    file_handler = None

    @classmethod
    def create_command_line_logs_file_handler(cls, filepath, mode='w'):
        file_handler = logging.handlers.RotatingFileHandler(filepath, mode=mode)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(cls.formatter)
        return file_handler


class OnlineNeptuneLogger(NeptuneLogger):
    ONLINE_EXECUTION_LOG_FILENAME = 'neptune.log'
    ONLINE_EXECUTION_LOG_FILEPATH = join_paths(os.getcwd(), ONLINE_EXECUTION_LOG_FILENAME)
    ONLINE_EXECUTION_IN_CONTAINER_LOG_FILEPATH = os.path.join('/output', ONLINE_EXECUTION_LOG_FILENAME)

    @classmethod
    def configure_online_logging(cls, cmd_line_args=None, inside_container=False):
        cls.configure_logging(cmd_line_args, inside_container=inside_container)

    @classmethod
    def configure_python_library_logging(cls, cmd_line_args=None):
        cls.configure_logging(cmd_line_args, create_logs_file=False)

    @classmethod
    def configure_logging(cls, cmd_line_args=None, create_logs_file=True, inside_container=False):
        cls.log_filename = cls.ONLINE_EXECUTION_LOG_FILENAME
        if inside_container:
            cls.log_filepath = cls.ONLINE_EXECUTION_IN_CONTAINER_LOG_FILEPATH
        else:
            cls.log_filepath = cls.ONLINE_EXECUTION_LOG_FILEPATH

        if cmd_line_args is not None:
            debug = CommonParametersConfigurator.in_debug_mode(cmd_line_args)
        else:
            debug = 'NEPTUNE_DEBUG' in os.environ

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler(stream=sys.stderr)
        stream_handler.setLevel(logging.WARN)
        stream_handler.setFormatter(cls.formatter)

        root_logger.addHandler(stream_handler)

        pykwalify_logger = logging.getLogger('pykwalify')
        neptune_logger = logging.getLogger('neptune')
        urllib3_logger = logging.getLogger('urllib3')
        swagger_logger = logging.getLogger("swagger_client")
        werkzeug_logger = logging.getLogger('werkzeug')
        raven_logger = logging.getLogger('raven')
        sentry_logger = logging.getLogger('sentry.errors')

        # Remove handlers added internally by Swagger.
        del urllib3_logger.handlers[:]
        del swagger_logger.handlers[:]

        del raven_logger.handlers[:]

        urllib3_logger.setLevel(logging.DEBUG if debug else logging.ERROR)
        neptune_logger.setLevel(logging.DEBUG if debug else logging.INFO)
        pykwalify_logger.setLevel(logging.WARNING)
        werkzeug_logger.setLevel(logging.WARNING)
        sentry_logger.setLevel(logging.CRITICAL)

        if create_logs_file:
            try:
                cls.file_handler = cls.create_command_line_logs_file_handler(
                    cls.log_filepath, mode='a+')
                root_logger.addHandler(cls.file_handler)
            except IOError:
                print('Could not open the file {}'.format(cls.log_filepath))  # pylint:disable=superfluous-parens

    @staticmethod
    def local_neptune_log_file_name(experiment_id):
        return u'neptune-{experiment_id}.log'.format(experiment_id=experiment_id)


# TODO(dzwiedziu) this logger completly ignores debug config
class OfflineNeptuneLogger(NeptuneLogger):
    OFFLINE_EXECUTION_LOG_FILENAME = 'offline_job.log'
    OFFLINE_EXECUTION_LOG_FILEPATH = join_paths(os.getcwd(), OFFLINE_EXECUTION_LOG_FILENAME)

    @classmethod
    def configure_offline_logging(cls):
        cls.log_filename = cls.OFFLINE_EXECUTION_LOG_FILENAME
        cls.log_filepath = cls.OFFLINE_EXECUTION_LOG_FILEPATH

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        job_logger = logging.getLogger('job')
        job_logger.setLevel(logging.INFO)

        try:
            cls.file_handler = logging.FileHandler(cls.log_filepath, mode='w')
            cls.file_handler.setFormatter(logging.Formatter('%(asctime)s  %(message)s'))
            job_logger.addHandler(cls.file_handler)
            root_logger.addHandler(cls.file_handler)
        except IOError:
            job_logger.addHandler(logging.NullHandler())
            root_logger.addHandler(logging.NullHandler())
            raise LogFileOpenError(cls.log_filepath)

    @classmethod
    def configure_python_library_logging(cls):
        cls.configure_offline_logging()


class DevNull(object):
    """
    Fake file-like object.
    """

    def __init__(self):
        pass

    def write(self, buf):
        pass

    def flush(self):
        pass

    def close(self):
        pass
