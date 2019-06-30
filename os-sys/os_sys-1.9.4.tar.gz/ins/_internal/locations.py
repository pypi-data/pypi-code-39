"""Locations where we look for configs, install stuff, etc"""
from __future__ import absolute_import

import os
import os.path
import platform
import site
import sys
import sysconfig
from distutils import sysconfig as distutils_sysconfig
from distutils.command.install import SCHEME_KEYS  # type: ignore

from ins._internal.utils import appdirs
from ins._internal.utils.compat import WINDOWS, expanduser
from ins._internal.utils.typing import MYPY_CHECK_RUNNING

if MYPY_CHECK_RUNNING:
    from typing import Any, Union, Dict, List, Optional


# Application Directories
USER_CACHE_DIR = appdirs.user_cache_dir("ins")


DELETE_MARKER_MESSAGE = '''\
This file is placed here by ins to indicate the source was put
here by ins.

Once this package is successfully installed this source code will be
deleted (unless you remove this file).
'''
ins_DELETE_MARKER_FILENAME = 'ins-delete-this-directory.txt'


def write_delete_marker_file(directory):
    # type: (str) -> None
    """
    Write the ins delete marker file into this directory.
    """
    filepath = os.path.join(directory, ins_DELETE_MARKER_FILENAME)
    with open(filepath, 'w') as marker_fp:
        marker_fp.write(DELETE_MARKER_MESSAGE)


def running_under_virtualenv():
    # type: () -> bool
    """
    Return True if we're running inside a virtualenv, False otherwise.

    """
    if hasattr(sys, 'real_prefix'):
        return True
    elif sys.prefix != getattr(sys, "base_prefix", sys.prefix):
        return True

    return False


def virtualenv_no_global():
    # type: () -> bool
    """
    Return True if in a venv and no system site packages.
    """
    # this mirrors the logic in virtualenv.py for locating the
    # no-global-site-packages.txt file
    site_mod_dir = os.path.dirname(os.path.abspath(site.__file__))
    no_global_file = os.path.join(site_mod_dir, 'no-global-site-packages.txt')
    if running_under_virtualenv() and os.path.isfile(no_global_file):
        return True
    else:
        return False


if running_under_virtualenv():
    src_prefix = os.path.join(sys.prefix, 'src')
else:
    # FIXME: keep src in cwd for now (it is not a temporary folder)
    try:
        src_prefix = os.path.join(os.getcwd(), 'src')
    except OSError:
        # In case the current working directory has been renamed or deleted
        sys.exit(
            "The folder you are executing ins from can no longer be found."
        )

# under macOS + virtualenv sys.prefix is not properly resolved
# it is something like /path/to/python/bin/..
# Note: using realpath due to tmp dirs on OSX being symlinks
src_prefix = os.path.abspath(src_prefix)

# FIXME doesn't account for venv linked to global site-packages

site_packages = sysconfig.get_path("purelib")  # type: Optional[str]

# This is because of a bug in PyPy's sysconfig module, see
# https://bitbucket.org/pypy/pypy/issues/2506/sysconfig-returns-incorrect-paths
# for more information.
if platform.python_implementation().lower() == "pypy":
    site_packages = distutils_sysconfig.get_python_lib()
try:
    # Use getusersitepackages if this is present, as it ensures that the
    # value is initialised properly.
    user_site = site.getusersitepackages()
except AttributeError:
    user_site = site.USER_SITE
user_dir = expanduser('~')
if WINDOWS:
    bin_py = os.path.join(sys.prefix, 'Scripts')
    bin_user = os.path.join(user_site, 'Scripts')
    # buildout uses 'bin' on Windows too?
    if not os.path.exists(bin_py):
        bin_py = os.path.join(sys.prefix, 'bin')
        bin_user = os.path.join(user_site, 'bin')

    config_basename = 'ins.ini'

    legacy_storage_dir = os.path.join(user_dir, 'ins')
    legacy_config_file = os.path.join(
        legacy_storage_dir,
        config_basename,
    )
else:
    bin_py = os.path.join(sys.prefix, 'bin')
    bin_user = os.path.join(user_site, 'bin')

    config_basename = 'ins.conf'

    legacy_storage_dir = os.path.join(user_dir, '.ins')
    legacy_config_file = os.path.join(
        legacy_storage_dir,
        config_basename,
    )
    # Forcing to use /usr/local/bin for standard macOS framework installs
    # Also log to ~/Library/Logs/ for use with the Console.app log viewer
    if sys.platform[:6] == 'darwin' and sys.prefix[:16] == '/System/Library/':
        bin_py = '/usr/local/bin'

global_config_files = [
    os.path.join(path, config_basename)
    for path in appdirs.site_config_dirs('ins')
]

site_config_file = os.path.join(sys.prefix, config_basename)
new_config_file = os.path.join(appdirs.user_config_dir("ins"), config_basename)


def distutils_scheme(dist_name, user=False, home=None, root=None,
                     isolated=False, prefix=None):
    # type:(str, bool, str, str, bool, str) -> dict
    """
    Return a distutils install scheme
    """
    from distutils.dist import Distribution

    scheme = {}

    if isolated:
        extra_dist_args = {"script_args": ["--no-user-cfg"]}
    else:
        extra_dist_args = {}
    dist_args = {'name': dist_name}  # type: Dict[str, Union[str, List[str]]]
    dist_args.update(extra_dist_args)

    d = Distribution(dist_args)
    # Ignoring, typeshed issue reported python/typeshed/issues/2567
    d.parse_config_files()
    # NOTE: Ignoring type since mypy can't find attributes on 'Command'
    i = d.get_command_obj('install', create=True)  # type: Any
    assert i is not None
    # NOTE: setting user or home has the side-effect of creating the home dir
    # or user base for installations during finalize_options()
    # ideally, we'd prefer a scheme class that has no side-effects.
    assert not (user and prefix), "user={} prefix={}".format(user, prefix)
    i.user = user or i.user
    if user:
        i.prefix = ""
    i.prefix = prefix or i.prefix
    i.home = home or i.home
    i.root = root or i.root
    i.finalize_options()
    for key in SCHEME_KEYS:
        scheme[key] = getattr(i, 'install_' + key)

    # install_lib specified in setup.cfg should install *everything*
    # into there (i.e. it takes precedence over both purelib and
    # platlib).  Note, i.install_lib is *always* set after
    # finalize_options(); we only want to override here if the user
    # has explicitly requested it hence going back to the config

    # Ignoring, typeshed issue reported python/typeshed/issues/2567
    if 'install_lib' in d.get_option_dict('install'):  # type: ignore
        scheme.update(dict(purelib=i.install_lib, platlib=i.install_lib))

    if running_under_virtualenv():
        scheme['headers'] = os.path.join(
            sys.prefix,
            'include',
            'site',
            'python' + sys.version[:3],
            dist_name,
        )

        if root is not None:
            path_no_drive = os.path.splitdrive(
                os.path.abspath(scheme["headers"]))[1]
            scheme["headers"] = os.path.join(
                root,
                path_no_drive[1:],
            )

    return scheme
