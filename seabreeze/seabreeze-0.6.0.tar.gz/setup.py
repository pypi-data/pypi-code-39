# -*- coding: utf-8 -*-
from setuptools import setup
from distutils.extension import Extension
from distutils.version import LooseVersion
import platform
import sys
import warnings

SEABREEZE_VERSION = "0.6.0"


if "--without-cseabreeze" in sys.argv:
    sys.argv.remove("--without-cseabreeze")  # this is a hack...
    # user requests to not install cython wrapper
    _extensions = []
else:
    # default to building the cython wrapper
    try:
        # try to import cython
        import Cython
        # We require at least version 0.18
        if LooseVersion(Cython.__version__) < LooseVersion("0.18"):
            raise ImportError("Cython version < 0.18")
    except ImportError:
        # if not installed or too old fall back to the provided C file
        cythonize = lambda x: x
        fn_ext = "c"
    else:
        from Cython.Build import cythonize
        fn_ext = "pyx"

    # The windows version of the cython wrapper depends on winusb
    if platform.system() == "Windows":
        libs = ['seabreeze', 'winusb']
    elif platform.system() == "Darwin":
        libs = ['seabreeze']
    else:
        libs = ['seabreeze', 'usb']

    # define extension
    extensions = [Extension('seabreeze.cseabreeze.wrapper',
                        ['./seabreeze/cseabreeze/wrapper.%s' % fn_ext],
                        libraries=libs,
                        library_dirs=['./libs']
                      )]
    _extensions = cythonize(extensions)

setup(
    name='seabreeze',
    version=SEABREEZE_VERSION,
    author='slepton',
    author_email='slepton@posteo.de',
    packages=['seabreeze',
              'seabreeze.cseabreeze',
              'seabreeze.pyseabreeze',
              'seabreeze.pyseabreeze.interfaces'],
    package_dir={'seabreeze': 'seabreeze'},
    package_data={'seabreeze': ['cseabreeze/*.dll', 'cseabreeze/*.lib', 'cseabreeze/*.exp']},
    include_package_data=True,
    url="https://github.com/ap--/python-seabreeze",
    scripts=['scripts/seabreeze-compare'],
    description=("This is a copy of the work done by Andreas Poehlmann with the goal to provide a pypi package for Ocean Optics spectrometers on Python 3.7"""),
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    requires=['python (>= 3.7)', 'pyusb (>= 1.0)', 'numpy'],
    ext_modules=_extensions,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
)
