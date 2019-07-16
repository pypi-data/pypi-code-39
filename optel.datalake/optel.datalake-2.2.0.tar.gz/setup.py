#!/usr/bin/python3
# coding: utf8


"""This scripts lays building blocks for development tooling."""


from distutils.version import LooseVersion
import email.utils
import errno
import fnmatch
import os
import platform
import setuptools
import shutil
from urllib.parse import urlparse

__all__ = (
    'ProjectMetadata',
    'Clean',
)


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

PYTHON_VERSION = platform.python_version_tuple()

DEFAULT_VERSION = '0.1'


class ProjectMetadata(object):
    """
    This hold distribution information primarily used at build time.

    Properties of this class are intended to roughly fit the
    `metadata
    <https://docs.python.org/2/distutils/setupscript.html#additional-meta-data>`_
    expected by keyword arguments by the :func:`setuptools.setup` function.

    Since we use *setuptools*, you may wish to read about
    `new and changed setup keywords
    <http://setuptools.readthedocs.io/en/latest/setuptools.html?highlight=keywords#new-and-changed-setup-keywords>`.
    """

    def __init__(self):
        """Initialize some cached or internal storage of data."""
        self._version = None

    @property
    def name(self):
        """
        Name of the package.

        Note:
            This field is required by :func:`setuptools.setup`

        Returns:
             str: A short string
        """
        value = 'optel.datalake'
        return self._ensure_short_string(value)

    @property
    def description(self):
        """
        Short, summary description of the package.

        Returns:
             str: A short string
        """
        value = 'Common tools used in the data refinery'
        return self._ensure_short_string(value)

    @property
    def long_description(self):
        """
        Returns:
             str: A string
        """
        return open('README.rst').read()

    @property
    def version(self):
        """
        Version of this release.

        Note:
            This field is required by :func:`setuptools.setup`

        Returns:
             str: A short string
        """
        if self._version is None:
            try:
                self._version = str(LooseVersion(read_file('VERSION'))).strip()
            except (OSError, IOError):
                self._version = str(LooseVersion(os.getenv('_VERSION',
                                                           DEFAULT_VERSION)))

        return self._ensure_short_string(self._version)

    @property
    def url(self):
        """
        Home page for the package.

        Note:
            This field is required by :func:`setuptools.setup`

        Returns:
             str: A URL
        """
        value = 'https://www.optelgroup.com/'
        return self._ensure_url(value)

    @property
    def download_url(self):
        """
        Location where the package may be downloaded.

        Returns:
             str: A URL
        """
        value = '{!s}/repository/master/archive.tar.gz'.format(self.url)
        return self._ensure_url(value)

    @property
    def license(self):
        """
        License for the package.

        Note:
            The "license" field is a text indicating the license
            covering the package where the license is not a selection
            from the "License" Trove classifiers. See the :attr:`~classifiers`
            field. Notice that there's a "licence" distribution option
            which is deprecated but still acts as an alias for license.

        Returns:
             str: A short string
        """
        value = 'LGPL'
        return self._ensure_short_string(value)

    @property
    def keywords(self):
        """
        A whitespace-separated list of keywords about this project.

        I have been able to find documentation about this parameter but it
        is clearly used in the setuptools documentation in the example
        provided for `basic usage
        <http://setuptools.readthedocs.io/en/latest/setuptools.html?highlight=keywords#basic-use>`
        """
        return ''

    @property
    def author(self):
        """
        Package author’s name.

        Either the author or the maintainer must be identified. If
        maintainer is provided, distutils lists it as the author in
        PKG-INFO.

        Returns:
             str: A short string
        """
        value = 'Optel Business Technologies Team'
        return self._ensure_short_string(value)

    @property
    def author_email(self):
        """
        Email address of the package author.

        See also :attr:`~author`

        Returns:
             str: An email address
        """
        value = 'btechsupport@optelgroup.com'
        return self._ensure_email_address(value)

    @property
    def classifiers(self):
        """
        A list of classifiers.

        Feel free to consult
        `all possibles classifiers
        <https://pypi.python.org/pypi?%3Aaction=list_classifiers>`.

        Returns:
             List[str]: A list of short strings
        """
        value = ['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python :: 3.6',
                 'Topic :: Utilities']
        return [self._ensure_short_string(string) for string in value]

    @property
    def packages(self):
        """
        A list of packages to distribute (and all their submodules).

        It's usage is explained in
        `distutils documentation
        <https://docs.python.org/2/distutils/setupscript.html#listing-whole-packages>`

        You may also read about :func:`setuptools.find_packages` function and
        `it's usage
        <http://setuptools.readthedocs.io/en/latest/setuptools.html?highlight=keywords#using-find-packages>`.

        Returns:
             List[str]: A list of strings
        """
        find_packages = setuptools.PEP420PackageFinder.find
        value = find_packages(str(PROJECT_ROOT), exclude=['doc',
                                                          'test*',
                                                          'requiremnts'])
        return [self._ensure_short_string(package) for package in value]

    @property
    def tests_require(self):
        """
        Automated tests dependancies.

        If your project’s tests need one or more additional packages besides
        those needed to install it, you can use this option to specify them.

        It's usage is explained in `setuptools documentation
        <http://setuptools.readthedocs.io/en/latest/setuptools.html#new-and-changed-setup-keywords>`

        Returns:
             List[str]: A list of short strings
        """
        return []

    @property
    def setup_requires(self):
        """
        A string or list of strings specifying what other distributions need to
        be present in order for the setup script to run. setuptools will
        attempt to obtain these (even going so far as to download them using
        EasyInstall) before processing the rest of the setup script or
        commands. This argument is needed if you are using distutils extensions
        as part of your build process; for example, extensions that process
        `setup()` arguments and turn them into EGG-INFO metadata files.

        Note:
            Projects listed in setup_requires will NOT be automatically
            installed on the system where the setup script is being run. They
            are simply downloaded to the ./.eggs directory if they’re not
            locally available already. If you want them to be installed, as
            well as being available when the setup script is run, you should
            add them to install_requires and setup_requires.

        Returns:
             List[str]: A list of short strings
        """
        return []

    @property
    def extras_require(self):
        """
        A dictionary mapping names of `extras` (optional features of your
        project) to strings or lists of strings specifying what other
        distributions must be installed to support those features.

        See Also:
            http://setuptools.readthedocs.io/en/latest/setuptools.html#declaring-extras-optional-features-with-their-own-dependencies

        Returns:
            Dict: Lists of dependencies indexed by the feature they enable.
        """
        return {}

    def setup(self):
        """Run :func:`setuptools.setup` using :func:~`raw`."""
        return setuptools.setup(**self.raw())

    def raw(self):
        """
        Create a generic dict representation.

        Provides a uniform access to all distribution data as python
        primitives, exactly the same one would provide to
        :func:`setuptools.setup`

        Returns:
            dict: Keyword arguments for :func:`setuptools.setup`.
        """
        return dict(name=self.name,
                    version=self.version,
                    description=self.description,
                    long_description=self.long_description,
                    url=self.url,
                    license=self.license,
                    author=self.author,
                    author_email=self.author_email,
                    classifiers=self.classifiers,
                    packages=self.packages,
                    include_package_data=True,
                    entry_points={
                        'console_scripts': [
                            '{module!s}={module!s}.cli:main'.format(
                                module=self.name)
                        ]
                    },
                    cmdclass={'clean': Clean},
                    tests_require=self.tests_require,
                    setup_requires=self.setup_requires,
                    extras_require=self.extras_require)

    def __str__(self):
        """Provide a human-readable representation."""
        import pprint
        return pprint.pformat(self.raw(),)

    @staticmethod
    def _ensure_short_string(string):
        string = str(string)
        assert len(string) <= 200
        return string

    @staticmethod
    def _ensure_long_string(string):
        string = str(string)
        return string

    @staticmethod
    def _ensure_email_address(string):
        string = str(string)
        _, email_str = email.utils.parseaddr(str(string))
        assert email_str == str(string)
        return string

    @staticmethod
    def _ensure_url(string, qualifying=None):
        string = str(string)
        min_attributes = ('scheme', 'netloc')

        qualifying = min_attributes if qualifying is None else qualifying
        token = urlparse(str(string))
        valid = all([getattr(token, qualifying_attr)
                     for qualifying_attr in qualifying])
        assert valid
        return string


class Clean(setuptools.Command):
    """Custom clean command to tidy up the project."""

    description = 'Custom clean command to tidy up the project.'
    user_options = []
    default_patterns = ['build',  'dist', '*.egg-info', '*.egg', '*.pyc',
                        '*.pyo', '*~', '__pycache__', '.tox', '.coverage',
                        'htmlcov']

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        for pattern in self.default_patterns:
            self._remove_matching_files(pattern)

    def _remove_matching_files(self, pattern):
        for path in find_files(pattern):
            self.announce('Cleaning path {!s}'.format(path), 2)
            shutil.rmtree(path, ignore_errors=True)


def read_file(file_path):
    """Read text from file relative to the project root."""
    return open(os.path.join(PROJECT_ROOT, str(file_path))).read()


def list_from_file(file_path):
    content = read_file(file_path)
    return [line.strip() for line in content.splitlines() if line]


def find_files(pattern, directory=PROJECT_ROOT):
    """Generate file names matching pattern recursively found in directory."""
    for root, dirs, files in os.walk(str(directory)):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename


def mkdir_p(path):
    """
    Behave like ``mkdir -b``

    Args:
        path (str):

    Returns:
        str: resulting path
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
    return path


def main():
    """Main entry point."""
    meta = ProjectMetadata()
    meta.setup()


if __name__ == '__main__':
    main()
