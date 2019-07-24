# Copyright 2019 Mike Shoup
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

from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
# Get contents of README
with open(path.join(this_directory, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

# Get current version number
version = {}
with open(path.join(this_directory, "src/humulus/_version.py")) as f:
    exec(f.read(), version)

install_requires = [
    "Flask==1.0.3",
    "Flask-WTF==0.14.2",
    "simplejson==3.16.0",
    "python-slugify==3.0.2",
    "cloudant==2.12.0",
]

setup(
    name="humulus",
    version=version["__version__"],
    url="https://github.com/shouptech/humulus",
    author="Mike Shoup",
    author_email="mike@shoup.io",
    description="Humulus is a beer recipe builder.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=install_requires + ["pytest-runner"],
    tests_require=["pytest"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
)
