from setuptools import setup, Command
import os
import sys
from shutil import rmtree

with open('README.md') as f:
    README = f.read()

VERSION = '0.1.1'

########
# Copied from https://github.com/kennethreitz/setup.py
here = os.path.abspath(os.path.dirname(__file__))


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(VERSION))
        os.system('git push --tags')

        sys.exit()
########


setup(
    name="odoo11_l10n_es_coop",
    version=VERSION,
    author="Coopdevs,Acysos",
    url="https://gitlab.com/coopdevs/odoo11-l10n-es-coop",
    description="Odoo Spanish Localization for Cooperatives",
    long_description=README,
    long_description_content_type='text/markdown',
    license="GPL",
    packages=['odoo/addons/l10n_es_coop'],
    classifiers=[],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)
