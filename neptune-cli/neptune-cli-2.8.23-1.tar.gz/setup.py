#!/usr/bin/env python

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

import os
import sys

from setuptools import find_packages, setup

from setup_utils import migrate_tokens, migrate_to_profile


def main():
    sys.path.append('neptune')
    from version import __version__  # nopep8
    root_dir = os.path.dirname(__file__)

    with open(os.path.join(root_dir, "requirements.txt")) as f:
        requirements = [r.strip() for r in f]
        setup(
            name='neptune-cli',
            version=__version__,
            description='Neptune client library',
            author='deepsense.ai',
            author_email='contact@neptune.ml',
            url='https://neptune.ml/',
            long_description="""\
                Neptune client library
            """,
            license='Apache License 2.0',
            install_requires=requirements,
            packages=find_packages(
                include=['neptune*', 'deepsense*'],
                exclude=['neptune.generated.test']),
            py_modules=['setup_utils'],
            package_data={
                'neptune.internal.cli.job_config': ['resources/*.yaml'],
                'neptune.internal.common.api': ['resources/*.json'],
                'neptune.internal.common.config': ['resources/*.ini', 'resources/*.yaml']
            },
            scripts=['scripts/neptune', 'scripts/neptune.bat']
        )
        migrate_tokens()
        migrate_to_profile()


if __name__ == "__main__":
    main()
