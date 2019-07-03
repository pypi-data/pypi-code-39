"""Package manager for downloading packages from content providers
"""
import os
import json
import argparse
from pkg_resources import parse_requirements, Requirement
from typing import Dict, List
from os import makedirs, path
from urllib.request import urlopen


class CDNJSProvider:
    """CDNJS support for packy
    """

    INFO_TIMEOUT = 30
    DOWNLOAD_TIMEOUT = 120

    @staticmethod
    def get_assets(req: Requirement) -> List:
        """Get package info

        Arguments:
            req {Requirement} -- Requirement to look for

        Returns:
            List -- List containing all assets as dictionaries
        """
        url = 'https://api.cdnjs.com/libraries/{}?fields=assets'.format(
            req.name
        )

        with urlopen(url, timeout=CDNJSProvider.INFO_TIMEOUT) as response:
            content = json.loads(response.read().decode('utf-8'))

            if not content:
                return []

            return content['assets']

    @staticmethod
    def download_file(req: Requirement, filename: str, destination: str):
        """Download file for requirement

        Arguments:
            req {Requirement} -- Requirement to download files from
            filename {str} -- File of requirement
            destination {str} -- Destination file path
        """
        url = 'https://cdnjs.cloudflare.com/ajax/libs/{}/{}/{}'.format(
            req.name,
            req.specs[0][1],
            filename,
        )

        with urlopen(url, timeout=CDNJSProvider.DOWNLOAD_TIMEOUT) as response:
            with open(destination, 'wb') as destfile:
                destfile.write(response.read())


class Packy:
    """Class for installing packages from cdnjs
    """

    _providers = {
        'cdnjs': CDNJSProvider
    }

    def __init__(self, *, installdir: str = os.getcwd(), provider='cdnjs'):
        """
        Keyword Arguments:
            installdir {str} -- Directory where all packages are installed
                                (default: {os.getcwd()})
            provider {str} -- Provider where packages are stored
        """
        self._installdir = path.abspath(installdir)
        self._provider = self._providers[provider]

        # Function which is executed before installing - args: name, version
        self.pre_hook = None
        # Function which is executed after installing - args: name, version
        self.post_hook = None
        # Function which is executed if package already exists - args: name
        self.exist_hook = None

    def _call_hook(self, hook, *args):
        """Call given hook if callable with given args

        Arguments:
            hook -- Hook function
        """
        if callable(hook):
            hook(*args)

    def get_info(self, package: str) -> Dict:
        """Retrieve package information

        Arguments:
            package {str} -- Package name (can include version)

        Returns:
            Dict -- Dictionary containing asset information. None if no
                    matching version is found
        """
        requirement = Requirement.parse(package)

        for asset in self._provider.get_assets(requirement):
            if asset['version'] in requirement:
                return asset

        raise KeyError('package %s not found' % package)

    def install(self, packages: str) -> List:
        """Install one or more packages given as python requirements like
           jquery>=3.1

        Arguments:
            packages {str} -- Requirement string

        Returns:
            List -- List containing the installed packages
        """
        install_list = []

        for requirement in parse_requirements(packages):
            info = self.get_info(str(requirement))

            # Create root folder for package
            pkgdir = path.join(self._installdir, requirement.name)

            try:
                makedirs(pkgdir)
            except FileExistsError:
                self._call_hook(self.exist_hook, requirement.name)
                continue

            self._call_hook(self.pre_hook, requirement.name, info['version'])

            # Download files
            for filename in info['files']:
                filepath = path.join(pkgdir, filename)
                requirement = Requirement.parse(
                    '%s==%s' % (requirement.name, info['version'])
                )

                makedirs(path.dirname(filepath), exist_ok=True)
                self._provider.download_file(requirement, filename, filepath)

            install_list.append(str(requirement))
            self._call_hook(self.post_hook, requirement.name, info['version'])

        return install_list


def main():
    """Main entry
    """
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('requirement', help='requirement specifier', nargs='?')
    group.add_argument('-r', dest='reqfile', help='requirements file')
    parser.add_argument('-p', dest='provider', default='cdnjs',
                        help='content provider')
    parser.add_argument('-o', dest='output',
                        help='install directory (default: current directory)')

    args = parser.parse_args()

    if args.output:
        installdir = path.join(os.getcwd(), args.output)
    else:
        installdir = os.getcwd()

    packy = Packy(
        provider=args.provider,
        installdir=installdir
    )
    packy.pre_hook = lambda n, v: print('Installing %s(%s)' % (n, v))
    packy.post_hook = lambda n, v: print('Installed %s(%s)' % (n, v))
    packy.exist_hook = lambda n: print('Package %s already existing' % n)

    if args.requirement:
        requirements = args.requirement
    else:
        with open(path.join(os.getcwd(), args.reqfile), 'r') as reqfile:
            requirements = reqfile.read()

    installed = packy.install(requirements)

    if installed:
        print('Successfully installed: %s' % ', '.join(installed))


if __name__ == '__main__':
    main()
