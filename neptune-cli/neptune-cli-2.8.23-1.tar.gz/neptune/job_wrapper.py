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
import imp
import os
import sys

from neptune.internal.cli.signal_handlers import setup_subprocess_signal_handlers
from neptune.internal.common.sentry import get_sentry_client_instance


def create_context():
    import neptune
    return neptune.Context()


def integrate_with_third_party_libs(job_globals):
    if 'NEPTUNE_INTEGRATE_WITH_KERAS' in os.environ:
        ctx = create_context()
        ctx.integrate_with_keras()

        from keras import backend as K  # pylint:disable=import-error

    elif 'NEPTUNE_INTEGRATE_WITH_TENSORFLOW' in os.environ:
        ctx = create_context()
        ctx.integrate_with_tensorflow()

    return job_globals


def stub_main_function(job_filepath):
    # We have no idea what may be going on in user's job. It may have a main function and
    # a 'if __name__ == '__main__' guard, but it may also be a pure script which may execute
    # during import (!). It may also have a 'main' function but with different name.
    # Because of all that we cannot just simply try to import main from the
    # job - it may result in script execution or it might be just a wrong assumption.
    #
    # However, tensorflow (at least in 0.12.1 and 1.2.1) allows running 'tf.app.run()'
    # without main argument provided. If it is run that way, it assumes that the job file
    # is the file being directly executed and tries to load 'main' function from the job
    # in a hacky way using 'sys.modules['__main__'].main' statement.
    #
    # Now since this file (job_wrapper.py) is the file being executed by the CLI,
    # 'sys.modules['__main__'].main' leads to main function defined below which is not
    # really the one user wants to have executed by the tensorflow.
    #
    # This is why this stub is needed. If user uses 'tf.app.run()' statement in the job,
    # we can assume that we can safely import main function from the job without any
    # side effects. This is exactly what the tensorflow does.

    # So all we do here is we import 'main' from the job and execute it.

    job_dirpath, job_filename = os.path.split(job_filepath)
    job_modulename = os.path.splitext(job_filename)[0]
    del sys.modules['__main__']
    sys.modules['__main__'] = imp.load_module('__main__', *imp.find_module(job_modulename, [job_dirpath]))


def execute():

    setup_subprocess_signal_handlers()
    # Remove this module name from sys.argv so that executed scripts
    # receives clear argv as it is being run by itself.
    sys.argv = sys.argv[1].split(" ") + sys.argv[2:]

    sys.path = [''] + sys.path

    job_filepath = sys.argv[0]

    job_globals = dict(__name__='__main__')

    if 'NEPTUNE_ONLINE_CONTEXT' in os.environ:
        try:
            integrate_with_third_party_libs(job_globals)
        except Exception as err:
            get_sentry_client_instance().send_exception()
            sys.exit(str(err))

    stub_main_function(job_filepath)


if __name__ == '__main__':
    execute()
