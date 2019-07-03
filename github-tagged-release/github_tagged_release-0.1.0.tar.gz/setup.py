import os
import sys

import setuptools
from setuptools.command.install import install

from github_release import VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setuptools.setup(
    name="github_tagged_release",
    version=VERSION,
    author="Nikolai R Kristiansen",
    author_email="nikolaik@gmail.com",
    license="MIT",
    description="GitHub changelogs using tags for your CircleCI workflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/convertelligence/github_tagged_release",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.18.4',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    cmdclass={
        'verify': VerifyVersionCommand,
    },
    entry_points={
        'console_scripts': ['github_tagged_release=github_release:main'],
    }
)
