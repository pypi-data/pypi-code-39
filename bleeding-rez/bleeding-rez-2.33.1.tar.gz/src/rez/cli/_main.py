"""The main command-line entry point."""
from __future__ import print_function
import sys
import importlib
from rez.vendor.argparse import _StoreTrueAction, SUPPRESS
from rez.cli._util import subcommands, LazyArgumentParser, _env_var_true
from rez.utils.logging_ import print_error
from rez.exceptions import RezError, RezSystemError, RezUncatchableError
from rez.utils.logging_ import setup_logging
from rez import __version__, __project__


class SetupRezSubParser(object):
    """Callback class for lazily setting up rez sub-parsers.
    """
    def __init__(self, module_name):
        self.module_name = module_name

    def __call__(self, parser_name, parser):
        mod = self.get_module()

        error_msg = None
        if not mod.__doc__:
            error_msg = "command module %s must have a module-level " \
                "docstring (used as the command help)" % self.module_name
        if not hasattr(mod, 'command'):
            error_msg = "command module %s must provide a command() " \
                "function" % self.module_name
        if not hasattr(mod, 'setup_parser'):
            error_msg = "command module %s  must provide a setup_parser() " \
                "function" % self.module_name
        if error_msg:
            print(error_msg, file=sys.stderr)
            return SUPPRESS

        mod.setup_parser(parser)
        parser.description = mod.__doc__
        parser.set_defaults(func=mod.command, parser=parser)
        # add the common args to the subparser
        _add_common_args(parser)

        # optionally, return the brief help line for this sub-parser
        brief = mod.__doc__.strip('\n').split('\n')[0]
        return brief

    def get_module(self):
        if self.module_name not in sys.modules:
            importlib.import_module(self.module_name)
        return sys.modules[self.module_name]


def _add_common_args(parser):
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="verbose mode, repeat for more verbosity")
    parser.add_argument("--debug", dest="debug", action="store_true",
                        help=SUPPRESS)
    parser.add_argument("--profile", dest="profile", type=str,
                        help=SUPPRESS)


class InfoAction(_StoreTrueAction):
    def __call__(self, parser, args, values, option_string=None):
        from rez.system import system
        txt = system.get_summary_string()
        print()
        print(txt)
        print()
        sys.exit(0)


def isolated_environment():
    import os
    from rez.backport.shutilwhich import which

    environ = {
        key: os.getenv(key)
        for key in ("USERNAME",
                    "SYSTEMROOT",

                    # Windows
                    "ComSpec",
                    "windir",
                    "PROMPT",
                    "PathExt",
                    "OS",
                    "TMP",
                    "Temp",

                    # For platform_.arch()
                    "PROCESSOR_ARCHITEW6432",
                    "PROCESSOR_ARCHITECTURE",

                    # Linux
                    "DISPLAY")
        if os.getenv(key)
    }

    def whichdir(exe):
        return os.path.dirname(which(exe))

    if os.name == "nt":
        environ["PATH"] = os.pathsep.join([
            whichdir("cmd"),
            whichdir("powershell"),
        ])

    else:
        environ["PATH"] = os.pathsep.join([
            whichdir("bash"),
        ])

    # Include REZ_ variables
    for key, value in os.environ.items():
        if not key.startswith("REZ_"):
            continue

        environ[key] = value

    return environ


def run(command=None):
    import os

    # For safety, replace the current session with one
    # that doesn't include PYTHONPATH.

    patched = "_REZ_PATCHED_ENV" in os.environ

    try:
        sys.argv.remove("--isolated")
    except ValueError:
        safe = False
    else:
        safe = True

    if safe and not patched:
        # Re-spawn Python with safe environment

        import subprocess
        environ = isolated_environment()

        # Prevent subsequent session from spawing new session
        environ["_REZ_PATCHED_ENV"] = "1"

        # Restore subsequent shells to the current directory,
        # countering the `cwd=rezdir` below.
        environ["_REZ_INITIAL_CWD"] = os.getcwd()

        # Replace absolute path to executable with python
        # Why not use sys.argv as-is?
        #   The first argument is the absolute path to the executable
        #   with this command, followed by the arguments. On Windows
        #   however, this executable does not include its extension,
        #   ".exe" which causes it not to be found.
        argv = [
            sys.executable,
            "-S",  # Do not `import site`
            "-B",  # Do not generate .pyc or __pycache__
        ]

        if sys.version > (2, 7):
            argv += [
                "-I",  # Isolate Python from the user's environment
            ]
        else:
            argv += [
                "-E",  # Ignore PYTHON* variables
                "-s",  # Do not load user site dir
            ]

        argv += [
            "-m", "rez"
        ] + sys.argv[1:]

        rezdir = os.path.join(__file__, "..", "..", "..")
        popen = subprocess.Popen(
            argv,

            # Use doctored-environment
            env=environ,

            # Consider rez from current working directory,
            # instead of PYTHONPATH
            cwd=rezdir
        )

        # Delegate all further input to child
        exit(popen.wait())

    setup_logging()

    # Prevent `__pycache__` folders from being accidentally
    # created and picked up as Rez packages.
    sys.dont_write_bytecode = True

    parser = LazyArgumentParser("rez")

    parser.add_argument("-i", "--info", action=InfoAction,
                        help="print information about rez and exit")
    parser.add_argument("-V", "--version", action="version",
                        version="%s %s" % (__project__, __version__))

    # add args common to all subcommands... we add them both to the top parser,
    # AND to the subparsers, for two reasons:
    #  1) this allows us to do EITHER "rez --debug build" OR
    #     "rez build --debug"
    #  2) this allows the flags to be used when using either "rez" or
    #     "rez-build" - ie, this will work: "rez-build --debug"
    _add_common_args(parser)

    # add lazy subparsers
    subparser = parser.add_subparsers(dest='cmd', metavar='COMMAND')
    for subcommand in subcommands:
        module_name = "rez.cli.%s" % subcommand

        subparser.add_parser(
            subcommand,
            help='',  # required so that it can be setup later
            setup_subparser=SetupRezSubParser(module_name))

    # construct args list. Note that commands like 'rez-env foo' and
    # 'rez env foo' are equivalent
    if command:
        args = [command] + sys.argv[1:]
    elif len(sys.argv) > 1 and sys.argv[1] in subcommands:
        command = sys.argv[1]
        args = sys.argv[1:]
    else:
        args = sys.argv[1:]

    # parse args depending on subcommand behaviour
    if command:
        arg_mode = subcommands[command].get("arg_mode")
    else:
        arg_mode = None

    if arg_mode == "grouped":
        # args split into groups by '--'
        arg_groups = [[]]
        for arg in args:
            if arg == '--':
                arg_groups.append([])
                continue
            arg_groups[-1].append(arg)

        opts = parser.parse_args(arg_groups[0])
        extra_arg_groups = arg_groups[1:]
    elif arg_mode == "passthrough":
        # unknown args passed in first extra_arg_group
        opts, extra_args = parser.parse_known_args(args)
        extra_arg_groups = [extra_args]
    else:
        # native arg parsing
        opts = parser.parse_args(args)
        extra_arg_groups = []

    if opts.debug or _env_var_true("REZ_DEBUG"):
        exc_type = RezUncatchableError
    else:
        exc_type = RezError

    def run_cmd():
        return opts.func(opts, opts.parser, extra_arg_groups)

    if opts.profile:
        import cProfile
        cProfile.runctx("run_cmd()", globals(), locals(), filename=opts.profile)
        returncode = 0
    else:
        try:
            returncode = run_cmd()
        except (NotImplementedError, RezSystemError) as e:
            raise
        except exc_type as e:
            print_error("%s: %s" % (e.__class__.__name__, str(e)))
            sys.exit(1)

    sys.exit(returncode or 0)


# Entry points for pip
def rez_config():
    return run("config")


def rez_build():
    return run("build")


def rez_release():
    return run("release")


def rez_env():
    return run("env")


def rez_context():
    return run("context")


def rez_suite():
    return run("suite")


def rez_interpret():
    return run("interpret")


def rez_python():
    return run("python")


def rez_selftest():
    return run("selftest")


def rez_bind():
    return run("bind")


def rez_search():
    return run("search")


def rez_view():
    return run("view")


def rez_status():
    return run("status")


def rez_help():
    return run("help")


def rez_depends():
    return run("depends")


def rez_memcache():
    return run("memcache")


def rez_yaml2py():
    return run("yaml2py")


def run_fwd():
    return run("forward")


def run_complete():
    return run("complete")


if __name__ == '__main__':
    run()


# Copyright 2013-2016 Allan Johns.
#
# This library is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library.  If not, see <http://www.gnu.org/licenses/>.
