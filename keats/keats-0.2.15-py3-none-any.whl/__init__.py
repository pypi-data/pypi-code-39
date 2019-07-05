import os
import toml
from os.path import join, abspath, dirname, isfile, isdir
import fire
from warnings import warn
from .version import __version__, __name__
from .changelog_utils import update_changelog_interactive, save_to_markdown
from glob import glob
from termcolor import cprint
import re


PYPROJECT = "pyproject.toml"
RED = "\u001b[31m"
RESET = "\u001b[0m"
VERSIONPY = "__version__.py"


def err(msg):
    return cprint(msg, "red")


def info(msg):
    return cprint(msg, "blue")


class Pkg(object):
    def __init__(self, directory, filename):
        self.path = join(str(directory), str(filename))
        self.directory = directory
        if not isfile(self.path):
            warn(
                err(
                    "Cannot run keats. No {} file found in current directory {}.".format(
                        PYPROJECT, directory
                    )
                )
            )

    def _get(self, key):
        return self.config["tool"]["poetry"].get(key, None)

    @property
    def config(self):
        """
        Return the toml file information.

        :return:
        :rtype:
        """
        return toml.load(self.path)

    def config_info(self):
        toml_info = dict(self.config["tool"]["poetry"])
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
        if "packages" in self.config["tool"]["poetry"]:
            pkgs = []
            for pkg in self.config["tool"]["poetry"]["packages"]:
                if "from" in pkg:
                    pkgs.append(join(pkg["from"], pkg["include"]))
                else:
                    pkgs.append(pkg["include"])
        else:
            pkgs = [self._get("name")]
        return pkgs

    def dependencies(self):
        return self.config["tool"]["poetry"]["dependencies"]

    def dev_dependencies(self):
        return self.config["tool"]["poetry"]["dev-dependencies"]

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
        cprint("spawning shell ({})".format(self.directory), "blue")
        cprint(" ".join(cmd), "yellow")
        cprint("exiting shell", "blue")
        return os.system(cline)

    def run_poetry_cmd(self, *cmd):
        return self.run_cmd("poetry run", *cmd)


class Base(object):
    def __init__(self, path):
        self._path = path

    def _cmd(self, *cmd):
        return self._path.run_cmd(*cmd)

    def _get(self, key):
        return self._path.config["tool"]["poetry"].get(key, None)


class Run(Base):
    def format(self):
        """
        Run the format script.

        :return:
        :rtype:
        """
        paths = [self._path.local_path(p) for p in self._path.packages() + ["tests"]]
        self._cmd(" ".join(["black"] + paths))

    def _script(self, name):
        here = abspath(dirname(__file__))
        return join(here, "..", "keat_scripts", name)

    def release(self):
        self._cmd("sh {}".format(self._script("release.sh")))

    def document(self):
        pass

    def clear_cache(self, cachename="pypi"):
        info("clearing poetry cache")
        self._cmd("poetry cache:clear --all {}".format(cachename))

    def install(self):
        """
        Install keats to this project.

        :return:
        """
        self._cmd("poetry add --dev keats")

    def update(self, cache="pypi"):
        """
        Update keats in this project.

        :param clear: if provided, will clear the poetry cache (default: pypi)

        :return:
        """
        self._cmd("poetry remove --dev keats")
        if cache:
            self.clear_cache(cache)
        self.install()


class Version(Base):
    def print(self):
        """Return package version"""
        return self._get("version")

    def bump(self, version=None):
        if version is None:
            self._cmd("poetry version")
        else:
            self._cmd("poetry version {}".format(version))
        self._write()

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

    def _write(self, with_confirm=False):
        pkg_info = self._path.config_info()
        path = self._path.version_py()
        if with_confirm:
            ans = input("Write to '{}'?".format(path))
        else:
            ans = ""
        if ans.strip() == "" or ans.strip().lower() == "y":
            with open(path, "w") as f:
                lines = [
                    "# {}\n".format(VERSIONPY),
                    "# autogenerated by {} {}\n".format(__name__, __version__),
                ]
                for k, v in pkg_info.items():
                    if isinstance(v, str):
                        v = '"{}"'.format(v)
                    lines.append("__{}__ = {}\n".format(k, v))
                f.writelines(lines)
        else:
            info("no files written")


class ChangeLog(Base):
    @property
    def _dir(self):
        d = join(self._path.directory, ".keats")
        if not isdir(d):
            os.mkdir(d)
        return d

    @property
    def _json(self):
        return join(self._dir, "changelog.json")

    @property
    def _markdown(self):
        return join(self._dir, "changelog.md")

    def up(self):
        """Save changelog to a markdown file."""
        save_to_markdown(self._json, self._markdown)

    def clear(self):
        """Clear the changelog files."""
        info(self._json)
        if isfile(self._json):
            os.remove(self._json)
        if isfile(self._markdown):
            os.remove(self._markdown)

    def new(self):
        """Interactively add a changelog entry. Entries are located in the '.keats' folder."""
        update_changelog_interactive(
            self._get("version"), self._json, self._markdown, self._path.package()
        )


class Keats(object):
    """Python version and worfklow release manager

    Usage `keats [command] [arguments]`
    """

    def __init__(self, directory=os.getcwd(), filename=PYPROJECT):
        self.pkg = Pkg(str(directory), str(filename))

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

    @property
    def v(self):
        """Return package version"""
        return self.version.print()

    @property
    def name(self):
        return self.pkg.name()

    @property
    def package(self):
        return self.pkg.package()

    @property
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

    def bump(self, version=None):
        self.version.bump(version)
        self.changelog.new()

    def release(self):
        return self.run.release()

    def install(self):
        """
        Install keats to this project.

        :return:
        """
        self.run.install()
        self.version.up()

    def update(self, cache="pypi"):
        """
        Update keats in this project.

        :param clear: if provided, will clear the poetry cache (default: pypi)

        :return:
        """
        self.run.update(cache=cache)

        #
        # for k in ["dependencies", "dev-dependencies"]:
        #     not_found = []
        #     for l in config["tool"]["poetry"][k]:
        #         if not find(l):
        #             not_found.append(l)
        #     if not_found:
        #         print("Could not find {}: {}".format(k, " ".join(not_found)))


def main():
    fire.Fire(Keats)
