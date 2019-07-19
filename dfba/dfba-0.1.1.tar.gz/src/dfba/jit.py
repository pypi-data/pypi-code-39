# Copyright (C) 2018, 2019 Columbia University Irving Medical Center,
#     New York, USA
# Copyright (C) 2019 Novo Nordisk Foundation Center for Biosustainability,
#     Technical University of Denmark

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import logging
import os
import sys
from tempfile import NamedTemporaryFile

import distutils.sysconfig
import setuptools
from setuptools.command.build_ext import build_ext


logger = logging.getLogger(__name__)


DARWIN_KEY = "Darwin"
LINUX_KEY = "Linux"

CXX_FLAGS = {
    "clang": [
        "-Wall",
        "-Wno-unused-variable",
        "-march=native",
        "-stdlib=libc++",
        "-std=c++11",
    ],
    "icc": [
        "-Wall",
        "-Wno-unused-variable",
        "-march=native",
        "-stdlib=libc++",
        "-std=c++11",
    ],
    "gcc-mac": ["-Wall", "-Wno-unused-variable", "-std=c++11", "-msse4.2"],
    "gcc-linux": ["-Wall", "-Wno-unused-variable", "-std=c++11"],
}


class UnsupportedCompilerException(Exception):
    """UnsupportedCompilerException is a class for raising exceptions on unsuported compilers.
    """

    pass


class BuildExtWithoutPlatformSuffix(build_ext):
    """BuildExtWithoutPlatformSuffix is a class for building library functionlib without the platform suffix added to the file name.
    """

    def get_ext_filename(self, ext_name):
        filename = super().get_ext_filename(ext_name)
        return get_ext_filename_without_platform_suffix(filename)


def get_ext_filename_without_platform_suffix(filename):
    """File name without platform suffix

        Returns
        -------
        filename
            Name of shared library without platform suffix.
    """

    name, ext = os.path.splitext(filename)
    ext_suffix = distutils.sysconfig.get_config_var("EXT_SUFFIX")

    if ext_suffix == ext:
        return filename

    ext_suffix = ext_suffix.replace(ext, "")
    idx = name.find(ext_suffix)

    if idx == -1:
        return filename
    else:
        return name[:idx] + ext


def get_cxxflags():
    """CXX FLAGS
        JIT compilation of functionlib.cpp adapted from <https://github.com/jakeret/hope>. Copyright (c) 2013 ETH Zurich, Institute of Astronomy, Lukas Gamper <lukas.gamper@usystems.ch>

        Returns
        -------
        flags
            The appropriate CXX FLAGS for compilation of functionlib.cpp on supported platform. Requires compilation with c++11 features enabled.
    """
    from distutils.ccompiler import new_compiler
    from distutils.sysconfig import customize_compiler
    from distutils import sysconfig
    from platform import system

    if system() == DARWIN_KEY:
        CXX_FLAGS["gcc"] = CXX_FLAGS["gcc-mac"]
        CXX_FLAGS["cc"] = CXX_FLAGS["clang"]
        CXX_FLAGS["c++"] = CXX_FLAGS["clang"]
    elif system() == LINUX_KEY:
        CXX_FLAGS["gcc"] = CXX_FLAGS["gcc-linux"]
        CXX_FLAGS["cc"] = CXX_FLAGS["gcc"]
        CXX_FLAGS["c++"] = CXX_FLAGS["gcc"]
    else:
        raise UnsupportedCompilerException(
            "System: %s is not supported" % system()
        )

    sysconfig.get_config_vars()
    compiler = new_compiler()
    customize_compiler(compiler)
    compiler_name = compiler.compiler[0].split("/")[-1]

    if compiler_name not in CXX_FLAGS.keys():
        compiler_name = (
            "gcc-linux" if compiler_name.find("gcc") > -1 else compiler_name
        )

    for name, flags in CXX_FLAGS.items():
        if compiler_name.startswith(name):
            return flags
    raise UnsupportedCompilerException(
        "Unknown compiler: {0}".format(compiler_name)
    )


def compile():
    """Compile
        JIT compilation of functionlib.cpp adapted from <https://github.com/jakeret/hope>. Copyright (c) 2013 ETH Zurich, Institute of Astronomy, Lukas Gamper <lukas.gamper@usystems.ch>
    """
    stdout = sys.stdout
    sys.stdout = NamedTemporaryFile(mode="w", suffix=".log", delete=False)
    argv, target, localfilename, so_filename = (
        sys.argv,
        os.getcwd(),
        "functionlib",
        "functionlib.so",
    )
    try:
        try:
            sources = os.path.join(target, "{0}.cpp".format(localfilename))
            sys.argv = ["", "build_ext", "-b", target, "-t", "/"]

            if sys.version_info[0] == 2:
                raise RuntimeError(
                    "This program is only intended for Python 3+."
                )

            cfg_vars = distutils.sysconfig.get_config_vars()
            if "CFLAGS" in cfg_vars:
                cfg_vars["CFLAGS"] = cfg_vars["CFLAGS"].replace(
                    "-Wstrict-prototypes", ""
                )
            if "OPT" in cfg_vars:
                cfg_vars["OPT"] = cfg_vars["OPT"].replace(
                    "-Wstrict-prototypes", ""
                )

            setuptools.setup(
                name=localfilename,
                ext_modules=[
                    setuptools.Extension(
                        localfilename,
                        sources=[sources],
                        extra_compile_args=get_cxxflags(),
                    )
                ],
                cmdclass={"build_ext": BuildExtWithoutPlatformSuffix},
            )
        except SystemExit as err:
            logger.error(
                "Dynamic compilation failed. "
                "You can find more information in %r.",
                sys.stdout.name,
                exc_info=err,
            )
        sys.stdout.flush(), sys.stderr.flush()
    finally:
        sys.argv = argv
        sys.stdout.close()
        sys.stdout = stdout

    if not os.path.isfile(os.path.join(target, so_filename)):
        raise Exception("Error compiling function library!")
