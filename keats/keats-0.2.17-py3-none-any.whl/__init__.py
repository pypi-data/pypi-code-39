import os
from os.path import join, abspath, dirname, isfile, isdir
from warnings import warn

import fire
import toml
from functools import wraps


from .changelog_utils import update_changelog_interactive, save_to_markdown
from .version import __version__, __name__

PYPROJECT = "pyproject.toml"
RED = "\u001b[31m"
RESET = "\u001b[0m"
VERSIONPY = "__version__.py"


def err(msg):
    return RED + msg + RESET


keats_version = __name__ + " " + __version__


class Pkg(object):
    def __init__(self, directory, filename):
        self.path = join(directory, filename)
        self.directory = directory

    def valid(self):
        return isfile(self.path)

    def _get(self, key):
        return self.get_config()["tool"]["poetry"].get(key, None)

    def get_config(self):
        """
        Return the toml file information.

        :return:
        :rtype:
        """

        return toml.load(self.path)

    def config_info(self):
        toml_info = dict(self.get_config()["tool"]["poetry"])
        pkg_info = {
            "version": toml_info["version"],
            "name": toml_info["name"],
            "title": toml_info["name"],
            "authors": toml_info.get("authors", list()),
            "repo": toml_info.get("repo", None),
            "homepage": toml_info.get("homepage", None),
            "description": toml_info.get("description", None),
        }
        return pkg_info

    def version_py(self):
        return join(self.pkg_path(), VERSIONPY)

    def local_path(self, path):
        return abspath(join(self.directory, path))

    def pkg_path(self):
        return self.local_path(self.package())

    def test_path(self):
        return self.local_path("tests")

    def packages(self):
        """
        Return all listed packaged in the pyproject.toml file. Note that this
        does not consider * files.

        :return: list of package names
        :rtype: list
        """
        if "packages" in self.get_config()["tool"]["poetry"]:
            pkgs = []
            for pkg in self.get_config()["tool"]["poetry"]["packages"]:
                if "from" in pkg:
                    pkgs.append(join(pkg["from"], pkg["include"]))
                else:
                    pkgs.append(pkg["include"])
        else:
            pkgs = [self._get("name")]
        return pkgs

    def name(self):
        return self._get("name")

    def package(self):
        """
        Return the estimated main package from the pyproject.toml file.

        :return: version
        :rtype: basestring
        """
        return self.packages()[0]

    def run_cmd(self, *cmd):
        cline = "(cd {}; {})".format(self.directory, " ".join(cmd))
        print(cline)
        return os.system(cline)

    def run_poetry_cmd(self, *cmd):
        return self.run_cmd("poetry run", *cmd)


def requires_config(f):
    """If config is unavailable, prints a warning and does an early exit"""

    @wraps(f)
    def wrapped(self, *args, **kwargs):
        if not self.pkg.valid():
            print(err("No pyproject.toml file found"))
            exit(0)
        else:
            return f(self, *args, **kwargs)

    return wrapped


class Base(object):
    def __init__(self, path):
        self.pkg = path

    def _cmd(self, *cmd):
        return self.pkg.run_cmd(*cmd)

    @requires_config
    def _get(self, key):
        return self.pkg.get_config()["tool"]["poetry"].get(key, None)


class Run(Base):
    @requires_config
    def format(self):
        """
        Run the format script.

        :return:
        :rtype:
        """
        paths = [self.pkg.local_path(p) for p in self.pkg.packages() + ["tests"]]
        self._cmd(" ".join(["black"] + paths))

    @requires_config
    def _script(self, name):
        here = abspath(dirname(__file__))
        return join(here, "..", "keat_scripts", name)

    @requires_config
    def release(self):
        self._cmd("sh {}".format(self._script("release.sh")))

    @requires_config
    def document(self):
        pass


class Version(Base):
    @requires_config
    def print(self):
        """Return package version"""
        return self._get("version")

    @requires_config
    def bump(self, version=None):
        if version is None:
            self._cmd("poetry version")
        else:
            self._cmd("poetry version {}".format(version))
        self._write()

    @requires_config
    def up(self, version=None):
        """
        Update the package version from the pyproject.toml file.

        :param version: if provided, bump the version number (optional)
        :type version: basestring
        :return: the version
        :rtype: basestring
        """
        if version is None:
            self._write()
        else:
            self.bump(version)
        return self._get("version")

    @requires_config
    def _write(self, with_confirm=False):
        pkg_info = self.pkg.config_info()
        path = self.pkg.version_py()
        if with_confirm:
            ans = input("Write to '{}'?".format(path))
        else:
            ans = ""
        if ans.strip() == "" or ans.strip().lower() == "y":
            with open(path, "w") as f:
                lines = [
                    "# {}\n".format(VERSIONPY),
                    "# autogenerated by {}\n".format(keats_version),
                ]
                for k, v in pkg_info.items():
                    if isinstance(v, str):
                        v = '"{}"'.format(v)
                    lines.append("__{}__ = {}\n".format(k, v))
                f.writelines(lines)
        else:
            print("no files written")


class ChangeLog(Base):
    def _dir(self):
        d = join(self.pkg.directory, ".keats")
        if not isdir(d):
            os.mkdir(d)
        return d

    @property
    def _json(self):
        return join(self._dir(), "changelog.json")

    @property
    def _markdown(self):
        return join(self._dir(), "changelog.md")

    @requires_config
    def up(self):
        """Save changelog to a markdown file."""
        save_to_markdown(self._json, self._markdown)

    @requires_config
    def clear(self):
        """Clear the changelog files."""
        print(self._json)
        if isfile(self._json):
            os.remove(self._json)
        if isfile(self._markdown):
            os.remove(self._markdown)

    @requires_config
    def new(self):
        """Interactively add a changelog entry. Entries are located in the '.keats' folder."""
        update_changelog_interactive(
            self._get("version"), self._json, self._markdown, self.pkg.package()
        )


class TemporaryPath(object):
    def __init__(self, path):
        self.path = path
        self.existed = isfile(path)

    def __enter__(self):
        pass

    def __exit__(self, exception_type, exception_value, traceback):
        if not self.existed and isfile(self.path):
            os.remove(self.path)


class TemporaryFileWriter(TemporaryPath):
    def __enter__(self):
        self.file = open(self.path, "w")
        return self.file

    def __exit__(self, exception_type, exception_value, traceback):
        self.file.close()
        super().__exit__(exception_type, exception_value, traceback)


class Keats(object):
    def __init__(self, directory=os.getcwd(), filename=PYPROJECT):
        self.pkg = Pkg(directory, filename)

    @requires_config
    def info(self):
        """
        Return package information from the toml file.

        :return:
        :rtype:
        """
        return self.pkg.config_info()

    def keats(self):
        """
        Return the keats version number.

        :return:
        :rtype:
        """
        return __name__ + " " + __version__

    @requires_config
    def v(self):
        """Return package version"""
        return self.version.print()

    @requires_config
    def name(self):
        return self.pkg.name()

    @requires_config
    def package(self):
        return self.pkg.package()

    @requires_config
    def packages(self):
        return self.pkg.packages()

    @property
    def version(self):
        return Version(self.pkg)

    @property
    def changelog(self):
        return ChangeLog(self.pkg)

    @property
    def run(self):
        return Run(self.pkg)

    @requires_config
    def bump(self, version=None):
        self.version.bump(version)
        self.changelog.new()

    @requires_config
    def global_install(self, *args, cmd="pip install ."):
        """
        Pip install in editable mode. If not setup.py exists, creates a minimal setup.py.

        :param args:
        :type args:
        :return:
        :rtype:
        """
        path = self.pkg.local_path("setup.py")
        if not isfile(path):
            with TemporaryFileWriter(path) as f:
                lines = [
                    "# autogenerated by {}\n".format(keats_version),
                    "from distutils.core import setup\n",
                    "\n",
                    'setup(title="{title}", name="{name}", version="{version}", packages={packages})\n'.format(
                        title=self.name,
                        name=self.name,
                        version=self.v(),
                        packages=self.packages,
                    ),
                ]
                f.writelines(lines)
                self.pkg.run_cmd(cmd, *args)
        else:
            self.pkg.run_cmd(cmd, *args)

    @requires_config
    def release(self):
        return self.run.release()

    # TODO: flesh this out with Jinja? When do we need a full setup.py file?
    @requires_config
    def develop(self, *args):
        """
        Pip install in editable mode. If not setup.py exists, creates a minimal setup.py.

        :param args:
        :type args:
        :return:
        :rtype:
        """
        self.global_install(*args, cmd="pip install -e .")


here = abspath(dirname(__file__))
self_keats = Keats(join(here, ".."))


def main():
    fire.Fire(Keats)
