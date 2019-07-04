# Copyright (c) 2019 AT&T Intellectual Property.
# Copyright (c) 2018-2019 Nokia.
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

"""Setup file for mdclogpy library."""

from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='mdclogpy',
      version='1.0',
      description='Structured logging library with Mapped Diagnostic Context',
      long_description=readme(),
      long_description_content_type="text/markdown",
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      url='https://gerrit.o-ran-sc.org/r/admin/repos/com/pylog',
      author_email='kturunen@nokia.com',
      license='Apache Software License',
      packages=['mdclogpy'],
      zip_safe=False)