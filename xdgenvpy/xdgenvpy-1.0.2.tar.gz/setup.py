# /usr/bin/env python3

from os.path import dirname
from os.path import exists
from os.path import join
from os.path import realpath
from shutil import rmtree

from setuptools import Command
from setuptools import find_packages
from setuptools import setup

PROJECT_NAME = 'xdgenvpy'
PROJECT_VERSION = '1.0.2'


def get_repo_file(*args):
    """
    Joins all the arguments into a single string that will be normalized into an
    absolute file path.  Essentially the path will point to a file within this
    repository.

    :param args: Names to join that make up a relative file path.

    :rtype: str`
    :return: The absolute path to a file within this repository.
    """
    return join(dirname(realpath(__file__)), *args)


def read_file(filename):
    """
    Reads the specified file and returns the full contents as a single string.

    :param filename: The file to read.

    :rtype: str
    :return: The full contents of the specified file.
    """
    with open(filename) as f:
        return ''.join(f.readlines())


def get_xdgenvpy_packages():
    """
    Finds all packages within this project and only returns the production ready
    ones.  Meaning, test packages will not be included.

    :rtype tuple
    :return: A sequence of package names that will be built into the file
            distribution.
    """
    packages = find_packages()
    packages = [p for p in packages if not p.endswith('_test')]
    return tuple(packages)


class CleanCommand(Command):
    """
    A custom clean command that removes any intermediate build directories.
    """

    description = 'Custom clean command that forcefully removes build, dist,' \
                  ' and other similar directories.'
    user_options = []

    def __init__(self, *args, **kwargs):
        """Initialized the custom clean command with a list of directories."""
        super(CleanCommand, self).__init__(*args, **kwargs)
        self.clean_dirs = tuple([
            'build',
            PROJECT_NAME + '.egg-info',
            'dist',
        ])
        proj_dir = dirname(realpath(__file__))
        self.clean_dirs = [join(proj_dir, d) for d in self.clean_dirs]
        self.clean_dirs = [d for d in self.clean_dirs if exists(d)]

    def initialize_options(self):
        """Unused, but required when implementing :class:`Command`."""
        pass

    def finalize_options(self):
        """Unused, but required when implementing :class:`Command`."""
        pass

    def run(self):
        """Performs the actual removal of the intermediate build directories."""
        for d in self.clean_dirs:
            print(f'removing {d}')
            rmtree(d)


setup(name=PROJECT_NAME,
      version=PROJECT_VERSION,

      author='Mike Durso',
      author_email='rbprogrammer@gmail.com',
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: MacOS',
          'Operating System :: POSIX',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Utilities',
      ],
      cmdclass={'clean': CleanCommand},
      install_requires=(),
      description='Another XDG Base Directory Specification utility.',
      long_description=read_file(get_repo_file('README.md')),
      long_description_content_type="text/markdown",
      packages=get_xdgenvpy_packages(),
      scripts=('bin/xdg-env',),
      tests_require=(),
      url='https://gitlab.com/rbprogrammer/xdgenvpy',
      )
