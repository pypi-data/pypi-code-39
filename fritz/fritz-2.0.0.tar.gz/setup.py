# pylint: disable=missing-docstring
import sys
import os
from setuptools import setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ["--boxed"]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        if isinstance(self.pytest_args, str):
            self.pytest_args = self.pytest_args.split(" ")
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)


dependency_links = [
    "git+https://github.com/apple/coremltools.git#egg=coremltools"
]


tests_require = [
    "astroid >= 2.1.0",
    "pytest >= 4.0.0",
    "pytest-runner",
    "pytest-pylint",
    "pytest-xdist",
    "pytest-cov",
    "requests-mock",
    "pylint",
    "requests_toolbelt",
    "Sphinx",
    "keras",
    "tensorflow <= 1.13.1",
    "coremltools",
    "numpy < 1.17",
]


setup(
    name="fritz",
    version="2.0.0",
    description="Fritz Machine Learning Library.",
    url="https://github.com/fritzlabs/fritz-python",
    author="Fritz Engineering",
    author_email="engineering@fritz.ai",
    license="MIT",
    zip_safe=False,
    packages=find_packages(),
    dependency_links=dependency_links,
    install_requires=[
        "requests",
        "click",
        "click-plugins",
        "termcolor",
        "pbxproj",
    ],
    extras_require={"train": ["keras", "tensorflow"]},
    tests_require=tests_require,
    cmdclass={"test": PyTest},
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={"console_scripts": ["fritz = cli:main"]},
)
