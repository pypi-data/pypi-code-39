"""Build script for C/C++ extensions. No need to call it, pyproject.toml_ uses this file automatically. This was based
on `Pendulum's extensions`_, as suggested by `this discussion`_ in Poetry's documentation. This script has been
substantially improved, here's how it works:

* The directory tree under ``ext/`` is recursively traversed
* Any leaf subdirectories will be considered to constitute a module, such that
  * The module's name is obtained by joining all the intermediate directories (``ext/`` excluded)
  * The source files will be the ``*.cpp`` files contained in the leaf directory
  * At least one of these source files should be named after the leaf directory itself

So, for instance, the directory tree

    + ext/
    |--+ _plx/
       |--- _plx.cpp
       |--- _plx.h

will result in the ``_plx`` module being built out of the ``ext/_plx/_plx.cpp`` source file.

.. _Pendulum's extensions: https://raw.githubusercontent.com/sdispater/pendulum/1.x/build_extensions.py
.. _pyproject.toml: pyproject.toml
.. _this dicusssion: https://github.com/sdispater/poetry/issues/11
"""

import os
import pathlib
import pybind11
import sysconfig

from distutils.core import Extension
from distutils.command.build_ext import build_ext
from distutils.dir_util import remove_tree


class BuildExtensions(build_ext):
    """Custom extension building command that ensures a clean build.
    """

    def run(self):
        if os.path.exists("build"):
            remove_tree("build")
        os.mkdir("build")
        return super().run()


def build(setup_kwargs):
    """This function is mandatory in order to build the extensions.
    """
    setup_kwargs.update(
        {"ext_modules": extensions, "cmdclass": {"build_ext": BuildExtensions}}
    )


extension_dirs = [
    pathlib.Path(directory)
    for directory, sub_directories, files in os.walk("ext")
    if not sub_directories
]

extensions = [
    Extension(
        name=".".join(extdir.parts[1:]),
        sources=[str(source_path) for source_path in extdir.glob("*.cpp")],
        include_dirs=[pybind11.get_include(), "ext"],
        optional=False,
        language="c++",
        extra_compile_args=sysconfig.get_config_var("CFLAGS").split(),
    )
    for extdir in extension_dirs
]
